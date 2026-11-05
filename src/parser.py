import os
from typing import Any
from .model_node import Node, ZoneTypes
from .parser_exception import ParserException, ParserMessage


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
        raise ParserMessage.find_key('SOE_REPEAT', typestr)
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
        raise ParserMessage.find_key('METADATA_BRACKETS')
    try:
        nodename, x, y = basic_data.strip().split(' ')
        node_values.update({'name': nodename})
    except ValueError:
        raise ParserMessage.find_key('HUB_DATA_SPLIT')
    try:
        node_values.update({'x': int(x)})
        node_values.update({'y': int(y)})
    except ValueError:
        raise ParserMessage.find_key('NON_VALID_TYPE', 'hub position')
    if metadata:
        args = metadata.split(' ')
        for arg in args:
            try:
                argname, argvalue = arg.split('=')
            except ValueError:
                raise ParserMessage.find_key('METADATA_SPLIT')
            match argname:
                case 'color' | 'max_drones' | 'zone':
                    if argname in node_values:
                        raise ParserMessage.find_key('METADATA_REPEAT')
                    match argname:
                        case 'max_drones':
                            try:
                                md = int(argvalue)
                            except ValueError:
                                raise ParserMessage.find_key('CONV',
                                                             'max drones')
                            if md < 1:
                                raise ParserMessage.find_key('INT_VAL',
                                                             'Max drones')
                            node_values.update({argname: md})
                        case 'zone':
                            try:
                                node_values.update({argname:
                                                    ZoneTypes(argvalue)})
                            except ValueError:
                                raise ParserMessage.find_key('HUB_ZONE_CONV')
                        case _:
                            node_values.update({argname: argvalue})
                case _:
                    raise ParserMessage.find_key('METADATA_EXTRA')
    return Node.model_validate(node_values)


def all_positions_unique(node_dict: dict[int, Node]) -> bool:
    """Check that there are no repeated positions in the nodes.

    Args:
        node_dict:  a dict containing all the node data.

    Returns:
        True if all the positions are unique, False if one is repeated.
    """
    positions: set[tuple[int, ...]] = set()
    for node in node_dict.values():
        t = tuple((node.x, node.y))
        if t in positions:
            return False
        else:
            positions.add(t)
    return True


# =============================================
#       EDGE FUNCTIONS
# =============================================


def find_edge_index(node_name: str, node_dict: dict[int, Node]) -> int:
    """Return the index corresponding to the given node name.

    Args:
        node_name:  The name of the node to find.
        node_dict:  The dict containing all the nodes.

    Returns:
        the index of the node found, or -1 if it's not found.
    """
    for index, node in node_dict.items():
        if node.name == node_name:
            return index
    return -1


