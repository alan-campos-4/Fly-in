from typing import Any
from pydantic import ValidationError
from .model_node import Node, ZoneTypes
from .model_graph import Graph
from .field_exception import FieldException


def read_file(filename: str) -> list[str]:
    """Return all the valid lines from a map file as a list.

    The data in the file should be structured as such:
        |nb_drones: x
        |
        |start_hub: ...
        |hub: ...
        |...
        |end_hub ...
        |
        |connection: ...
        |connection: ...
        |...

    Args:
        filename:   the name of the file to read.

    Returns:
        a list containing all the lines in the file with valid data.
    """
    values: list[str] = []
    with open(filename, 'r') as f:
        for line in f:
            l: str = line.strip()
            if l and not l.startswith('#'):
                if ": " in l:
                    values.append(l)
                else:
                    raise FieldException(
                        "file reading",
                        "Invalid line format, must contain ': ' between"
                        "the parameter and its value"
                    )
    return values


def group_values(fld: str,
                 data: list[str]) -> tuple[int, list[str], list[str]]:
    """Divides the map file data it into different variables.

    Args:
        fld:    the scope of this function.
        data:   a list containing all the data read from the map file.

    Returns:
        num_drones: The number of drones, -1 if not found.
        hub_list:   A list with all the hub lines, including
            the first word.
        conn_list:  A list with all the connections lines, excluding
            the first word.

    Raises:
        FieldException: if there are any errors within the values read.
    """
    num_drones: int = -1
    hub_list: list[str] = []
    conn_list: list[str] = []
    for d in data:
        name, value = d.split(':')
        if name == "nb_drones":
            try:
                num_drones = int(value)
            except ValueError:
                raise FieldException(
                    fld, "Found non-valid number of drones "
                    f"value '{num_drones}'"
                )
        elif 'hub' in name:
            hub_list.append(d)
        elif name == 'connection':
            conn_list.append(value)
        else:
            raise FieldException(fld, "Invalid parameter found")
    return num_drones, hub_list, conn_list


def split_metadata(value: str) -> tuple[str, str | None]:
    """Split a given string if it has data enclosed by brackets '[]'

    Args:
        value:  the string to split.

    Returns:
        the separate strings if the value can be split,
            or none if it cannot.

    Raises:
        ValueError, if there more instances of the '[]' characters.
    """
    if '[' in value and ']' in value:
        basic_str, metadata_str = value.strip().split('[')
        return basic_str.strip(), metadata_str.strip('[]')
    return value.strip(), None


def create_node(fld: str, value: str) -> Node:
    """Create a graph node from the value given.

    Args:
        fld:    The scope of this function.
        value:  The string containing data for a specific node.

    Returns:
        A new node object.

    Raises:
        FieldException: if there are any errors within the values read.
    """
    node_values: dict[str, Any] = {}
    try:
        basic_data, metadata = split_metadata(value)
    except ValueError:
        raise FieldException(fld, "Could not parse hub data")
    try:
        nodename, x, y = basic_data.strip().split(' ')
        node_values.update({'name': nodename})
    except ValueError:
        raise FieldException(
            fld, "Could not parse hub data, make sure you are not "
            "missing values"
        )
    try:
        node_values.update({'x': int(x)})
        node_values.update({'y': int(y)})
    except ValueError:
        raise FieldException(
            fld, "Found non-valid hub position value, must be two integers"
        )
    if metadata:
        args = metadata.strip('[]').split(' ')
        for arg in args:
            try:
                argname, argvalue = arg.split('=')
            except ValueError:
                raise FieldException(fld, "Could not parse hub metadata")
            if argname == 'color' and 'color' not in node_values:
                node_values.update({'color': argvalue})
            elif argname == 'max_drones' and 'max_drones' not in node_values:
                try:
                    node_values.update({'max_drones': int(argvalue)})
                except ValueError:
                    raise FieldException(
                        fld,
                        f"Found non-valid max drones value '{argvalue}'"
                    )
            elif argname == 'zone' and 'zone' not in node_values:
                try:
                    node_values.update({'zone': ZoneTypes(argvalue)})
                except ValueError:
                    raise FieldException(
                        fld, f"Found non-valid zone value '{argvalue}'"
                    )
            else:
                raise FieldException(
                    fld, 'Found non-valid metadata for node'
                )
    return Node.model_validate(node_values)


