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

        old_coords = [self.active[0][0].coords, self.active[0][1].coords, self.active[0][2].coords]
        self.active[2], self.active[1] = self.active[1], self.active[0]
        new_list = []
        for i in range(0, 3):
            new_square = Square((old_coords[i][0] - 1, old_coords[i][1]), choice(types))
            new_list.append(new_square)
            self.squares.append(new_square)
            self.active[0] = new_list

    def right(self):

        #   1   1   1       1   1   n
        #   2   2   2   ->  2   2   n
        #   3   3   3       3   3   n

        print("before")
        counter = 0
        for row in self.active:
            print(f"row {counter} ---------")
            for square in row:
                print(square.coords)
            counter += 1

        old_coords = [self.active[2][0].coords, self.active[2][1].coords, self.active[2][2].coords]
        new_coords = []
        for i in range(0, 3):
            new_coords.append((old_coords[i][0], old_coords[i][1] + 1))
        self.active[0], self.active[1] = self.active[1], self.active[2]

        # one boolean state for each square in self.active[2]
        crawler = [False, False, False]
        # working on it :/
        """counter = 0
        for square in self.active[2]:
            for field in self.squares:
                if (field.coords[0], field.coords[1] + 2) == square.coords:
                    print(square.coords)
                    # crawler[counter] = True
                    self.active[2][counter] = field
            counter += 1"""

        print(crawler)
        test = []
        for i in range(0, 3):
            """if crawler[i]:
                pass
                print("oopsi")
            else:"""
            new_square = Square((old_coords[i][0], old_coords[i][1] + 1), choice(types))
            self.squares.append(new_square)
                # self.active[2][i] = new_square
            test.append(new_square)
        self.active[2] = test

        counter = 0
        print("after")
        for row in self.active:
            print(f"row {counter} ---------")
            for square in row:
                print(square.coords)
            counter += 1

    def up(self):

        #   1   1   1       n   n   n
        #   2   2   2   ->  1   1   1
        #   3   3   3       2   2   2

        found = False
        for row in self.active:
            row[2], row[1] = row[1], row[0]
            for square in self.squares:
                if square.coords[0] == row[0].coords[0] + 1:
                    row[0] = square
                    found = True
            if not found:
                row[0] = Square((row[1].coords[0] + 1, row[1].coords[1]), choice(types))
                self.squares.append(row[0])

    def down(self):

        #   1   1   1       2   2   2
        #   2   2   2   ->  3   3   3
        #   3   3   3       n   n   n

        found = False
        for row in self.active:
            coords = row[0].coords
            row[0], row[1] = row[1], row[2]
            for square in self.squares:
                if square.coords == row[2].coords[0] + 1:
                    row[2] = square
                    found = True
            if not found:
                row[2] = Square((coords[0] + 1, coords[1]), choice(types))
                self.squares.append(row[2])


class Square:
    def __init__(self, coords, type):
        self.coords = coords
        self.type = type
        self.objects = []


grass = "Pictures/grass.png"
rocky = "Pictures/rocky.png"
types = ["grass", "rocky"]
