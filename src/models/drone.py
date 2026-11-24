from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self


class Drone(BaseModel):
    """A drone that will travel through the graph.

    Variables:
        ind:        the index of this drone.
        path:       the path this drone will go through.
        pos:        the position of this drone within its path.
        curr_node:  the index of the node this drone is located at.
        next_node:  the index of the node this drone will try to move
            in the next turn.
        prev_node:  the index of the node this drone was located at
            in the previous turn.
        prev_edge:  the index of the edge this drone went through
            in the previous turn.
        delivered:  True if this drone has arrived at the end node.
        in_transit: True if this drone is traversing a restricted zone.

    If prev_node = -1, the drone is at the start of the path.
    If next_node = -1, the drone is at the end of the path.
    if curr_node = -1, the drone is in transit inside an edge.
    """
    ind: int
    path: tuple[int, ...]
    pos: int = Field(default=0)
    curr_node: int = Field(default=-1)
    next_node: int = Field(default=-1)
    prev_node: int = Field(default=-1)
    prev_edge: int = Field(default=-1)
    delivered: bool = Field(default=False)
    in_transit: bool = Field(default=False)

    def __str__(self) -> str:
        """Return the drone identifier string."""
        return f"D{self.ind + 1}"

    @model_validator(mode='after')
    def check_model(self) -> Self:
        """Obtain the current and next nodes from the path."""
        if len(self.path) < 2:
            raise ValueError("The path is too short")
        self.curr_node = self.path[self.pos]
        self.next_node = self.path[self.pos + 1]
        return self

    def update_next_node(self) -> None:
        """Determine the next node for this drone.
        Set it as -1 if the end has been reached."""
        if self.pos + 1 >= len(self.path):
            self.next_node = -1
        else:
            self.next_node = self.path[self.pos + 1]

    def move_to_next_node(self) -> None:
        """Move this drone to the next node, and change its variables
        accordingly.

        During transit, curr_node is set to -1, so prev_node is not updated.
        """
        self.pos += 1
        if not self.in_transit:
            self.prev_node = self.curr_node
        self.curr_node = self.next_node
        if self.curr_node == self.path[-1]:
            self.delivered = True
