import os
import json


class ParserException(Exception):
    """A custom exception that stores a message describing the error,
    as well as the file and the line in which it occured.

    Variables:
        filename:   The name of the file in which the error is found.
        linenum:    The number of the line where the error is found.
        message:    The error message.
    """
    filename: str
    linenum: int
    message: str

    def __init__(self, filepath: str, ln: int, msg: str) -> None:
        f = filepath
        if '/' in f:
            f = f.split('/')[-1]
        self.filename = f
        self.linenum = ln
        self.message = msg

    def get_message(self) -> str:
        """Return the full message to display when an error is produced."""

        endstr = (f"An error was found in file '{self.filename}' ")
        if self.linenum == -1:
            endstr += "after reading the file"
        else:
            endstr += f"at line {self.linenum}"
        endstr += f":\n    {self.message}."
        return endstr


class ParserMessage(Exception):
    """Stores a message so it can later be retrieved by a ParserException.

    When called with find_key(), it will try to get an error message
    from the json file, and may also receive an extra value which will
    be inserted into the selected message.

    Variables:
        message:    The message that will be displayed for a given error.
    """

    def __init__(self, message: str) -> None:
        self.message = message

    @classmethod
    def find_key(self, key: str, value: str = None) -> "ParserMessage":
        """Load the json file containing the error messages, try to find
        one with the key, and save it in a ParserMesage instance.

        Args:
            key:    the key that will identify a message from the file.
            value:  a value that will be added to the message.

        Returns:
            a ParserMessage instance whose message has been loaded from
                the json file, with the extra value added if it was given.
        """
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        with open(curr_dir + '/messages.json', 'r') as f:
            doc = json.load(f)
            msg = doc[key]
            if "{}" in msg and value is not None:
                msg = msg.replace("{}", value)
            return ParserMessage(msg)
