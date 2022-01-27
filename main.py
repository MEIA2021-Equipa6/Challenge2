from signal import valid_signals
from dijkstra import Dijkstra
from astar import astar
from colorama import init
from termcolor import colored



def main():
    #        0  1  2  3  4  5  6  7  8  9
    maze = [[0, 0, 0, 1, 1, 0, 0, 0, 0, 0],   # 0
            [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],   # 1
            [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],   # 2
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],   # 3
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],   # 4
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # 5
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 0],   # 6
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],   # 7
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],   # 8
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]   # 9

    start = (0, 0)
    end = (9, 9)
    init()
    path = astar(maze, start, end)

    dijkstra = Dijkstra()
    dijkstra.exec(maze=maze, start=start, end=end, visual=True)

    path = djikstra_shortest(maze, start, end)

    path = ["A1", "B1", "C1"]
    
    # Djikstra - Initialization of variables
    len_maze = len(maze)*len(maze[0])
    g = Graph(len_maze)
    g.fill_edges_using_matrix(maze=maze)

    # Djikstra - Initialization of variables
    g.dijkstra(start, end)




    # Print the solution
    g.dijkstra(0)


if __name__ == '__main__':
    main()
