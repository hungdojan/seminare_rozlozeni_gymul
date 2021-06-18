class Zak:

    def __init__(self, index: int, name: str):
        self.index = index
        self.name  = name

    def __str__(self):
        return "{} {}".format(self.index, self.name)

