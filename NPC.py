from random import randint, choice


class NPC:
    def __init__(self, x, y, kind):
        self.X = x
        self.Y = y
        self.mov_X = 0
        self.mov_Y = 0
        self.moving = False
        self.Name = False
        self.kind = kind
        self.busy = False
        self.proxi = True
        self.idle = None
        self.walking = None
        self.thinker = 200
        self.right = True

    def move(self):
        self.mov_X = choice([-2, 0, 2])
        self.mov_Y = choice([-2, 0, 2])
        if self.mov_Y != 0 or self.mov_X != 0:
            self.moving = True
            if self.mov_X < 0:
                self.right = False
            elif self.mov_X > 0:
                self.right = True

    def idling(self):
        self.mov_X = 0
        self.mov_Y = 0
        self.moving = False

    # Here, the borders between mind and machine are blurred
    def think(self):
        if not self.busy:
            thought = randint(0, 1)
            if thought == 0:
                self.idling()
            else:
                self.move()
        else:
            self.idling()

    def speak(self):
        self.busy = True
        if self.Name:
            return f"Hi, my name is {self.Name}"
        else:
            return f"I can't remember my name, can you help me? :("


kinds = ["Newt", "Fish"]
