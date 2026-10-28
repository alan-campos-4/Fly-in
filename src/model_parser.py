import os
from typing import Any
from pydantic import ValidationError
from .model_node import Node, ZoneTypes
from .model_graph import Graph
from .parser_exception import ParserException


def create_node(value: str) -> Node:
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


def create_edge(fld: str, value: str) -> tuple(int, int, int):
    """..."""

    return 0, 0, 0


def create_name_index_dict()
    """..."""
    name_index_dict: dict[str, int] = {}
    edge_int_list: list[tuple[int, int, int]] = []
    for ind, node in node_data.items():
        name_index_dict.update({node.name: ind})
    return name_index_dict


def get_data_from_file(filename: str) -> dict[str, Any]:
    """..."""

    filedata: dict[str, Any] = {}
    node_data: dict[int, Node] = {}
    edge_list: list[tuple[int, int, int]] = []
    node_index: int = 0
    have_found_nb: bool = False
    have_found_hubs: bool = False
    have_found_conns: bool = False
    if not os.path.isfile(filename):
        return None
    with open(filename, 'r') as f:
        for n, line in enumerate(f, start=1):
            l: str = line.strip()
            if l and not l.startswith('#'):
                if ": " in l:
                    name, data = l.split(':')
                    if name == 'nb_drones':
                        if 'nb_drones' in filedata:
                            raise ParserException(
                                filename, n,
                                "Cannot have more than one number of drones"
                            )
                        filedata.update({'nb_drones', int(data)})
                        have_found_nb = True
                    elif 'hub' in name:
                        if edge_list:
                            raise ParserException(
                                filename, n,
                                "The hubs must be placed before the connections"
                            )
                        new_node = create_node(data, f, n)
                        node_data.update({node_index, new_node})
                        node_index += 1
                        have_found_hubs = True
                    elif name == 'connection':
                        edge_list.append()
                        have_found_conns = True
                else:
                    raise ParserException(
                        filename, n,
                        "Invalid line format, must contain ': ' between "
                        "the parameter and its value"
                    )
    return filedata