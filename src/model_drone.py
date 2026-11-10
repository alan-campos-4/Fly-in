from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self


class Drone(BaseModel):
    """A drone that will travel through the graph.

    Variables:
        ind:            the index of this drone.
        path:           the path this drone will go through.
        current_node:   the current node this drone is located at.
        previous_node:  the index of the node this drone was located at
            in the previous turn.
        previous_edge:  the index of the edge this drone went through
            in the previous turn.
        in_transit:     True if this drone is travelling through the path.
        delivered:      True if this drone has arrived at the end node.
    """
    ind: int
    path: list[int] = []
    current_node: int = Field(default=0)
    previous_node: int = Field(default=-1)
    previous_edge: int = Field(default=-1)
    in_transit: bool = Field(default=True)
    delivered: bool = Field(default=False)
    #transit_destination: Zone | None = None

    def __str__(self) -> str:
        """Return the drone identifier string."""
        return f"D{self.ind + 1}"

    @model_validator(mode='after')
    def check_model(self) -> Self:
        """Ensure that all the data inserted into the Graph is valid."""
        if not self.path:
            raise ValueError(get_message_by_key('PATH_EMPTY'))
        self.current_node = self.path[0]
        return self

    def get_next_node(self) -> int:
        i = 0
        while i < len(self.path):
            if self.path[i] == self.current_node:
                return self.path[i + 1]
            i += 1
        return -1
