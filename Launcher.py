import pygame
from Player import *
from Enemy import *
from World import *
from PIL import Image

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


world = World()
world.build_world()


class Map:
    def __init__(self):
        self.background = [[], [], []]
        self.backcheck = []
        self.out = None
        self.bX = -560  # -560
        self.bY = -990  # -990


GMap = Map()


def back(x, y):
    if GMap.bX <= -1060:
        world.right()
        GMap.bX += 1000
        GMap.backcheck = False
        print("went right")
    if GMap.bX >= -40:
        world.left()
        GMap.bX -= 1000
        GMap.backcheck = False
    if GMap.bY <= -1845:
        world.down()
        GMap.bY += 1000
        GMap.backcheck = False
    if GMap.bY >= -155:
        world.up()
        GMap.bY -= 1000
        GMap.backcheck = False
    if GMap.background == [[], [], []] or GMap.background != GMap.backcheck:
        counter = 0
        GMap.background = [[], [], []]
        for i in world.active:
            for sq in i:
                GMap.background[counter].append(Image.open(f"Pictures/{sq.type}.png"))
                GMap.backcheck = GMap.background
            counter += 1
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

    screen.blit(GMap.out, (x, y))


# Player
# PlayerImg = pygame.image.load("Pictures/Player_b.png")
PlayerX = 370
PlayerY = 250
PlayerX_c = 0
PlayerY_c = 0


# def player(x, y):
#     screen.blit(PlayerImg, (x, y))


# 370x116, 5 sprites
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
            (0, -h), (-hw, -h), (-w, -h),
        ])

    def draw(self, surface, cellindex, x, y, handle=0):
        surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[cellindex])


s = sprite("Pictures/Idle_smooth_b.png", 5, 1)
s_l = sprite("Pictures/Idle_smooth_left_b.png", 5, 1)
walking = sprite("Pictures/walking_smooth.png", 9, 1)
walking_l = sprite("Pictures/walking_left_smooth.png", 9, 1)
moving = False
right = True

CENTER_HANDLE = 4
index = 0

Player = "The Player Class I'm going to make"
selected = Player


# Game Loop
frameManager = 0
running = True
while running:

    screen.fill((0, 0, 0))

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
    back(GMap.bX, GMap.bY)
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
        # print(PlayerY_c, ":", PlayerX_c)

    GMap.bX += PlayerX_c
    GMap.bY += PlayerY_c

    # player(PlayerX, PlayerY)
    pygame.display.update()
    FPS.tick(60)
