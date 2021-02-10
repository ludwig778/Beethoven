class NameContainer:
    def __init__(self, names):
        self.names = names
        self.index = 0

    def __repr__(self):
        return self.names[self.index]
