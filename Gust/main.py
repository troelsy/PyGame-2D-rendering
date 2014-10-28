# -*- coding: utf-8 -*-

__author__ = "Troels Ynddal"
__version__ = "1.0"
__copyright__ = "Copyright (c) 2012 Troels Ynddal"
__license__ = "LGPL"

#//////////////////////////////////////////////////////////////////////////////////
#///This program is free software: you can redistribute it and/or modify        ///
#///it under the terms of the GNU Lesser General Public License as published by ///
#///the Free Software Foundation, version 3 of the License.                     ///
#///                                                                            ///
#///This program is distributed in the hope that it will be useful,             ///
#///but WITHOUT ANY WARRANTY; without even the implied warranty of              ///
#///MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               ///
#///GNU Lesser General Public License for more details.                         ///
#///                                                                            ///
#///You should have received a copy of the GNU Lesser General Public License    ///
#///along with this program.  If not, see <http://www.gnu.org/licenses/>.       ///
#//////////////////////////////////////////////////////////////////////////////////

import pygame
import random
from pygame.locals import *
pygame.init()

screenResolution = (640,480)
screen = pygame.display.set_mode(screenResolution,0,32)
background = pygame.Surface(screenResolution)
background.fill((255,255,255))

font_normal = pygame.font.Font("CaviarDreams.ttf",36)


class textGust(object):
    def __init__(self,x,y,start,end,font,label, in_s, stay_s, out_s, in_a, out_a):
        self.src_x = x
        self.src_y = y
        self.x = x + end + start # self.x will be the starting point
        self.x_in   = x + end + start/2 # stop intro at this point
        self.x_out  = x + end + start/4 # start outro at this point
        self.x_stop = x + end
        self.y = y

        self.alpha = 0
        self.in_alpha = in_a
        self.out_alpha = out_a

        self.in_speed = in_s
        self.stay_speed = stay_s
        self.out_speed= out_s
        
        self.label = label
        self.surface = font.render(self.label,1,(0,0,0),(255,255,255))

    def Draw(self):
        self.surface.set_alpha(self.alpha)

        if self.x_in < self.x:                          # State: Intro
            self.x -= time_passed * self.in_speed
            if self.alpha <= 255:
                self.alpha += time_passed * self.in_alpha
            else:
                self.alpha = 255
            
        if self.x_in > self.x and self.x_out < self.x:  # State: Stay
            self.x -= time_passed * self.stay_speed
            
        if self.x_out > self.x and self.x_stop < self.x:# State: Outro
            self.x -= time_passed * self.out_speed
            self.alpha -= time_passed * self.out_alpha

        if self.x < self.x_stop:
            pass # delete
            
        screen.blit(self.surface, (self.x,self.y))

txt = textGust(200,200,200,0,font_normal,"text", 0.30, 0.05, 0.65, 1.25, 3.5)

clock = pygame.time.Clock()
while True:
    time_passed = clock.tick()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    screen.blit(background,(0,0))

    txt.Draw()
    
    pygame.display.flip()

