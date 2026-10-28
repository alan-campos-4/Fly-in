from pydantic import ValidationError
from inspect import stack


class ParserException(Exception):
    """A custom exception that stores a custom message and field.

    Variables:
        message:    The error message.
        field:      The field or scope of the error, the part of
            the script where it occurs.
    """

    def __init__(self, f: str, n: int, m: str) -> None:
        if '/' in f:
            self.file_name = f.split('/')[-1]
        else:
            self.file_name = f
        self.file_linenum = n
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
