# PathSearching

PathSearching is a visual representation tool for exploring and understanding pathfinding algorithms using the Pygame library. This project is ideal for anyone interested in learning how different algorithms navigate a grid-based environment. Currently, the only implemented algorithm is A*, with plans to add more in the future.

## Features

- **Visual Representation**: Watch as the A* algorithm searches for the optimal path in real-time.
- **Modular Design**: The code is structured to allow for easy addition of new algorithms.

## Future Expansion

- **Dijkstra's Algorithm**: An algorithm that finds the shortest path in a weighted graph.
- **Breadth-First Search (BFS)**: A simple algorithm that explores all possible paths layer by layer.
- **Depth-First Search (DFS)**: A method of exploring paths by diving deep before backtracking.
- **Greedy Best-First Search**: Chooses the path that appears to be closest to the goal.

## Project Structure

```
PathSearching/
│
├── a_star.py             # Implementation of the A* algorithm
├── main.py               # Entry point of the program (currently empty)
└── utils/
    └── vars.py           # Contains global variables and utility functions
```

## Getting Started

### Prerequisites

- Python 3.x (preferably 3.10)
- Pygame (preferably 2.6.0)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/UnStudentRoman/PathSearching.git
    cd PathSearching
    ```
2. Install requirements:
    ```bash
    pip install pygame
    # OR
    pip install -r requirements.txt
    ```

### Running the Project

Currently, the project is still in its early stages. To see the A* algorithm in action, run the `a_star.py` file:

```bash
python a_star.py
