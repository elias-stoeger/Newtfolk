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


class Enemy:
    def __init__(self):
        self.name = choice(Enemies[0])
        self.hp = 10
        self.tier = 1


Enemies = [["a Ratling", "a Snider", "like 12 or 13 ants", "a Dust Golem", "a Sproutling", "3/4 of an adder"],
           ["an Adder", "an Ent", "a brittle Ghule", "25 to 30 ants", "a Fish with legs", "a bubbling pile of goo"],
           ["a Jackalope", "at least a basket of ants", "a DogCat", "a murdering mantis", "a Whispling", "a Treant"],
           ["a Skin fairy", "hundreds of ants", "a Chimera", "a Skunk with 3 butts", "a Shark with legs", "a Reverse Centaur"],
           ["a Bone Fairy", "a hulking Ant Golem", "a rabid Ursine", "a Voidcrawler", "the Left Arm of the Forbidden One", "Steve"]]
