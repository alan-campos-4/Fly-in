import os
from typing import Any
from .model_node import Node, ZoneTypes
from .parser_exception import ParserException, ParserMessage


# ==============================
#       GENERAL FUNCTIONS
# ==============================


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


# ==============================
#       NODE FUNCTIONS
# ==============================


def check_start_end(filedata: dict[str, Any],
                node_index: int, typestr: str) -> None:
    """Try to establish the given node, identified by its index, as
    the graph's start or end node.

    Args:
        filedata:   the dict that contains the data read from the file.
        node_type:  the index of the node being checked.
        typestr:    'start' or 'end'.

    Raises:
        ParserMessage:  if the given special node already exists.
    """

    if typestr in filedata:
        raise ParserMessage(f"There can only be one {typestr} node")
    filedata.update({typestr: node_index})


def create_node(value: str) -> Node:
    """Create a graph node from the value given. Store all the data found
    in a dict, and use it with model_validate to create a Node.

    Args:
        value:  The string containing data for a specific node.

    Returns:
        A new node object.

    Raises:
        ParserMessage: if there are any errors within the values read.
    """
    node_values: dict[str, Any] = {}
    try:
        basic_data, metadata = split_metadata(value)
    except ValueError:
        raise ParserMessage(
            "A hub's metadata should be wrapped in []"
        )
    try:
        nodename, x, y = basic_data.strip().split(' ')
        node_values.update({'name': nodename})
    except ValueError:
        raise ParserMessage(
            "There is an incorrent amount of hub values"
        )
    try:
        node_values.update({'x': int(x)})
        node_values.update({'y': int(y)})
    except ValueError:
        raise ParserMessage(
            "Found non-valid hub position value, must be two integers"
        )
    if metadata:
        args = metadata.strip('[]').split(' ')
        for arg in args:
            try:
                argname, argvalue = arg.split('=')
            except ValueError:
                raise ParserMessage(
                    "Metadata and value must be "
                    "separated wuth '='"
                )
            if argname == 'color' and 'color' not in node_values:
                node_values.update({'color': argvalue})
            elif argname == 'max_drones' and 'max_drones' not in node_values:
                try:
                    node_values.update({'max_drones': int(argvalue)})
                except ValueError:
                    raise ParserMessage(
                        f"Found non-valid max drones value '{argvalue}'"
                    )
            elif argname == 'zone' and 'zone' not in node_values:
                try:
                    node_values.update({'zone': ZoneTypes(argvalue)})
                except ValueError:
                    raise ParserMessage(
                        f"Found non-valid zone value '{argvalue}'"
                    )
            else:
                raise ParserMessage(
                    'Found non-valid metadata for node'
                )
    return Node.model_validate(node_values)


def all_positions_unique(node_data: dict[int, Node]) -> bool:
    """Check that there are no repeated positions in the nodes.

    Args:
        node_data:  a dict containing all the node data.

    Returns:
        True if all the positions are unique, False if one is repeated.
    """
    positions: set[tuple[int, ...]] = set()
    for node in node_data.values():
        t = tuple((node.x, node.y))
        if t in positions:
            return False
        else:
            positions.add(t)
    return True


# ==============================
#       EDGE FUNCTIONS
# ==============================


def find_edge_index(node_name: str, node_data: dict[int, Node]) -> int:
    """Return the index corresponding to the given node name.

    Args:
        node_name:  The name of the node to find.
        node_data:  The dict containing all the nodes.

    Returns:
        the index of the node found, or -1 if it's not found.
    """
    for index, node in node_data.items():
        if node.name == node_name:
            return index
    return -1


def create_edge(value: str,
                node_data: dict[int, Node]) -> tuple[int, int, int]:
    """Create a graph edge from the value given.

    Args:
        value:      A string containing the file's data on a single edge.
        node_data:  The dict containing all the nodes.

    Returns:
        an edge, represented with the indexes of the two nodes it connects,
            and its maximum link capacity.

    Raises:
        ParserMessage: if there are any errors within the values read.
    """

    link_capacity: int = 1
    try:
        basic_data, metadata = split_metadata(value)
    except ValueError:
        raise ParserMessage(
            "An edge's metadata should be wrapped in []"
        )
    try:
        edge_start, edge_end = basic_data.strip().split('-')
    except ValueError:
        raise ParserMessage(
            "An edge's node names should be separated with '-'"
        )
    edge_start_index = find_edge_index(edge_start, node_data)
    edge_end_index = find_edge_index(edge_end, node_data)
    if edge_start_index == -1:
        raise ParserMessage("Could not find the edge's start node")
    if edge_end_index == -1:
        raise ParserMessage("Could not find the edge's end node")
    if metadata:
        try:
            argname, argvalue = metadata.split('=')
        except ValueError:
            raise ParserMessage(
                "Metadata and value must be separated with '='"
            )
        if argname == 'max_link_capacity':
            try:
                link_capacity = int(argvalue)
            except ValueError:
                raise ParserMessage(
                    "Found non-valid value for link capacity"
                )
        else:
            raise ParserMessage(
                "Found non-valid metadata for connection"
            )
    return edge_start_index, edge_end_index, link_capacity


