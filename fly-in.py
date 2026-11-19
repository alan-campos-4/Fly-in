#!/usr/bin/python3

import os
import argparse
import traceback
from src import (
    Graph, ParserError, PathFindingError,
    get_data_from_file, find_paths, find_paths_1, find_paths_2,
    travel
)


def arguments() -> argparse.Namespace:
    """Parse the arguments received through the command line.

        map_file:   the index for a map file.
        pathfinder: the index for the algorithm used for pathfinding.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--map_file", default=-1)
    return parser.parse_args()


def menu(map_file: int) -> str | None:
    """Return the selected map file. If not received by parameter,
    display all possibles files in the output.

    Returns:
        the name of the selected file, or None.
    """
    options: dict[int, str] = {
        0: "easy/01_linear_path.txt",
        1: "easy/02_simple_fork.txt",
        2: "easy/03_basic_capacity.txt",
        3: "medium/01_dead_end_trap.txt",
        4: "medium/02_circular_loop.txt",
        5: "medium/03_priority_puzzle.txt",
        6: "hard/01_maze_nightmare.txt",
        7: "hard/02_capacity_hell.txt",
        8: "hard/03_ultimate_challenge.txt",
        9: "challenger/01_the_impossible_dream.txt",
        10: "test.txt"
    }
    try:
        if map_file != -1:
            opt: int = int(map_file)
        else:
            for key, name in options.items():
                print(f" {key} - {name}")
            opt_str: str = input("Select an option: ")
            opt: int = int(opt_str)
    except ValueError:
        print("Invalid input.")
    else:
        if opt in options:
            cwd = os.getcwd()
            return (cwd + "/maps/" + options[opt])
        else:
            print("Option not available.")
    return None


def main() -> None:
    args = arguments()
    filename = menu(args.map_file)
    print()
    if not filename:
        print("No file was selected.")
        exit(1)
    try:
        g: Graph = get_data_from_file(filename)
        find_paths(g)
        print(f"\nPath: {path}")
        # travel(g, path)
        g.visualize()
    except OSError as e:
        msg = str(e).split(':')[0].split(']')[1].strip()
        print(f"An error occured with the file '{filename}': {msg}.")
    except ParserError as e:
        print(e.get_message())
    except PathFindingError as e:
        print(f"An error occured during path finding: {e.message}")
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    except Exception:
        print("An unknown error occured.")
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
