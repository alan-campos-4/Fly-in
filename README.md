*This project has been created as part of the 42 curriculum by alvespin.*

# FLY-IN

<div align="center">
    <img src="assets/graph.svg" width="50%">
</div>
<br>

## Table of Contents

1. [Description](#description)
2. [Intructions](#instructions)
3. [Resources](#resources)

---
## Description

...

#### Pathfinding limitations

Blocked zones: nodes marked with this zonetype are removed from the adjancency list before pathfinding starts, thus preventing them from being used in the algorithm.

Priority zones: nodes marked with this zonetype are checked during pathfinding and assigned as the parent of a node when appropiate

Restricted zones:
...

#### Benchmarks

| Map name | Shortest path (nodes) | Best Result (turns) |
|--|--|--|
| 01_linear_path.txt    | 4 | 4 |
| 02_simple_fork.txt    | 4 | 6 |
| 03_basic_capacity.txt | 4 | 4 |
| 01_dead_end_trap.txt      | 5 | 8 |
| 02_circular_loop.txt      | 5 | 9 |
| 03_priority_puzzle.txt    | 7 | 13 |
| 01_maze_nightmare.txt         | . | . |
| 02_capacity_hell.txt          | . | . |
| 03_ultimate_challenge.txt     | . | . |
| 01_the_impossible_dream.txt   | . | . |


---
## Instructions

...

---
## Resources

#### Guides

- [Introduction to Graphs in Python](https://www.geeksforgeeks.org/python/introduction-to-graphs-in-python/)
- [Breadth First Search for a Graph in Python](https://www.geeksforgeeks.org/python/python-program-for-breadth-first-search-or-bfs-for-a-graph/)

#### Documentation

- [Dijkstra's_algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm/)
- [uv documentation](https://docs.astral.sh/uv/)

#### Projects

- [Fly-in by megyant](https://github.com/megyant/42_Fly-in)

#### IA

The AI chatbot Claude was used to resolve incedental problems and unexpected results. No code was provided.





# TODO

- map >7 pathfindings
- Restricted zones (2 turn edge)
- Change between paths
- Fill Readme
- (OPTIONAL) gui
