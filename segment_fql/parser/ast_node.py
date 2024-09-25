class ASTNode:
    def __init__(self, node_type, children=None):
        self.type = node_type
        self.children = children or []

    def __repr__(self):
        if self.children:
            return f'{self.type} ({self.children})'
        return f'{self.type}'

    def is_leaf(self):
        return not self.children