def get_node_data(hub_list: list[str]) -> tuple[dict[int, Node], int, int]:
    """Iterate throught the hub lines from the map file and retrieve
    all the data pertaining to the nodes.

    Args:
        hub_list:   A list with all the hub lines, including
            the first word.

    Returns:
        A dictionary with all of the nodes found, as well as
        the start and end nodes.

    Raises:
        FieldException: if there are any errors within the values read.
    """
    fld: str = 'node parsing'
    node_data: dict[int, Node] = {}
    node_index: int = 0
    start_index: int = -1
    end_index: int = -1
    for node_str in hub_list:
        nodetype, nodevalue = node_str.split(':')
        try:
            nodeobj = create_node(fld, nodevalue.strip())
        except ValidationError as exc:
            raise FieldException.process_error(fld, exc)
        node_data.update({node_index: nodeobj})
        if 'start' in nodetype:
            if start_index == -1:
                start_index = node_index
            else:
                raise FieldException(fld, "Found more than one start node")
        if 'end' in nodetype:
            if end_index == -1:
                end_index = node_index
            else:
                raise FieldException(fld, "Found more than one end node")
        node_index += 1
    if start_index == -1:
        raise FieldException(fld, "Start node missing")
    if end_index == -1:
        raise FieldException(fld, "End node missing")
    return node_data, start_index, end_index


def get_edge_list(node_data: dict[int, Node],
                  conn_list: list[str]) -> list[tuple[int, int, int]]:

    def get_edge_indexes(node_data: dict[int, Node],
                         edge_str_list: list[tuple[str, str, int]]
                         ) -> list[tuple[int, int, int]]:
        """Return a new list of edges with the names of each node replaced
        with their respective indexes.

        Args:
            node_data:      the dictionary containing the graph's nodes.
            edge_str_list:  the list containing the graph's edges,
                stored with the names of the nodes.

        Returns:
            a new list with the node names replaced with indexes.

        Raises:
            KeyError, if a node name in the list does not exist
                in the dictionary.
        """
        name_index_dict: dict[str, int] = {}
        edge_int_list: list[tuple[int, int, int]] = []
        for ind, node in node_data.items():
            name_index_dict.update({node.name: ind})
        for n1, n2, l in edge_list:
            new_n1 = name_index_dict[n1]
            new_n2 = name_index_dict[n2]
            edge_int_list.append((new_n1, new_n2, l))
        return edge_int_list

    """Iterate through the connection lines from the map file and return
    a list with all the data for the edges.

    Args:
        conn_list:  A list with all the connection lines, excluding
            the first word

    Returns:
        A list of tuples containing the start node, the end node,
            and the max capacity of each edge.

    Raises:
        FieldException: if there are any errors within the values read.
    """
    fld: str = 'edge parsing'
    link_capacity: int
    conn_data: str
    conn_metadata: str | None
    edge_list: list[tuple[str, str, int]] = []
    for conn_str in conn_list:
        conn_data, conn_metadata = split_metadata(conn_str)
        if conn_metadata is not None:
            argname, argvalue = conn_metadata.split('=')
            if argname == 'max_link_capacity':
                try:
                    link_capacity = int(argvalue)
                except ValueError:
                    raise FieldException(
                        fld, "Found non-valid value for link capacity"
                    )
            else:
                raise FieldException(
                    fld, "Found non-valid metadata for connection"
                )
        else:
            link_capacity = 1
        try:
            edge_start, edge_end = conn_data.split('-')
            edge_list.append((edge_start, edge_end, link_capacity))
        except ValueError:
            raise FieldException(
                fld, "Could not read edge data, must be divided by '-'"
            )
    try:
        return get_edge_indexes(node_data, edge_list)
    except KeyError:
        raise FieldException(
            fld, "Found edge connected to a non-existent node"
        )


def parse_values(data: list[str]) -> Graph:
    """Create a Graph object from the values retrieved from the txt file.

    Args:
        data:   A list containing all the valid lines
            read from the map file.

    Returns:
        the Graph object formed from those values.

    Raises:
        FieldException: if there are any errors within the values read.
    """

    fld = 'map file reading'
    num_drones, hub_list, conn_list = group_values(fld, data)
    node_data: dict[int, Node] = {}
    edge_list: list[tuple[int, int, int]] = []
    if not hub_list:
        raise FieldException(fld, "No nodes found")
    if not conn_list:
        raise FieldException(fld, "No edges found")
    node_data, start_index, end_index = get_node_data(hub_list)
    edge_list = get_edge_list(node_data, conn_list)
    try:
        g: Graph = Graph(drones=num_drones, nodes=node_data, edges=edge_list,
                         start=start_index, end=end_index)
    except ValidationError as exc:
        raise FieldException.process_error("graph validation", exc)
    else:
        return g

