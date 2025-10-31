# Shortest Paths and Minimum Spanning Trees algorithm implementations
In this project three graphs algorithms are being implemented:
    
    Prim's algorithm for the minimum spanning tree

    Floyd-Warshall algorithm for shortest paths on directed graphs

    Bellman-Ford algorithm for shortest paths from a single source to all others


## How to run
Ideally, the tool uv should be used to run this project, so the python libraries can be easily synchronized.
To sync the libraries execute ``uv sync`` in the root of the project.

To run any of the algorithms, using prim's algorithm as an example, simply run ``uv run python3 ./src/prim.py {path to the .dot file}`` from the root of the project. The other algorithms are ran the same way.

In case uv is not being used, this project needs the pydot library installed 


## Output of the program

Prim's algorithm will output a .dot file with the minimum spanning tree of the given graph.

The other algorithms with have a simple command line output with the shortest paths
