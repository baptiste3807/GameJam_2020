import pygame

GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class souffle(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([10,10])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.nb_util = 5
        self.nb_cases = 1

class cahier(pygame.sprite.Sprite):
    def __init__(self):
        self.nom = "cahier"
        self.image = pygame.Surface([10,10])
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.nb_util = 3
        self.nb_cases = 2

class eventail(pygame.sprite.Sprite):
    def __init__(self):
        self.nom = "eventail"
        self.image = pygame.Surface([10,10])
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.nb_util = 2
        self.nb_cases = 3

class ventilateur(pygame.sprite.Sprite):
    def __init__(self):
        self.nom = "ventilateur"
        self.image = pygame.Surface((10,10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.nb_util = 1
        self.nb_cases = 4

class Miel(pygame.sprite.Sprite):
    def __init__(self):
        self.nom = "miel"
        self.image = pygame.Surface((10,10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()