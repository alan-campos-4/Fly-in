from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self
from .node import Node


class Path(BaseModel):
    node_list: tuple[int, ...]
    size: int = Field(default=1)
    cost: int = Field(default=1)

    @model_validator(mode='after')
    def check_model(self) -> Self:
        """Obtain the size of the path."""
        self.size = len(self.node_list)
        return self

    def set_cost(self, nodes: dict[int, Node]) -> None:
        """Assign a cost to the Path depending of zone types of its nodes."""
        cost = 0
        for p in self.node_list:
            zone = nodes[p].zone.value
            if zone == 'restricted':
                cost += 2
            else:
                cost += 1
        self.cost = cost