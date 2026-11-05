import os
import json
import sys


class ParserMessage(Exception):
    error_messages = {
        "COLON_MISS": "Invalid line format, must contain ': ' between the parameter and its value",
        "NON_VALID_TYPE": "Found non-valid type for {}",
        "ZONE_VALUE": "Found non-valid zone value, must be 'normal', "
            "'blocked', 'restricted' or 'priority'",
        "INT_VAL": "{} value must be an equal or greater than 1",
        "HUB_DATA_SPLIT": "Found an incorrent amount of hub data",
        "EDGE_SPLIT": "Edge node names should be separated with '-'",
        "EDGE_NODE_MISS": "Could not find the edge's {} node",
        "EDGE_NOT_CONN": "The {} not connected to the graph",
        "METADATA_BRACKETS": "Metadata should be wrapped in []",
        "METADATA_SPLIT": "Metadata argument and value must be separated with '='",
        "METADATA_REPEAT": "Metadata contains repeated argument",
        "METADATA_EXTRA": "Metadata contains non-valid argument",
        "SOE_REPEAT": "There can only be one {} node",
        "NBD_REPEAT": "There can only be one number of drones",
        "CONN_AFTER_HUB": "The hubs must be placed before the connections",
        "HUB_AFTER_CONN": "The connections must be placed after the hubs",
        "EDGE_NOT_UNIQUE": "Found two different edges connecting the same two nodes",
        "POS_NOT_UNIQUE": "Found two nodes with the same coordinate values",
        "NODES_MISS": "No nodes were found",
        "EDGES_MISS": "No edges were found",
        "START_MISS": "A start node could not be found",
        "END_MISS": "An end node could not be found",
    }

    def __init__(self, message: str) -> None:
        self.message = message

    @classmethod
    def find_key(self, key: str, value: str = None) -> "ParserMessage":
        msg = self.error_messages[key]
        if "{}" in msg and value is not None:
            msg = msg.replace("{}", value)
        return ParserMessage(msg)


class ParserGetter(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    @classmethod
    def find_key(self, key: str, value: str = None) -> "ParserGetter":
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        with open(curr_dir + '/messages.json', 'r') as f:
            doc = json.load(f)
            msg = doc[key]
            if "{}" in msg and value is not None:
                msg = msg.replace("{}", value)
            return ParserGetter(msg)


if __name__ == "__main__":
    choice: int = 0
    if len(sys.argv) == 2:
        choice = int(sys.argv[-1])
    if choice == 0:
        try:
            raise ParserMessage.find_key('HUB_AFTER_CONN')
        except ParserMessage as e:
            print(e.message)
    else:
        try:
            raise ParserGetter.find_key('METADATA_SPLIT')
        except ParserGetter as e:
            print(e.message)