class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.type, self.value))