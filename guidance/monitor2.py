import RPi.GPIO as GPIO

import os
import pygame
import sys
import threading
import gevent.monkey; gevent.monkey.patch_tread()
import time

from pygame.locals import *

isOnTFT = False

path = "/home/pi/Development/guidance/log_fifo"

if isOnTFT:
    os.putenv("SDL_VIDEODRIVER","fbcon")
    os.putenv("SDL_FBDEV","/dev/fb1")
    os.putenv("SDL_MOUSEDRV","TSLIB")
    os.putenv("SDL_MOUSEDEV","/dev/input/touchscreen")

BLACK = (0 , 0, 0)
WHITE = (255, 255, 255)
EXIT_POS=(300, 220)
CENTER_POS=(160, 120)

#Initialize oygame
pygame.init()
screen = pygame.display.set_mode((320, 240))
pygame.mouse.set_visible(not isOnTFT)

#Set up the quit button
def quit(channel):
    sys.exit()

class Monitor:

    def __init__(self, display):
        self.display = display

      
    def direction(self, L_R):
        self.direction = L_R
        return self


    def distance(self, feet):
        self.distance = feet
        return self
    

    def _add_text(self, text, position, size, color):
        font = pygame.font.Font(None, size)
        text_surf = font.render(text, True, color)
        rect = text_surf.get_rect(center=position)
        return (text_surf, rect)


    def update_screen(self, color=(255,255,255), size=20):
        # Add text and the exit button
        text=["Turning {} in {} feet".format(self.direction, self.distance), "Exit"]

        position=[CENTER_POS,EXIT_POS]
        txt_pos=[(text[0], position[0]),(text[1], position[1])]
        self.display.fill(BLACK)
        
        display_objects=[]
        for txt,pos in txt_pos:
            text_surf,rect = self._add_text(txt, pos, size, color)
            screen.blit(text_surf, rect)
        pygame.display.flip()


    def _inside_quit(self, tl, br, x, y):
        return tl[0] <= x and x<=br[0] and tl[1] <= y and y<= br[1]


    def check_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type is MOUSEBUTTONUP:
                x,y=pygame.mouse.get_pos()
                tl=(EXIT_POS[0]-80,EXIT_POS[1]-20)
                br=(320,240)
                return not self._inside_quit(tl, br, x, y)
        return True


if __name__ == "__main__":
    # Initialize oygame
    pygame.init()
    screen = pygame.display.set_mode((320, 240))
    pygame.mouse.set_visible(not isOnTFT)
    
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(27, GPIO.FALLING, callback=quit)
    
    # Create Monitor instance
    nav = Monitor(screen)
   
    nav.direction("-")
    nav.distance(0)


    nav.update_screen(WHITE,20)

    running = True
    while running:
        running = nav.check_screen()
        with open(path) as fifo:
            myline = fifo.readline()
            print(myline)
            if str(myline.strip()) == "Arrived":
                running = False
                
            else:
                direction = myline[0]
                nav.direction = direction
                nav.distance = float(myline[1])
                nav.update_screen(WHITE,20)
        time.sleep(.02)
    GPIO.cleanup()

