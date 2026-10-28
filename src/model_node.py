from pydantic import BaseModel, Field
from enum import Enum


class ZoneTypes(Enum):
    """The different types of zone a node can be located in.

        ◦ normal: Standard zone with 1 turn movement cost.
        ◦ blocked: Inaccessible zone.
        ◦ restricted: Movement to this zone costs 2 turns.
        ◦ priority: Movement to this zone costs 1 turn
            but is prioritized in pathfinding.
    """
    NORMAL = 'normal'
    BLOCKED = 'blocked'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'


class Node(BaseModel):
    """A Node of a Graph. This class stores data pertaining to every node.

    The name of each node, or whether it is the start or the end,
    are not stored in this class and are processed elsewhere.

    Variables:
        x, y:       the position of the node
        color:      the color of the node
        zone:       the zone the node is located in, defined by an enum
        max_drones: the maximum amount of drones that can occupy the node
        distance:   the distance to the start node
    """
    name: str
    x: int
    y: int
    color: str = Field(default="")
    zone: ZoneTypes = Field(default=ZoneTypes.NORMAL)
    max_drones: int = Field(default=1, ge=1)

    def display(self) -> None:
        print(f"  name:  {self.name}")
        print(f"  pos:   [{self.x}, {self.y}]")
        print(f"  zone:  {self.zone.value}")
        print(f"  color: {self.color}")
        print(f"  max:   {self.max_drones}")
