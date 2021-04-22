

class move:
    def __init__(self, start, destination, captured):
        self.start = start
        self.destination = destination
        self.captured = captured

    def __eq__(self, other):
        if self.start == other.start and self.destination == other.destination:
            return True
        else:
            return False

    def __repr__(self):
        return str(self.start) + "->" +str(self.destination)

