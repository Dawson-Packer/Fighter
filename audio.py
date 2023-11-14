import pygame as pygame
import random as random

pygame.mixer.init()

def punch():
    punch_sound = pygame.mixer.Sound("assets/sounds/punch_" + str(random.randint(0, 3)) + ".wav")
    pygame.mixer.Sound.play(punch_sound)

def kick():
    kick_sound = pygame.mixer.Sound("assets/sounds/kick.wav")
    pygame.mixer.Sound.play(kick_sound)

def nero_meow():
    meow_sound = pygame.mixer.Sound("assets/sounds/nero_meow.wav")
    pygame.mixer.Sound.play(meow_sound)

def miss():
    pass

def walk():
    pass