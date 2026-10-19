from pydantic import ValidationError
from inspect import stack


class FieldException(Exception):
    """A custom exception that stores a custom message and field.

    Variables:
        message:    The error message.
        field:      The field or scope of the error, the part of
            the script where it occurs.
    """

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        self.p = stack()[1].function

    @classmethod
    def process_error(self, fld: str,
                      exc: ValidationError) -> "FieldException":
        """Retrieve the error message of a Pydantic ValidationError and
        display it more clearly.

        The data will differ depending on what part of the code the error
        is raised by, and the content of the error object.

        Args:
            fld:    the field or scope of the error.
            exc:    the ValidationError object.

        Raises:
            a FieldException with the most appropiate data.
        """
        err = exc.errors()[0]
        err_msg = err['msg'].split(', ')[1]
        return FieldException(fld, err_msg)
