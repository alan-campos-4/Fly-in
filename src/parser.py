from typing import Any
from pydantic import ValidationError
from .models import Graph, Node, ZoneTypes, Edge
from .parser_error import ParserError, ParserMessage


# =============================================
#       GENERAL FUNCTIONS
# =============================================


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


# =============================================
#       NODE FUNCTIONS
# =============================================


def check_soe_found(filedata: dict[str, Any],
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
        raise ParserMessage.by_key('SOE_REPEAT', typestr)
    filedata.update({typestr: node_index})


def create_node(value: str, is_start: bool, is_end: bool) -> Node:
    """Create a graph node from the value given. Store all the data found
    in a dict, and use it with model_validate to create a Node.

    Args:
        value:      A string containing data for a new node, after the ':'.
        is_start:   True if this new node is the start node.
        is_end:     True if this new node is the end node.

    Returns:
        A new node object.

    Raises:
        ParserMessage: if there are any errors within the values read.
    """
    node_values: dict[str, Any] = {}
    try:
        basic_data, metadata = split_metadata(value)
    except ValueError:
        raise ParserMessage.by_key('METADATA_BRACKETS')
    try:
        nodename, x, y = basic_data.strip().split(' ')
        node_values.update({'name': nodename})
    except ValueError:
        raise ParserMessage.by_key('HUB_DATA_SPLIT')
    try:
        node_values.update({'x': int(x)})
        node_values.update({'y': int(y)})
    except ValueError:
        raise ParserMessage.by_key('NON_VALID_TYPE', 'hub position')
    if metadata:
        args = metadata.split(' ')
        for arg in args:
            try:
                argname, argvalue = arg.split('=')
            except ValueError:
                raise ParserMessage.by_key('METADATA_SPLIT')
            is_color = argname == 'color'
            is_zone = argname == 'zone'
            is_md = argname == 'max_drones'
            if is_color or is_md or is_zone:
                if argname in node_values:
                    raise ParserMessage.by_key('METADATA_REPEAT')
                if is_md:
                    try:
                        md = int(argvalue)
                    except ValueError:
                        raise ParserMessage.by_key('CONV', 'max drones')
                    if is_start:
                        raise ParserMessage.by_key('SOE_MAX_DRONES', 'start')
                    if is_end:
                        raise ParserMessage.by_key('SOE_MAX_DRONES', 'end')
                    if md < 1:
                        raise ParserMessage.by_key('INT_VAL', 'Max drones')
                    node_values.update({argname: md})
                elif is_zone:
                    try:
                        node_values.update({argname: ZoneTypes(argvalue)})
                    except ValueError:
                        raise ParserMessage.by_key('HUB_ZONE_CONV')
                else:
                    node_values.update({argname: argvalue})
            else:
                raise ParserMessage.by_key('METADATA_EXTRA')
    return Node.model_validate(node_values)


# =============================================
#       EDGE FUNCTIONS
# =============================================


def find_edge_index(node_name: str, node_dict: dict[int, Node]) -> int:
    """Return the index corresponding to the given node name.

    Args:
        node_name:  The name of the node to find.
        node_dict:  The dict containing all the nodes.

    Returns:
        the index of the node found.

    Raises:
        ParserMessage:  if the index is not found in the dict.
    """
    for index, node in node_dict.items():
        if node.name == node_name:
            return index
    raise ParserMessage.by_key('NODE_NOT_FOUND', node_name)


def create_edge(value: str, node_dict: dict[int, Node]) -> Edge:
    """Create a graph edge from the value given.

    Args:
        value:      A string containing data for a new edge, after the ':'.
        node_dict:  The dict containing all the nodes.

    Returns:
        an edge, represented with the indexes of the two nodes it connects,
            and its maximum link capacity.

    Raises:
        ParserMessage:  if there are any errors within the values read.
    """
    link_capacity: int = 1
    try:
        basic_data, metadata = split_metadata(value)
    except ValueError:
        raise ParserMessage.by_key('METADATA_BRACKETS')
    try:
        node_a_name, node_b_name = basic_data.strip().split('-')
    except ValueError:
        raise ParserMessage.by_key('EDGE_SPLIT')
    node_a_index = find_edge_index(node_a_name, node_dict)
    node_b_index = find_edge_index(node_b_name, node_dict)
    if metadata:
        try:
            argname, argvalue = metadata.split('=')
        except ValueError:
            raise ParserMessage.by_key('METADATA_SPLIT')
        if argname == 'max_link_capacity':
            try:
                link_capacity = int(argvalue)
            except ValueError:
                raise ParserMessage.by_key('EDGE_LINK_CONV')
        else:
            raise ParserMessage.by_key('METADATA_EXTRA')
    return Edge(node_a=node_a_index, node_b=node_b_index,
                max_link_capacity=link_capacity)


# =============================================
#       CHECKING FUNCTIONS
# =============================================


def all_nodenames_unique(node_dict: dict[int, Node]) -> bool:
    """Check that there are no repeated names in the nodes.

    Args:
        node_dict:  a dict containing all the node data.

    Returns:
        True if all the names are unique, False if one is repeated.
    """
    names = [node.name for node in node_dict.values()]
    if len(names) != len(set(names)):
        return False
    return True


def all_positions_unique(node_dict: dict[int, Node]) -> bool:
    """Check that there are no repeated positions in the nodes.

    Args:
        node_dict:  a dict containing all the node data.

    Returns:
        True if all the positions are unique, False if one is repeated.
    """
    positions = [tuple((node.x, node.y)) for node in node_dict.values()]
    if len(positions) != len(set(positions)):
        return False
    return True


def all_edges_unique(edge_dict: dict[int, Edge]) -> bool:
    """Check that all edges found are unique, i.e: there are no edges
    connecting two already connected nodes, in the same or opposite order.

    Returns:
        True if all edges are unique, False otherwise.
    """
    edges_found: set[tuple[int, int]] = set()
    for edge in edge_dict.values():
        if (edge.node_a, edge.node_b) in edges_found:
            return False
        elif (edge.node_b, edge.node_a) in edges_found:
            return False
        else:
            edges_found.add((edge.node_a, edge.node_b))
    return True


def get_isolated_nodes(edges: dict[int, Edge],
                       node_keys: set[int]) -> set[int]:
    """Check if there are any isolated nodes in the graph, i.e: nodes not
    connected to any other node.

    Create two sets with the node indexes found on either side of an edge,
    join them, and compare them to the total amount of nodes found.

    Variables:
        edges:      the dict containing all the edges.
        node_keys:  a set containing all the nodes' indexes.

    Returns:
        a set with the indexes of the isolated nodes, or an empty set
            if all the nodes are connected.
    """
    nodes_a = set([edge.node_a for edge in edges.values()])
    nodes_b = set([edge.node_b for edge in edges.values()])
    nodes_connected = nodes_a.union(nodes_b)
    nodes_missing = node_keys.difference(nodes_connected)
    return nodes_missing


# =============================================
#
#       MAIN PARSER FUNCTION
#
# =============================================


def get_data_from_file(filepath: str) -> Graph:
    """Read the data from a file, iterate through every line, store
    all valid data in a dict, and use model_validate to create a Graph.

    Args:
        filepath:   the path of the file that will be read.

    Returns:
        a Graph object with the data from the file.

    Raises:
        FileNotFoundError:  if the file cannot be opened.
        ParserError:        if the data found in the file is invalid,
            or there is data repeated or missing.
        ValidationError:    if the data cannot validated as a Graph.
    """
    filedata: dict[str, Any] = {}
    node_dict: dict[int, Node] = {}
    edge_dict: dict[int, Edge] = {}
    node_index: int = 0
    edge_index: int = 0
    is_hub: bool = False
    is_sh: bool = False
    is_eh: bool = False
    with open(filepath, 'r') as fileobj:
        for linenum, line in enumerate(fileobj, start=1):
            l: str = line.strip()
            if l and not l.startswith('#'):
                try:
                    try:
                        name, data = l.split(':')
                    except ValueError:
                        raise ParserMessage.by_key('COLON_MISS')
                    if name == 'nb_drones':
                        if 'nb_drones' in filedata:
                            raise ParserMessage.by_key('NBD_REPEAT')
                        try:
                            nb_drones = int(data)
                        except ValueError:
                            raise ParserMessage.by_key('NON_VALID_TYPE',
                                                       'number of drones')
                        if nb_drones < 1:
                            raise ParserMessage.by_key('INT_VAL',
                                                       'Number of drones')
                        filedata.update({'nb_drones': nb_drones})
                    elif name == 'connection':
                        if not node_dict:
                            raise ParserMessage.by_key('HUB_AFTER_CONN')
                        try:
                            new_edge = create_edge(data, node_dict)
                        except ValidationError as e:
                            raise ParserMessage.process_error(e)
                        edge_dict.update({edge_index: new_edge})
                        if not all_edges_unique(edge_dict):
                            raise ParserMessage.by_key('EDGE_NOT_UNIQUE')
                        edge_index += 1
                    else:
                        is_hub = name == 'hub'
                        is_sh = name == 'start_hub'
                        is_eh = name == 'end_hub'
                        if is_hub or is_sh or is_eh:
                            if edge_dict:
                                raise ParserMessage.by_key('CONN_AFTER_HUB')
                            try:
                                new_node = create_node(data, is_sh, is_eh)
                            except ValidationError as e:
                                raise ParserMessage.process_error(e)
                            node_dict.update({node_index: new_node})
                            if not all_nodenames_unique(node_dict):
                                raise ParserMessage.by_key('NAME_NOT_UNIQUE')
                            if not all_positions_unique(node_dict):
                                raise ParserMessage.by_key('POS_NOT_UNIQUE')
                            if is_sh:
                                check_soe_found(filedata, node_index, 'start')
                            if is_eh:
                                check_soe_found(filedata, node_index, 'end')
                            node_index += 1
                        else:
                            raise ParserMessage.by_key('LINE_NOT_VALID')
                except ParserMessage as e:
                    raise ParserError(filepath, linenum, e.message)
    try:
        if not node_dict:
            raise ParserMessage.by_key('NODES_MISS')
        if not edge_dict:
            raise ParserMessage.by_key('EDGES_MISS')
        if 'start' not in filedata:
            raise ParserMessage.by_key('START_MISS')
        if 'end' not in filedata:
            raise ParserMessage.by_key('END_MISS')
        iso_nodes = get_isolated_nodes(edge_dict, set(node_dict.keys()))
        if len(iso_nodes) > 0:
            iso_node_names = [node_dict[i].name for i in iso_nodes]
            raise ParserMessage.by_key('NODES_LEFT', ", ".join(iso_node_names))
    except ParserMessage as e:
        raise ParserError(filepath, -1, e.message)
    filedata.update({'nodes': node_dict})
    filedata.update({'edges': edge_dict})
    try:
        g = Graph.model_validate(filedata)
    except ValidationError as exc:
        raise ParserError.process_error(filepath, -1, exc)
    return g
