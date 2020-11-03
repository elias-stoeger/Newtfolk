import pygame
from Player import *
from Enemy import *
from World import *
from NPC import *
from PIL import Image
import threading


# A thread for some image processing
class Thread(threading.Thread):
    def __init__(self, n, x, y):
        threading.Thread.__init__(self)
        self.n = n
        self.x = x
        self.y = y

    def run(self):
        minor_back(self.n, self.x, self.y)


# initialize game
pygame.init()

# create screen
W, H = 1920, 1080
HW, HH = W / 2, H / 2
screen = pygame.display.set_mode((W, H))

# FPS
FPS = pygame.time.Clock()

# Title and Icon
pygame.display.set_caption("Newtfolk")
icon = pygame.image.load("Pictures/Icon.png")
pygame.display.set_icon(icon)


# create and initialize world
world = World()
world.build_world()


# used in the making of the background
class Map:
    def __init__(self):
        self.background = [[], [], []]
        self.backcheck = []
        self.out = None
        self.bX = -560  # -560
        self.bY = -990  # -990
        self.monster_chance = 1
        self.backup = None
        self.make_backup()
        self.busy = False
        self.generated = False

    def make_backup(self):
        self.backup = pygame.image.load("temp/back.png")


# I'll let you figure that one out yourself
GMap = Map()


# some prepared squares to have a little less lag when loading the world further
grass = Image.open(f"Pictures/grass.png")
rocky = Image.open(f"Pictures/rocky.png")
red = Image.open(f"Pictures/red.png")
terrains = {"grass": grass, "rocky": rocky, "red": red}


# Create the background each frame
def back(x, y):
    directX = 0
    directY = 0
    n = 0
    if GMap.bX <= -1060 and not GMap.busy:
        n += world.right()
        directX = 1000
        GMap.backcheck = False
    if GMap.bX >= -40 and not GMap.busy:
        n += world.left()
        directX = -1000
        GMap.backcheck = False
    if GMap.bY <= -1845 and not GMap.busy:
        n += world.down()
        directY = 1000
        GMap.backcheck = False
    if GMap.bY >= -155 and not GMap.busy:
        n += world.up()
        directY = -1000
        GMap.backcheck = False
    if GMap.background != GMap.backcheck and not GMap.busy:     # GMap.background == [[], [], []] or
        GMap.busy = True
        background = Thread(n, directX, directY)
        background.start()
    if GMap.out:
        screen.blit(GMap.out, (x, y))
    else:
        screen.blit(GMap.backup, (x, y))


# that part is threaded, it creates and loads the new 3x3 picture
def minor_back(n, x, y):
    counter = 0
    GMap.background = [[], [], []]
    for i in world.active:
        for sq in i:
            GMap.background[counter].append(terrains[sq.type])
        counter += 1
    GMap.backcheck = GMap.background
    picture = Image.new('RGB', (3000, 3000))
    counter = 0
    for row in GMap.background:
        counter2 = 0
        for pic in row:
            picture.paste(pic, (counter * 1000, counter2 * 1000))
            counter2 += 1
        counter += 1
    picture.save("temp/back.png")
    GMap.out = pygame.image.load("temp/back.png")
    GMap.bX += x
    GMap.bY += y
    GMap.make_backup()
    GMap.monster_chance += n
    spawn = npcs.spawn(GMap.monster_chance, GMap.bX + randint(-350, 350) + 960, GMap.bY + randint(-350, 350) + 540, choice(kinds))
    if spawn:
        GMap.monster_chance = 0
    GMap.busy = False
    if not GMap.generated:
        GMap.generated = True


# Player
PlayerX = 370
PlayerY = 250
PlayerX_c = 0
PlayerY_c = 0
Player_h = 136  # actually 116 but it's for putting enemies behind the player and that number works ¯\_(ツ)_/¯


# NPCs
class NPCs:
    def __init__(self):
        self.NPCs = []

    def spawn(self, chance, x, y, kind):
        roll = randint(0, 10)
        if chance >= roll:
            new = NPC(x, y, kind)
            self.NPCs.append(new)
            if new.kind == "Newt":
                new.walking = [pink_walking, pink_walking_left]
                new.idle = [pink_idle, pink_idle_left]
            elif new.kind == "Fish":
                new.walking = [fish_walking, fish_walking_left]
                new.idle = [fish_idle, fish_idle_left]
            return True


npcs = NPCs()


# Sprite class
class sprite:
    def __init__(self, filename, cols, rows):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows
        self.rect = self.sheet.get_rect()
        w = self.cellWidth = self.rect.width / cols
        h = self.cellHeight = self.rect.height / rows
        hw, hh = self.cellCenter = (w / 2, h / 2)
        self.cells = list([(i % cols * w, int(i / cols) * h, w, h) for i in range(self.totalCellCount)])
        self.handle = list([
            (0, 0), (-hw, 0), (-w, 0),
            (0, -hh), (-hw, -hh), (-w, -hh),
            (0, -h), (-hw, -h), (-w, -h)
        ])

    def draw(self, surface, cellindex, x, y, handle=0):
        surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[cellindex])


