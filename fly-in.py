#!/usr/bin/python3

import os
import argparse
import time
import traceback
from src import (
    Graph, ParserError, PathFindingError,
    get_data_from_file, find_paths, travel
)


def arguments() -> argparse.Namespace:
    """Parse the arguments received through the command line.

        map_file:   the index for a map file.
        log:        whether to display the time taken between operations.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--map_file", default=-1)
    parser.add_argument("--log", default=False)
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
    opt: int
    try:
        if map_file != -1:
            opt = int(map_file)
        else:
            for key, name in options.items():
                print(f" {key} - {name}")
            opt_str: str = input("Select an option: ")
            opt = int(opt_str)
    except ValueError:
        print("Invalid input.")
    else:
        if opt in options:
            cwd = os.getcwd()
            return (cwd + "/maps/" + options[opt])
        else:
            print("Option not available.")
    return None


def time_passed(msg: str, prev_time: float) -> float:
    curr_time = time.time()
    print(f"{msg} in {(curr_time - prev_time):.6f} seconds")
    return curr_time


def main() -> None:
    args = arguments()
    filename = menu(args.map_file)
    print()
    if not filename:
        print("No file was selected.")
        exit(1)
    try:
        if args.log:
            curr_time = time.time()
        g: Graph = get_data_from_file(filename)
        if args.log:
            # t_graph = time.time()
            # print(f"Graph created in {(t_graph - t_start):.6f} seconds")
            curr_time = time_passed("Graph created", curr_time)
        paths = find_paths(g)
        if args.log:
            # t_path = time.time()
            # print(f"Path finding done in {(t_path - t_graph):.6f} seconds")
            curr_time = time_passed("Path finding", curr_time)
            print("\nPaths: ")
            for path in paths:
                print(path)
        travel(g, paths)
        if args.log:
            curr_time = time_passed("Movement", curr_time)
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
