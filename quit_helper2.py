"""
Sofya Pugach (sp2535)
Darian Nwankwo (don4)
Lab Assignment 1
February 20, 2019
"""
import RPi.GPIO as GPIO

import subprocess
import sys
import time
import pygame

pygame.init()


PATH_TO_FIFO = "/home/pi/Development/guidance/log_fifo"
EXIT_POS=(300,220)

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...
NOT_PRESSED = True

def execute(action, path_to_fifo):
    """Sends the action to the fifo at <path_to_fifo>."""
    cmd = 'echo "{}" > {}'.format(action, path_to_fifo)
    subprocess.check_output(cmd, shell=True)


def quit(channel):
    print("Here...")
    global NOT_PRESSED
    NOT_PRESSED = False
    
def inside_quit(tl, br, x, y):
    return tl[0] <= x and x<=br[0] and tl[1] <= y and y<= br[1]

def check_screen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type is MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            tl=(EXIT_POS[0]-80, EXIT_POS[1]-20)
            br=(320,240)
            return not inside_quit(tl, br, x,y)
    return True
                    
if __name__ == "__main__":

    

    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(27, GPIO.FALLING, callback=quit)
    running = True
    while running and NOT_PRESSED:
        time.sleep(0.02)
        running = check_screen()
    GPIO.cleanup()
    execute("Quit", PATH_TO_FIFO)
