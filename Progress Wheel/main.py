# -*- coding: utf-8 -*-

# Idéer
# - Pulse ud af som heartbeat eller bølge
# - Brug vectorer til at skyde ud fra center


import math
import pygame
pygame.init()

screenResolution = (780, 520)
screen = pygame.display.set_mode(screenResolution, 0, 32)
background = pygame.Surface(screenResolution)
background.fill((255, 255, 255))

def quadrant(degrees):
    if 0 <= degrees <= 90:
        return (1., -1.)
    if 90 < degrees <= 180:
        return (-1., -1.)
    if 180 < degrees <= 270:
        return (-1., 1.)
    return (1., 1.)

def foo(degrees):
    if 0 <= degrees <= 90:
        return degrees
    if 90 < degrees <= 180:
        if 180 == degrees:
            return 0
        else:
            return 90 - degrees % 90
    if 180 < degrees <= 270:
        return degrees-180.

    return 90. - degrees % 90

class Dot(object):
    def __init__(self, vec, center, r, func, time=0):
        self.vec = vec
        self.center = center
        self.r = r
        self.surface = pygame.image.load("dot.png").convert_alpha()
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.func = func
        self.time = time

    def tick(self,timePassed, tMax):
        self.time += timePassed

        if self.time > tMax:
            self.time = 0.

    def draw(self):
        centerOffsetX = self.vec[0]*self.r
        centerOffsetY = self.vec[1]*self.r

        funcOffsetX = self.vec[0]*self.func(self.time)
        funcOffsetY = self.vec[1]*self.func(self.time)

        screen.blit(self.surface, (self.center[0]+centerOffsetX+funcOffsetX-self.width/2,
                                   self.center[1]+centerOffsetY+funcOffsetY-self.height/2))

class Circle(object):
    def __init__(self, x, y, r, n, tMax, o, func):
        self.x = x
        self.y = y
        self.radius = r
        self.tMax = tMax

        self.dots = []

        self.n = n

        degrees = 360./self.n
        offset = o/self.n
        for n in range(self.n):
            q1, q2 = quadrant(degrees*n)
            x = q1*math.cos(math.radians(foo(degrees*n)))
            y = q2*math.sin(math.radians(foo(degrees*n)))
            self.dots.append(Dot((x, y), (self.x, self.y), self.radius, func, time=offset*n))

    def tick(self, timePassed):
        for obj in self.dots:
            obj.tick(timePassed, self.tMax)

    def draw(self):
        for obj in self.dots:
            obj.draw()


def groove(time):
        return math.sin(time/400.)*15.

def wave(time):
        if 0 < time/150. < math.pi:
            return math.sin(time/150.)*25.
        else:
            return 0

def star(time):
        return math.sin(time/85.)*15.

def square(time):
    if math.sin(time/80.) > 0:
        return 20.
    else:
        return -20.

def space(time):
    return (2*(time/150. - math.floor(0.5+time/150.)))*15.

def sawtooth(time):
    return (2*(time/350. - math.floor(0.5+time/350.)))*13.

           #Circle   x,  y,  r, n,delay,  max, func
circles = [Circle(130, 130, 75., 24, 2500., 2500., wave),
           Circle(390, 130, 75., 16, 2500., 2500., groove),
           Circle(650, 130, 75., 32, 2500., 2500., space),

           Circle(130, 390, 75., 32, 2500., 2500., star),
           Circle(390, 390, 75., 32, 2500., 2500., square),
           Circle(650, 390, 75., 32, 2500., 2500., sawtooth)
           ]

clock = pygame.time.Clock()
while True:
    timePassed = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))

    for c in circles:
        c.tick(timePassed)
        c.draw()

    pygame.display.flip()





