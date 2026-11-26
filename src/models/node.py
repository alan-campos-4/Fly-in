from pydantic import BaseModel, Field
from enum import Enum


class ZoneTypes(Enum):
    """The different types of zone a node can be located in.

    - normal: Movement to this zone costs 1 turn.
    - restricted: Movement to this zone costs 2 turns.
    - priority: Movement to this zone costs 1 turn
        but is prioritized in pathfinding.
    - blocked: Inaccessible zone.
    """
    NORMAL = 'normal'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'
    BLOCKED = 'blocked'


class Node(BaseModel):
    """A Node in a Graph.

    Variables:
        name:           the name of this node, unique to each one.
        x, y:           the position of this node.
        zone:           the zone this node is located in, defined by an enum.
        color:          the color of this node.
        max_drones:     the maximum amount of drones that can occupy this node.
        curr_drones:    the amount of drones occupying this node.
    """
    name: str
    x: int
    y: int
    zone: ZoneTypes = Field(default=ZoneTypes.NORMAL)
    color: str = Field(default="")
    max_drones: int = Field(default=1, ge=1)
    curr_drones: int = Field(default=0, ge=0)

    def display(self) -> None:
        print(f"  name:  {self.name}")
        print(f"  pos:   [{self.x}, {self.y}]")
        print(f"  zone:  {self.zone.value}")
        print(f"  color: {self.color}")
        print(f"  max:   {self.max_drones}")