# Sprites for Newt (The Player)
s = sprite("Pictures/Idle_ws.png", 5, 1)
s_l = sprite("Pictures/Idle_ws_left.png", 5, 1)
walking = sprite("Pictures/walking_ws.png", 9, 1)
walking_l = sprite("Pictures/walking_left_ws.png", 9, 1)
moving = False
right = True

# Sprites for NPCs and Enemies
fish_idle = sprite("Pictures/Fish_smooth_idle.png", 5, 1)
fish_idle_left = sprite("Pictures/Fish_smooth_idle_left.png", 5, 1)
fish_walking = sprite("Pictures/fish_smooth_walking.png", 6, 1)
fish_walking_left = sprite("Pictures/fish_smooth_walking_left.png", 6, 1)

# Pink Newt Sprites
pink_idle = sprite("Pictures/Idle_pink.png", 5, 1)
pink_idle_left = sprite("Pictures/Idle_pink_left.png", 5, 1)
pink_walking = sprite("Pictures/walking_pink.png", 9, 1)
pink_walking_left = sprite("Pictures/walking_left_pink.png", 9, 1)

# May be used later
Player = "The Player Class I'm going to make"
selected = Player

# tester = NPC(800, 500, "Fish")
# tester.walking = [fish_walking, fish_walking_left]
# tester.idle = [fish_idle, fish_idle_left]
# npcs.NPCs.append(tester)


# Game Loop
CENTER_HANDLE = 4
index = 0
frameManager = 0
running = True
while running:

    # Move the background around depending on what buttons you press
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                PlayerX_c = 1
                right = False
            if event.key == pygame.K_d:
                PlayerX_c = -1
                right = True
            if event.key == pygame.K_w:
                PlayerY_c = 1
            if event.key == pygame.K_s:
                PlayerY_c = -1
            if event.key == pygame.K_LSHIFT:
                PlayerX_c = PlayerX_c * 2
                PlayerY_c = PlayerY_c * 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                PlayerX_c = 0
            if event.key == pygame.K_s or event.key == pygame.K_w:
                PlayerY_c = 0
            if event.key == pygame.K_LSHIFT:
                if PlayerY_c == 2 or PlayerY_c == -2:
                    PlayerY_c = PlayerY_c / 2
                if PlayerX_c == 2 or PlayerX_c == -2:
                    PlayerX_c = PlayerX_c / 2
        if PlayerX_c == 0 and PlayerY_c == 0:
            moving = False
        else:
            if not moving:
                moving = True
                index = 0

    # draw the background
    back(GMap.bX, GMap.bY)

    # draw NPCs in front of the player
    def monster_draw():
        if not creature.moving and creature.proxi and creature.right:
            creature.idle[0].draw(screen, index % creature.idle[0].totalCellCount, creature.X, creature.Y, CENTER_HANDLE)
        elif creature.moving and creature.proxi and creature.right:
            creature.walking[0].draw(screen, index % creature.walking[0].totalCellCount, creature.X, creature.Y, CENTER_HANDLE)
        elif not creature.moving and creature.proxi and not creature.right:
            creature.idle[1].draw(screen, index % creature.idle[0].totalCellCount, creature.X, creature.Y, CENTER_HANDLE)
        elif creature.moving and creature.proxi and not creature.right:
            creature.walking[1].draw(screen, index % creature.walking[0].totalCellCount, creature.X, creature.Y, CENTER_HANDLE)

    for creature in npcs.NPCs:
        if creature.thinker // 200 == 1:
            creature.think()
            creature.thinker = 0
        if creature.Y < 540 and creature.kind == "Newt":
            monster_draw()
        elif creature.Y < 555 and creature.kind == "Fish":
            monster_draw()
        creature.thinker += 1

    # draw Player
    if right and not moving:
        s.draw(screen, index % s.totalCellCount, HW, HH, CENTER_HANDLE)
    elif not right and not moving:
        s_l.draw(screen, index % s_l.totalCellCount, HW, HH, CENTER_HANDLE)
    elif right and moving:
        walking.draw(screen, index % walking.totalCellCount, HW, HH, CENTER_HANDLE)
    else:
        walking_l.draw(screen, index % walking.totalCellCount, HW, HH, CENTER_HANDLE)
    frameManager += 1
    if frameManager // 10 != 0:
        index += 1
        frameManager = 0

    # draw NPCs behind the Player
    for creature in npcs.NPCs:
        if creature.Y >= 540 and creature.kind == "Newt":
            monster_draw()
        elif creature.Y >= 555 and creature.kind == "Fish":
            monster_draw()

    # Apply movement done that frame
    GMap.bX += PlayerX_c
    GMap.bY += PlayerY_c
    for creature in npcs.NPCs:
        creature.X += PlayerX_c + creature.mov_X
        creature.Y += PlayerY_c + creature.mov_Y
        if creature.X <= 0 or creature.X >= 1920 or creature.Y <= -50 or creature.Y >= 1080:
            creature.proxi = False
        else:
            creature.proxi = True

    if not GMap.generated:
        screen.fill((0, 0, 0))
        screen.blit(pygame.image.load("Pictures/generating.png"), (820, 550))

    # update display and set frame rate
    pygame.display.update()
    FPS.tick(60)
