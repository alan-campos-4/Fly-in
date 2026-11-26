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


## Description

...

#### Pathfinding limitations

- **Blocked zones**: nodes marked with this zonetype are excluded from the adjancency list before pathfinding starts, thus preventing them from being used in the algorithm.

- **Priority zones**: nodes marked with this zonetype are checked during pathfinding and assigned as the parent of a node when appropiate.

- **Restricted zones**: nodes marked with this zonetype make the drone travelling towards it wait for a turn, i.e.: it doesn't move to the next node until the drone tries to move again in the following turn. This is achieved with a specific attribute that is set during the first turn and checked at the beginning of the second. Additionally, their presence will make a path less likely to be assigned to a drone.

#### Benchmarks

|   | Map name | Shortest path (nodes) | Best Result (turns) |
|---|---|---|---|
| 0 | 01_linear_path.txt    | 4 | 5 |
| 1 | 02_simple_fork.txt    | 4 | 6 |
| 2 | 03_basic_capacity.txt | 4 | 5 |
| 3 | 01_dead_end_trap.txt      | 5 | 12 |
| 4 | 02_circular_loop.txt      | 5 | 15 |
| 5 | 03_priority_puzzle.txt    | 5 | 12 |
| 6 | 01_maze_nightmare.txt         |  7 | 20 |
| 7 | 02_capacity_hell.txt          |  6 | 27 |
| 8 | 03_ultimate_challenge.txt     | 13 | 40 |
| 9 | 01_the_impossible_dream.txt   | 16 | 115 |


## Instructions

...

## Resources

#### Guides

- [Introduction to Graphs in Python](https://www.geeksforgeeks.org/python/introduction-to-graphs-in-python/)
- [Breadth First Search for a Graph in Python](https://www.geeksforgeeks.org/python/python-program-for-breadth-first-search-or-bfs-for-a-graph/)

#### Documentation

- [uv documentation](https://docs.astral.sh/uv/)
- [Dijkstra's_algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm/)
- [Difference Between List and Tuple in Python](https://www.geeksforgeeks.org/python/python-difference-between-list-and-tuple/)

#### Projects

- [Fly-in by megyant](https://github.com/megyant/42_Fly-in)

#### IA

The AI chatbot Claude was used to resolve incedental problems and unexpected results. No code was provided.





# TODO

- Change between paths
- Fill Readme
- (OPTIONAL) gui