def create_edge(value: str,
                node_dict: dict[int, Node]) -> tuple[int, int, int]:
    """Create a graph edge from the value given.

    Args:
        value:      A string containing the file's data on a single edge.
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
        raise ParserMessage.find_key('METADATA_BRACKETS')
    try:
        edge_start, edge_end = basic_data.strip().split('-')
    except ValueError:
        raise ParserMessage.find_key('EDGE_SPLIT')
    edge_start_index = find_edge_index(edge_start, node_dict)
    edge_end_index = find_edge_index(edge_end, node_dict)
    if edge_start_index == -1:
        raise ParserMessage.find_key('EDGE_NODE_MISS', 'first')
    if edge_end_index == -1:
        raise ParserMessage.find_key('EDGE_NODE_MISS', 'second')
    if metadata:
        try:
            argname, argvalue = metadata.split('=')
        except ValueError:
            raise ParserMessage.find_key('METADATA_SPLIT')
        if argname == 'max_link_capacity':
            try:
                link_capacity = int(argvalue)
            except ValueError:
                raise ParserMessage.find_key('EDGE_LINK_CONV')
        else:
            raise ParserMessage.find_key('METADATA_EXTRA')
    return edge_start_index, edge_end_index, link_capacity


def all_edges_unique(edge_dict: dict[int, tuple[int, int, int]]) -> bool:
    """Check that there are no repeated edges in the list, i.e:
    two edges connecting the same two nodes.

    Returns:
        True, if all edges are unique
    """
    edges_found: set[tuple[int, int]] = set()
    for n1, n2, l in edge_dict.values():
        if (n1, n2) in edges_found:
            return False
        elif (n2, n1) in edges_found:
            return False
        else:
            edges_found.add((n1, n2))
    return True


def check_soe_connected(edge_dict: dict[int, tuple[int, int, int]],
                        start: int, end: int) -> None:
    """Iterate through the edge list and check if the start and end nodes
    are found within it.

    Args:
        edge_dict:  a dict containin all of the graph's edges.
        start:      the index of the start node.
        end:        the index of the end node.

    Raises:
        ParserMessage:  if the start or end node is missing from the dict.
    """
    found_start: bool = False
    found_end: bool = False
    for n1, n2, l in edge_dict.values():
        if n1 == start or n2 == start:
            found_start = True
        if n1 == end or n2 == end:
            found_end = True
        if found_start is True and found_end is True:
            return None
    f: str = ""
    match found_start, found_end:
        case False, True:
            f = "start node is"
        case False, False:
            f = "start and end nodes are"
        case _:
            f = "end node is"
    raise ParserMessage.find_key('EDGE_NOT_CONN', f)


# =============================================
#
#       MAIN PARSER FUNCTION
#
# =============================================


def get_data_from_file(filepath: str) -> dict[str, Any]:
    """Read the data from a file and return it in a format that can be
    passed to the Map class' model_validate.

    Args:
        filepath:   the file that will be read.

    Returns:
        the valid data within the file stored a dict.

    Raises:
        ParserException:    if any error is found within the file.
    """
    filedata: dict[str, Any] = {}
    if not os.path.isfile(filepath):
        return filedata
    node_dict: dict[int, Node] = {}
    edge_dict: dict[int, tuple[int, int, int]] = {}
    node_index: int = 0
    edge_index: int = 0
    is_hub: bool = False
    is_hub_s: bool = False
    is_hub_e: bool = False
    with open(filepath, 'r') as fileobj:
        for linenum, line in enumerate(fileobj, start=1):
            l: str = line.strip()
            if l and not l.startswith('#'):
                try:
                    try:
                        name, data = l.split(':')
                    except ValueError:
                        raise ParserMessage.find_key('COLON_MISS')
                    if name == 'nb_drones':
                        if 'nb_drones' in filedata:
                            raise ParserMessage.find_key('NBD_REPEAT')
                        try:
                            nb_drones = int(data)
                        except ValueError:
                            raise ParserMessage.find_key('NON_VALID_TYPE',
                                                         'number of drones')
                        if nb_drones < 1:
                            raise ParserMessage.find_key('INT_VAL',
                                                         'Number of drones')
                        filedata.update({'nb_drones': nb_drones})
                    elif name == 'connection':
                        if not node_dict:
                            raise ParserMessage.find_key('HUB_AFTER_CONN')
                        new_edge = create_edge(data, node_dict)
                        edge_dict.update({edge_index: new_edge})
                        if not all_edges_unique(edge_dict):
                            raise ParserMessage.find_key('EDGE_NOT_UNIQUE')
                        edge_index += 1
                    else:
                        is_hub = name == 'hub'
                        is_hub_s = name == 'start_hub'
                        is_hub_e = name == 'end_hub'
                        if is_hub or is_hub_s or is_hub_e:
                            if edge_dict:
                                raise ParserMessage.find_key('CONN_AFTER_HUB')
                            new_node = create_node(data)
                            node_dict.update({node_index: new_node})
                            if not all_positions_unique(node_dict):
                                raise ParserMessage.find_key('POS_NOT_UNIQUE')
                            if is_hub_s:
                                check_soe_found(filedata, node_index, 'start')
                            if is_hub_e:
                                check_soe_found(filedata, node_index, 'end')
                            node_index += 1
                        else:
                            raise ParserMessage("Invalid name found")
                except ParserMessage as e:
                    raise ParserException(filepath, linenum, e.message)
    try:
        if not node_dict:
            raise ParserMessage.find_key('NODES_MISS')
        if not edge_dict:
            raise ParserMessage.find_key('EDGES_MISS')
        if 'start' not in filedata:
            raise ParserMessage.find_key('START_MISS')
        if 'end' not in filedata:
            raise ParserMessage.find_key('END_MISS')
        check_soe_connected(edge_dict, filedata['start'], filedata['end'])
    except ParserMessage as e:
        raise ParserException(filepath, -1, e.message)
    filedata.update({'nodes': node_dict})
    filedata.update({'edges': edge_dict})
    return filedata
