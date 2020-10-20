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

        #   1   1   1       n   1   1
        #   2   2   2   ->  n   2   2
        #   3   3   3       n   3   3

        new_fields = 0
        bonus_list = []
        for item in self.active[0]:
            bonus_list.append(item)
        self.active[2], self.active[1] = self.active[1], bonus_list

        for i in range(0, 3):
            found = False
            for square in self.squares:
                if (self.active[0][i].coords[0] - 1, self.active[0][i].coords[1]) == square.coords:
                    self.active[0][i] = square
                    found = True
            if not found:
                new_square = Square((self.active[0][i].coords[0] - 1, self.active[0][i].coords[1]), choice(types))
                self.active[0][i] = new_square
                self.squares.append(new_square)
                new_fields += 1
        return new_fields

    def right(self):

        #   1   1   1       1   1   n
        #   2   2   2   ->  2   2   n
        #   3   3   3       3   3   n

        new_fields = 0
        bonus_list = []
        for item in self.active[2]:
            bonus_list.append(item)
        self.active[0], self.active[1] = self.active[1], bonus_list

        for i in range(0, 3):
            found = False
            for square in self.squares:
                if (self.active[2][i].coords[0] + 1, self.active[2][i].coords[1]) == square.coords:
                    self.active[2][i] = square
                    found = True
            if not found:
                new_square = Square((self.active[2][i].coords[0] + 1, self.active[2][i].coords[1]), choice(types))
                self.active[2][i] = new_square
                self.squares.append(new_square)
                new_fields += 1
        return new_fields

    def up(self):

        #   1   1   1       n   n   n
        #   2   2   2   ->  1   1   1
        #   3   3   3       2   2   2

        new_fields = 0
        found = False
        for col in self.active:
            col[2], col[1] = col[1], col[0]
            for square in self.squares:
                if square.coords == (col[0].coords[0], col[0].coords[1] - 1):
                    col[0] = square
                    found = True
            if not found:
                col[0] = Square((col[0].coords[0], col[0].coords[1] - 1), choice(types))
                self.squares.append(col[0])
                new_fields += 1
        return new_fields

    def down(self):

        #   1   1   1       2   2   2
        #   2   2   2   ->  3   3   3
        #   3   3   3       n   n   n

        new_fields = 0
        found = False
        for col in self.active:
            col[0], col[1] = col[1], col[2]
            for square in self.squares:
                if square.coords == (col[2].coords[0], col[2].coords[1] + 1):
                    col[2] = square
                    found = True
            if not found:
                col[2] = Square((col[2].coords[0], col[2].coords[1] - 1), choice(types))
                self.squares.append(col[2])
                new_fields += 1
        return new_fields


class Square:
    def __init__(self, coords, type):
        self.coords = coords
        self.type = type
        self.objects = []


grass = "Pictures/grass.png"
rocky = "Pictures/rocky.png"
red = "red"
types = ["grass", "rocky"]
