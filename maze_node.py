import string
from node import Node


class MazeNode(Node):

    def __init__(self, parent=None, position=None):
        super().__init__(parent, position)
        column_names = list(string.ascii_uppercase)
        
            
        #self.node_name = f"{column_names[position[0]]}{position[1]}" if not node_name else node_name
        self.value = position[0]*10 + position[1]*100

        # g -> a node's distance to starting node
        self.g = 0

        # h (heuristic) -> a node's distance to end node
        self.h = 0

        # f = g + h
        self.f = 0

    def calculate_f(self):
        self.f = self.g + self.h


class MazeOperations():
    
    TRAVELING_WEIGHT = 1

    def verify_obstacles(self, maze, node):
        # obstacle
        if maze[node.position[0]][node.position[1]] != 1:
            return True

    def verify_out_of_bounds(self, maze, node):
         # out of bounds
        if node.position[0] >= len(maze[0]) or node.position[0] < 0 \
                or node.position[1] >= len(maze) or node.position[1] < 0:
            return True

    def find_possible_neighbor_nodes(self, current_node):
        possible_neighbor_nodes = []
        for relative_coord in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]:
            neighbor_pos = (current_node.position[0] + relative_coord[0], current_node.position[1] + relative_coord[1])
            neighbor_node = MazeNode(current_node, neighbor_pos)
            possible_neighbor_nodes.append(neighbor_node)

        return possible_neighbor_nodes