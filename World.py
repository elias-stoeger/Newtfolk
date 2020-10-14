from random import choice


class World:
    def __init__(self):
        self.squares = []
        self.current = None
        self.active = [[], [], []]
        # 460, 10

    def build_world(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                self.active[i + 1].append(Square((i, j), choice(types)))
        self.current = self.active[1][1]
        for list in self.active:
            for square in list:
                self.squares.append(square)

    def speak(self):
        for square in self.squares:
            print(square.coords, square.type)

    def left(self):

        #   1   2   3       n   1   2
        #   1   2   3   ->  n   1   2
        #   1   2   3       n   1   2

        for row in self.active:
            coords = row[0].coords
            row[2], row[1] = row[1], row[0]
            for square in self.squares:
                if square.coords == row[0].coords[0] - 1:
                    row[0] = square
                else:
                    row[0] = Square((coords[0] - 1, coords[1]), choice(types))
                    self.squares.append(row[0])

    def right(self):

        #   1   2   3       2   3   n
        #   1   2   3   ->  2   3   n
        #   1   2   3       2   3   n

        for row in self.active:
            coords = row[0].coords
            row[0], row[1] = row[1], row[2]
            for square in self.squares:
                if square.coords == row[2].coords[0] + 1:
                    row[2] = square
                else:
                    row[2] = Square((coords[0] + 1, coords[1]), choice(types))
                    self.squares.append(row[2])

    def up(self):
        print(self)

    def down(self):
        print(self)


class Square:
    def __init__(self, coords, type):
        self.coords = coords
        self.type = type
        self.objects = []


grass = "Pictures/grass.png"
rocky = "Pictures/rocky.png"
types = ["grass", "rocky"]
