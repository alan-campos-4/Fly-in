#!/usr/bin/python3

import os
import traceback
from src import (
    Graph, ParserException, get_data_from_file,
    read_file, parse_values, find_paths, travel
)


def menu() -> str | None:
    """..."""
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
        9: "challenger/01_the_impossible_dream.txt"
    }
    for key, name in options.items():
        print(f" {key} - {name}")
    opt_str: str = input("Select an option: ")
    try:
        opt: int = int(opt_str)
    except ValueError:
        print("Invalid option")
    else:
        if opt in options:
            project_dir = os.path.dirname(os.path.abspath(__file__))
            return (project_dir + "/maps/" + options[opt])
        else:
            print("Option not available")
    return None


if __name__ == "__main__":
    try:
        filename = menu()
        print()
        if filename:
            data = get_data_from_file(filename)
            print(data)
        else:
            print("No file was selected.")
    except ParserException as e:
        print(f"An error was found in file '{e.file_name}'", end='')
        print(f" at line {e.file_linenum}:")
        print(f"\t{e.message}.")
    else:
        try:
            """if data:
                g: Graph = parse_values(data)
                path = find_paths(g)
                print(f"--- {path} ---")
                travel(g, path)
                g.visualize()"""
        except KeyboardInterrupt:
            print("\nProgram interrupted.")
        except Exception:
            print("An unknown error occured.")
            print(traceback.format_exc())
