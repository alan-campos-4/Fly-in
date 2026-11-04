class ParserMessage(Exception):
    """A custom exception that represents a ParserException's message."""
    def __init__(self, message: str) -> None:
        self.message = message


class ParserException(Exception):
    """A custom exception that stores in which file and line the error occured.

    Variables:
        filename:   The name of the file in which the error is found.
        linenum:    The number of the line where the error is found.
        message:    The error message.
    """
    filename: str
    linenum: int
    message: str

    def __init__(self, f: str, n: int, m: str) -> None:
        if '/' in f:
            f = f.split('/')[-1]
        self.filename = f
        self.linenum = n
        self.message = m

    def get_message(self) -> str:
        """Return the full message to display if an error is produced."""
        endstr = (f"An error was found in file '{self.filename}' ")
        if self.linenum == -1:
            endstr += "after reading the file"
        else:
            endstr += f"at line {self.linenum}"
        endstr += f":\n    {self.message}."
        return endstr
