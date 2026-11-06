import os
import json
from pydantic import ValidationError


def get_message_by_key(key: str, add: str | None = None) -> str:
    """Load the json file containing the error messages, try to find
    one with the key, and return the message.

    Args:
        key:    the key that will identify a message from the file.
        add:    an optional string that can be added to the message to
            complete the message.

    Returns:
        a message loaded from the json file, with another string added
            if one was given and the message allows for it.
    """
    curr_dir: str = os.path.dirname(os.path.abspath(__file__))
    with open(curr_dir + '/messages.json', 'r') as f:
        doc = json.load(f)
        msg: str = doc[key]
        if "{}" in msg and add is not None:
            msg = msg.replace("{}", add)
        return msg


class ParserError(Exception):
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
    """Stores a message so it can later be retrieved by a ParserError.

    When called with by_key(), it will try to get an error message
    from the json file, and may also receive an extra value which will
    be inserted into the selected message.

    Variables:
        message:    The message that will be displayed for a given error.
    """

    def __init__(self, message: str) -> None:
        self.message = message

    @classmethod
    def by_key(self, key: str, add: str | None = None) -> "ParserMessage":
        """Load the json file containing the error messages, try to find
        one with the key, and save it in a ParserMesage instance.
        """
        return ParserMessage(get_message_by_key(key, add))

    @classmethod
    def process_error(self, exc: ValidationError) -> "ParserMessage":
        """Retrieve the error message of a Pydantic ValidationError and
        display it more clearly.

        The data will differ depending on what part of the code the error
        is raised by, and the content of the error object.

        Args:
            exc:    the ValidationError object.

        Raises:
            a ParserMessage instance with the ValidationError's message.
        """
        err_msg: str
        loc_str: str
        err = exc.errors()[0]
        err_msg = err['msg']
        if ',' in err_msg:
            err_msg = err_msg.split(', ')[1]
        loc = err['loc']
        if loc and type(loc[0]).__name__ == 'str':
            loc_str = str(loc[0])
            err_msg = "For variable '" + loc_str + "': " + err_msg
        return ParserMessage(err_msg)
