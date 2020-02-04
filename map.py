import pygame
successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

screen = pygame.display.set_mode((720, 480))  # a modifier en fonction de la taille de la map
clock = pygame.time.Clock()
FPS = 60

