class ASTNode:
    def __init__(self, node_type, children=None):
        self.type = node_type
        self.children = children or []

    def is_leaf(self):
        return not self.children
