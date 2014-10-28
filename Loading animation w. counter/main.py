import pygame
import random
from pygame.locals import *
pygame.init()

screenResolution = (640, 480)
screen = pygame.display.set_mode(screenResolution, 0, 32)
background = pygame.Surface(screenResolution)
background.fill((255, 255, 255))

font_normal = pygame.font.Font("CaviarDreams.ttf", 18)


def loadSlicedsprites(width, height, filename):
    images = []
    master_image = pygame.image.load(filename).convert_alpha()

    master_width, master_height = master_image.get_size()
    for n in range(int(master_width/width)):
        images.append(master_image.subsurface((n*width, 0, width, height)))
    return images


def repeatSprite(list, new_width):  # width in pixels
    list_return = []

    height = list[0].get_height()
    width = list[0].get_width()
    span = new_width/width

    if not span % width == 0:
        span += 1

    for img in list:
        surface = pygame.Surface((new_width, height))
        for n in range(span):
            surface.blit(img, (n*width, 0))

        list_return.append(surface)

    return list_return


class animation(object):
    def __init__(self, x, y, width, height, filename, interval, loop, alpha):
        self.x = x
        self.y = y
        self.images = loadSlicedsprites(width, height, filename)
        self.images = repeatSprite(self.images, 170)
        self.interval = interval
        self.loop = loop  # True/False
        self.currentIndex = 0
        self.timeCount = 0

        # Set alpha
        for img in self.images:
            img.set_alpha(alpha)

    def Draw(self):
        self.timeCount += time_passed

        if self.timeCount > self.interval:
            self.timeCount = 0
            self.currentIndex += 1
            if self.currentIndex > len(self.images)-1:  # when calling the len() function, it does not count the '0'.
                if self.loop:
                    self.currentIndex = 0
                else:
                    self.currentIndex -= 1

        screen.blit(self.images[self.currentIndex], (self.x, self.y))


class Progress_Bar(object):
    def __init__(self, x, y, width, aniWidth, aniHeight, alpha_animation, interval):
        self.x = x
        self.y = y
        self.width = width
        self.animation_width = aniWidth
        self.animation_height = aniHeight

        self.animation = animation(self.x, self.y, self.animation_width, self.animation_height,
                                   "bar.png", interval, True, alpha_animation)
        self.bar_frame = pygame.image.load("frame.png").convert_alpha()
        self.invisible = pygame.Surface((self.width, aniHeight))
        self.invisible.fill((255, 255, 255))
        self.invisible.set_colorkey((0, 0, 0))

        self.coefficient = self.width/100.

    def Draw(self):
        pct = pctGen.pct
        pct *= self.coefficient
        for x in range(int(pct)):
            for y in range(self.animation_height):
                self.invisible.set_at((x, y), (0, 0, 0))

        screen.blit(self.bar_frame, (self.x-5, self.y-5))
        self.animation.Draw()
        screen.blit(self.invisible, (self.x, self.y))

LEFT = 0x00
UP   = 0x01
IDLE = 0x02


class flowDisplay(object):
    class Text(object):
        def __init__(self, x, y, label, state, font):
            self.font = font
            self.src_x = x
            self.src_y = y
            self.x = x
            self.y = y
            self.state = state
            self.label = str(int(label))
            self.surface = self.font.render(self.label, 1, (0, 0, 0), (255, 255, 255))
            self.width = self.surface.get_width()

            self.x -= self.width

            self.up_speed = .10
            self.left_speed = .175
            self.alpha_speed = .75

            if state == LEFT:
                self.x += self.surface.get_width()*1.25
                self.alpha = 0
            if state == IDLE:
                self.alpha = 255

        def Run(self):
            if self.state == UP:
                self.y -= time_passed*self.up_speed
                self.alpha -= time_passed*self.alpha_speed

            if self.state == LEFT:
                if self.alpha < 255:
                    self.alpha += time_passed*self.alpha_speed

                if self.x > self.src_x - self.width:
                    self.x -= time_passed*self.left_speed

                if self.x <= self.src_x - self.width and self.alpha >= 255:
                    self.state = IDLE

    def __init__(self, x, y, font):
        self.font = font
        self.x = x
        self.y = y
        self.timeInterval = 750
        self.timeCurrent = 0
        self.list = []
        self.list.append(self.Text(self.x, self.y, pctGen.pct, IDLE, self.font))
        self.surfacePct = self.font.render("%", 1, (0, 0, 0))
        self.updateToggle = True

    def State(self):
        self.timeCurrent += time_passed

        if self.timeCurrent > self.timeInterval and self.updateToggle:
            self.timeCurrent = 0

            # time passed. Shift state
            for obj in self.list:
                if obj.state == IDLE:
                    obj.state = UP
                    self.list.append(self.Text(self.x, self.y, pctGen.pct, LEFT, self.font))

            if pctGen.pct == 100:
                self.updateToggle = False

    def Draw(self):
        self.State()

        for obj in self.list:
            obj.surface.set_alpha(obj.alpha)
            obj.Run()

            if obj.alpha < 0 and obj.state == UP:
                self.list.remove(obj)

        for obj in self.list:
            screen.blit(obj.surface, (obj.x, obj.y))

        screen.blit(self.surfacePct, (self.x, self.y))


class percentGenerator(object):
    def __init__(self):
        self.pct = 0.

    def Run(self):
        if self.pct >= 100.:
            self.pct = 100.
        else:
            self.pct += random.random()*time_passed/100.

pctGen = percentGenerator()
bar = Progress_Bar(230, 270, 170, 20, 20, 127, 25)
flowDisplayPercent = flowDisplay(320, 240, font_normal)

clock = pygame.time.Clock()
while True:
    time_passed = clock.tick()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    pctGen.Run()

    screen.blit(background, (0, 0))
    flowDisplayPercent.Draw()
    bar.Draw()

    pygame.display.flip()
