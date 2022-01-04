class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

    def __eq__(self, other):
        return self.position == other.position
