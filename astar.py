from node import Node


class AStarNode(Node):

    def __init__(self, parent=None, position=None):
        super().__init__(parent, position)

        # g -> a node's distance to starting node
        self.g = 0

        # h (heuristic) -> a node's distance to end node
        self.h = 0

        # f = g + h
        self.f = 0

    def calculate_f(self):
        self.f = self.g + self.h


def astar(maze, start_pos, end_pos):
    start_node = Node(None, start_pos)
    end_node = Node(None, end_pos)

    open_list = [start_node]
    closed_list = []

    while len(open_list) > 0:
        current_node = open_list.pop(0)

    # todo
