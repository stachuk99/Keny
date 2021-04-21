

class move:
    def __init__(self, piece, destination, captured):
        self.piece = piece
        self.destination = destination
        self.captured = captured

    def __eq__(self, other):
        if self.piece == other.piece:
            if self.destination == other.destination:
                return True
        else:
            return False

    def __repr__(self):
        return str(self.piece) + "-> " +str(self.destination) + str(self.captured)

