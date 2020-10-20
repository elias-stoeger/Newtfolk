from random import choice


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
