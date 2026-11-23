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
        delivered:      True if this drone has arrived at the end node.
    """
    ind: int
    path: tuple[int, ...]
    current_node: int = Field(default=0)
    previous_node: int = Field(default=-1)
    previous_edge: int = Field(default=-1)
    delivered: bool = Field(default=False)

    def __str__(self) -> str:
        """Return the drone identifier string."""
        return f"D{self.ind + 1}"

    @model_validator(mode='after')
    def check_model(self) -> Self:
        """Set the current node as the the first node of the path, i.e:
        the Graph's start node."""
        self.current_node = self.path[0]
        return self

    def get_next_node(self) -> int:
        """Return the index of the next node in the path"""
        i = 0
        while i < len(self.path) - 1:
            if self.path[i] == self.current_node:
                return self.path[i + 1]
            i += 1
        return -1
