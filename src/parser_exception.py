from pydantic import ValidationError
from inspect import stack


class ParserMessage(Exception):
    """A custom exception that represents a ParserException's message."""
    def __init__(self, message) -> None:
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
        fn: str = f
        if '/' in f:
            fn = fn.split('/')[-1]
        self.filename = fn
        self.linenum = n
        self.message = m

    @classmethod
    def process_error(self, f: str, n: int,
                      exc: ValidationError) -> "ParserException":
        """Retrieve the error message of a Pydantic ValidationError and
        display it more clearly.

        The data will differ depending on what part of the code the error
        is raised by, and the content of the error object.

        Args:
            fld:    the field or scope of the error.
            exc:    the ValidationError object.

        Raises:
            a ParserException with the most appropiate data.
        """
        err = exc.errors()[0]
        err_msg = err['msg'].split(', ')[1]
        return ParserException(f, n, err_msg)
