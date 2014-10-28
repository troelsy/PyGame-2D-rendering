# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
pygame.init()

screenResolution = (640, 480)
screen = pygame.display.set_mode(screenResolution, 0, 32)
background = pygame.Surface(screenResolution)
background.fill((255, 255, 255))

font_normal = pygame.font.Font("CaviarDreams.ttf", 18)


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
            self.label = str(label)
            self.surface = self.font.render(self.label, 1, (0, 0, 0), (255, 255, 255))
            self.width = self.surface.get_width()
            self.height = self.surface.get_height()

            self.up_speed = .10
            self.left_speed = .175
            self.alpha_speed = .75

            if state == LEFT:
                self.y += self.surface.get_height()*1.25
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

                if self.y > self.src_y:
                    self.y -= time_passed*self.left_speed

                if self.y <= self.src_y and self.alpha >= 255:
                    self.state = IDLE

    def __init__(self, x, y, font):
        self.font = font
        self.x = x
        self.y = y
        self.timeInterval = 2000
        self.timeCurrent = 0
        self.list = []
        self.list.append(self.Text(self.x, self.y, textGen.text,  IDLE, self.font))
        self.updateToggle = True

    def State(self):
        self.timeCurrent += time_passed

        if self.timeCurrent > self.timeInterval and self.updateToggle:
            self.timeCurrent = 0

            # time passed. Shift state
            for obj in self.list:
                if obj.state == IDLE:
                    obj.state = UP

                    textGen.Run()
                    self.list.append(self.Text(self.x, self.y, textGen.text, LEFT, self.font))

    def Draw(self):
        self.State()

        for obj in self.list:
            obj.surface.set_alpha(obj.alpha)
            obj.Run()

            if obj.alpha < 0 and obj.state == UP:
                self.list.remove(obj)

        for n in self.list:
            screen.blit(n.surface, (n.x, n.y))


class textGenerator(object):
    def __init__(self):
        self.list = ["Breaking news breaking 24/7 - All day",
                     "News from all around the world and here",
                     "Are anybody reading this?"]

        self.text = self.list[0]
        self.n = 0

    def Run(self):
        self.n += 1
        if self.n == 3:
            self.n = 0

        self.text = self.list[self.n]


textGen = textGenerator()
flowDisplayPercent = flowDisplay(50, 100, font_normal)

clock = pygame.time.Clock()

while True:
    time_passed = clock.tick()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))

    flowDisplayPercent.Draw()

    pygame.display.flip()
