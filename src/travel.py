from .model_graph import Graph


def travel(g: Graph, path: list[int]) -> None:
    drone_dict = {f"D{(i+1)}": 0 for i in range(g.drones)}
    print(drone_dict)
