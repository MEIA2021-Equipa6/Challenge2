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

        


'''
It is being assumed that each line in the maze has the same length
'''
def astar(maze, start_pos, end_pos):
    start_node = MazeNode(None, start_pos)
    end_node = MazeNode(None, end_pos)

    mo = MazeOperations()

    open_list = [start_node]
    closed_list = []

    while len(open_list) > 0:
        # step 1: find open node with smallest f number

        open_list.sort(key=lambda x: (x.f, x.h))
        current_node = open_list[0]

        open_list.pop(0)
        closed_list.append(current_node)

        # step 2: if current is end node, build path, return

        if current_node == end_node:
            path = []
            node_in_path = current_node
            while node_in_path is not None:
                path.append(node_in_path.position)
                node_in_path = node_in_path.parent
            return path[::-1]

        # step 3: calculate neighbor nodes

        neighbor_nodes = mo.find_neighbor_nodes(current_node=current_node)
        for neighbor_node in neighbor_nodes:

            # out of bounds
            if mo.verify_out_of_bounds(maze=maze, neighbor_node=neighbor_node):
                continue

            # obstacle
            if mo.verify_obstacles(maze=maze, neighbor_node=neighbor_node):
                continue

            # in closed list
            if neighbor_node in closed_list:
                continue

            # current_node is the parent node
            neighbor_node.g = current_node.g + (
                    abs(neighbor_node.position[0] - current_node.position[0]) ** 2 +
                    abs(neighbor_node.position[1] - current_node.position[1]) ** 2
            )
            new_h = abs(neighbor_node.position[0] - end_node.position[0]) ** 2 + \
                    abs(neighbor_node.position[1] - end_node.position[1]) ** 2

            if neighbor_node in open_list:
                if new_h < neighbor_node.h:
                    neighbor_node.h = new_h
            else:
                open_list.append(neighbor_node)

            neighbor_node.calculate_f()
