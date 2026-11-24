from pydantic import BaseModel, Field, model_validator
from pydantic.dataclasses import dataclass
from typing_extensions import Self


@dataclass
class Drone():
    ind: int
    path: tuple[int, ...]
    pos: int = Field(init=False, default=0)
    current_node: int = Field(default=-1, init_var=True)
    next_node: int = Field(default=-1)
    next_edge: int = Field(default=-1)
    previous_node: int = Field(default=-1)
    previous_edge: int = Field(default=-1)

    @model_validator(mode='after')
    def check_model(self) -> Self:
        """Set the current node as the the first node of the path, i.e:
        the Graph's start node."""
        if len(self.path) < 2:
            raise ValueError("The path is too short.")
        self.pos = 0
        self.current_node = self.path[self.pos]
        self.next_node = self.path[self.pos + 1]
        return self


if __name__ == "__main__":
    D = Drone(ind=0, path=(0, 8, 5, 4, 2), pos=1, curr_node=8)
    print(D)