def all_edges_unique(edge_list: list[tuple[int, int, int]]) -> bool:
    """Check that there are no repeated edges in the list
    two edges connecting the same two nodes."""

    edges_found: set[tuple[int, int]] = set()
    for n1, n2, l in edge_list:
        if (n1, n2) in edges_found:
            return False
        elif (n2, n1) in edges_found:
            return False
        else:
            edges_found.add((n1, n2))
    return True


def start_end_connected(edge_list: list[tuple[int, int, int]],
                        start: int, end: int) -> None:
    """Iterate through the edge list and check if the start and end nodes
    are found within it.

    Args:
        edge_list:  a list containin all of the graph's edges.
        start:      the index of the start node.
        end:        the index of the end node.

    Raises:
        ParserMessage:  
    """
    found_start: bool = False
    found_end: bool = False
    for n1, n2, l in edge_list:
        if found_start is False and (n1 == start or n2 == start):
            found_start = True
        if found_end is False and (n1 == end or n2 == end):
            found_end = True
        if found_start and found_end:
            return None
    f: str = ""
    match found_start, found_end:
        case True, False:
            f = "end node is"
        case False, True:
            f = "start node is"
        case _:
            f = "start and end nodes are"
    raise ParserMessage(f"The {f} not connected to the graph")


# ==============================
#
#   MAIN PARSER FUNCTION
#
# ==============================


def get_data_from_file(filename: str) -> dict[str, Any]:
    """Read the data from a file and return it in a format that can be
    passed to the Map class' model_validate.

    Args:
        filename:   the file that will be read.

    Returns:
        the valid data within the file stored a dict.

    Raises:
        ParserException:    if any error is found within the file.
    """
    filedata: dict[str, Any] = {}
    if not os.path.isfile(filename):
        return filedata
    node_data: dict[int, Node] = {}
    edge_list: list[tuple[int, int, int]] = []
    node_index: int = 0
    is_hub: bool = False
    is_hub_s: bool = False
    is_hub_e: bool = False
    with open(filename, 'r') as fileobj:
        for n, line in enumerate(fileobj, start=1):
            l: str = line.strip()
            if l and not l.startswith('#'):
                try:
                    name, data = l.split(':')
                    if name == 'nb_drones':
                        if 'nb_drones' in filedata:
                            raise ParserMessage(
                                "Cannot have more than one number of drones"
                            )
                        try:
                            nb_drones = int(data)
                        except ValueError:
                            raise ParserMessage(
                                "Invalid value for number of drones"
                            )
                        if nb_drones < 1:
                            raise ParserMessage(
                                "Number of drones cannot be lower than 1"
                            )
                        filedata.update({'nb_drones': nb_drones})
                    elif name == 'connection':
                        if not node_data:
                            raise ParserMessage(
                                "The connections must be placed after the hubs"
                            )
                        new_edge = create_edge(data, node_data)
                        edge_list.append(new_edge)
                        if not all_edges_unique(edge_list):
                            raise ParserMessage(
                                "Found two different edges "
                                "connecting the same two nodes"
                            )
                    else:
                        is_hub = name == 'hub'
                        is_hub_s = name == 'start_hub'
                        is_hub_e = name == 'end_hub'
                        if is_hub or is_hub_s or is_hub_e:
                            if edge_list:
                                raise ParserMessage(
                                    "The hubs must be placed "
                                    "before the connections"
                                )
                            new_node = create_node(data)
                            node_data.update({node_index: new_node})
                            if not all_positions_unique(node_data):
                                raise ParserMessage(
                                    "Found two nodes with the same "
                                    "coordinate values"
                                )
                            if is_hub_s:
                                check_start_end(filedata, node_index, 'start')
                            if is_hub_e:
                                check_start_end(filedata, node_index, 'end')
                            node_index += 1
                        else:
                            raise ParserMessage("Invalid name found")
                except ValueError:
                    raise ParserMessage(
                        "Invalid line format, must contain ': ' between "
                        "the parameter and its value"
                    )
                except ParserMessage as e:
                    raise ParserException(filename, n, e.message)
    try:
        if not node_data:
            raise ParserMessage("No nodes could be found")
        if not edge_list:
            raise ParserMessage("No edges could be found")
        if 'start' not in filedata:
            raise ParserMessage("No start node could be found")
        if 'end' not in filedata:
            raise ParserMessage("No end node could be found")
        start_end_connected(edge_list, filedata['start'], filedata['end'])
    except ParserMessage as e:
        raise ParserException(filename, -1, e.message)
    filedata.update({'nodes': node_data})
    filedata.update({'edges': edge_list})
    return filedata
