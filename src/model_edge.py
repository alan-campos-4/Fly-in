from pydantic import BaseModel, Field


class Edge(BaseModel):
    """An Edge in a Graph.

    Variables:
        node_a:             the index of the first node in this edge.
        node_b:             the index of the second node in this edge.
        max_link_capaciy:   the maximum amount of drones that can pass
                        through this edge simultaniously.
    """
    node_a: int = Field(ge=0)
    node_b: int = Field(ge=0)
    max_link_capacity: int = Field(ge=1)
