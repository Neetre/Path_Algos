# Path_Algos

## Description

This repository contains the implementation of the most common pathfinding algorithms.
If you don't know what pathfinding algorithms are, they are algorithms that find the shortest path between two points in a graph.
For example, in a maze, the pathfinding algorithm will find the shortest path between the start and end points.
Or in a map, the pathfinding algorithm will find the shortest path between two cities, think about Google Maps.
The algorithms are implemented in Python and visualized using Pygame.

Also, I have implemented a maze generator that generates random mazes using the recursive division algorithm (look [here](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_division_method)).

## Features

- [x] Visualize the pathfinding algorithms
- [x] Change the speed of the visualization
- [x] Generate random mazes
- [x] Change the heuristic
- [x] Toggle diagonal movement
- [x] Clear the grid
- [x] Clear the path
- [x] Clear the barriers
- [x] Clear the weights
- [x] Clear the start and end points
- [x] Change the algorithm
- [x] Change the animation speed

## Commands

### Key Bindings

| Key           | Functionality                          |
|---------------|---------------------------------------|
| Left Click    | Place Start, End, Barriers, or Weights |
| Right Click   | Clear Node                            |
| Space         | Start Algorithm                       |
| C            | Clear Grid                            |
| D            | Toggle Diagonal Movement              |
| H            | Change Heuristic                      |
| S            | Change Animation Speed                |
| R            | Generate Random Maze                  |
| 1            | Select A* Algorithm                   |
| 2            | Select Dijkstra's Algorithm           |
| 3            | Select Greedy Best-First Search       |

In the future, I will add more algorithms and functionalities.

| Key           | Functionality                          |
|---------------|---------------------------------------|
| 4            | Select Breadth First Search           |
| 5            | Select Depth First Search             |

What are 'Heuristics'?

Heuristics are like shortcuts.  They're rules of thumb that help an algorithm make smart guesses about which path to take next.  In the A* search, the heuristic is an estimate of the total cost of a path, combining how far we've already traveled with a guess of how much further it is to the goal.  The algorithm prioritizes exploring the paths that seem closest to the end, based on these estimates.  So, a lower heuristic means the algorithm thinks it's on the right track.

## Algorithms

- [x] Greedy Best-First Search   -> [Greedy Best-First Search](https://en.wikipedia.org/wiki/Best-first_search)
- [x] Dijkstra's Algorithm -> [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [x] A* Algorithm -> [A* Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [X] Depth First Search -> [Depth First Search](https://en.wikipedia.org/wiki/Depth-first_search)
- [X] Breadth First Search -> [Breadth First Search](https://en.wikipedia.org/wiki/Breadth-first_search)

## Requirements

- Python 3.9 or higher

### Python Packages

1. Create a virtual environment

    ```bash
    python -m venv .venv
    ```

2. Activate the virtual environment

    ```bash
    source .venv/bin/activate
    ```

3. Install the required packages

    ```bash
    pip install -r requirements.txt
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

[Neetre](https://github.com/Neetre)