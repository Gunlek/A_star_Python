class Cell:

    # x and y are the cell's positions that can't
    # be changed later
    def __init__(self, x, y):
        self.state = 0
        self.x = x
        self.y = y

    # Return x position of the cell
    def getX(self):
        return self.x

    # Return y position of the cell
    def getY(self):
        return self.y

    # Return current state of the cell
    def getState(self):
        return self.state

    # Update the cell's state according to the new specified one
    def setState(self, state):
        self.state = state