from astar import astar
from colorama import init
from termcolor import colored


def main():
    #        0  1  2  3  4  5  6  7  8  9
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # 0
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # 1
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # 2
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],  # 3
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],  # 4
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],  # 5
            [0, 0, 0, 0, 1, 0, 1, 1, 0, 0],  # 6
            [0, 0, 0, 0, 1, 1, 0, 1, 1, 0],  # 7
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],  # 8
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]  # 9

    start = (0, 0)
    end = (9, 9)
    init()
    path = astar(maze, start, end)

    start1 = (0, 9)
    end1 = (9, 0)
    path1 = astar(maze, start1, end1)

    iteration = 0
    if path:

        for x in path:
            maze[x[0]][x[1]] = 2
        for x1 in path1:
            maze[x1[0]][x1[1]] = 3

        for y in maze:
            for x in y:
                if x == 2:
                    print(colored(str(x), 'green', 'on_red'), end =",")
                elif x == 3:
                    print(colored(str(x), 'red', 'on_green'), end=",")
                else:
                    print(str(x), end =",")
            print('\n')
        iteration += 1
    print(path)
    print(path1)

if __name__ == '__main__':
    main()
