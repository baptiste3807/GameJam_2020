import pygame

GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class Souffle(pygame.sprite.Sprite):
    def __init__(self, player):
        self.image = pygame.Surface([10,10])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.nb_util = 5
        self.velocity = 5
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.x_initial = player.rect.x
        self.y_initial = player.rect.y
        self.player = player
        self.direction = player.direction
        if self.direction == "bas":
            self.rect.y = player.rect.y+32
        elif self.direction == "droite":
            self.rect.x = player.rect.x+32

    def remove(self):
        self.player.liste_souffle.remove_internal(self)

    def move(self):
        if self.direction == "bas":
            self.rect.y += self.velocity
        elif self.direction == "haut":
            self.rect.y -= self.velocity
        elif self.direction == "gauche":
            self.rect.x -= self.velocity
        elif self.direction == "droite":
            self.rect.x += self.velocity

        if self.rect.x > 1024 or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > 728:
            self.remove()
        elif self.rect.x-self.x_initial > 80 or self.x_initial-self.rect.x > 80:
            self.remove()
        elif self.rect.y-self.y_initial > 80 or self.y_initial-self.rect.y > 80:
            self.remove()

class Cahier(pygame.sprite.Sprite):
    def __init__(self, player):
        self.nom = "cahier"
        self.image = pygame.Surface([10,10])
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.nb_util = 3
        self.velocity = 5
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.x_initial = player.rect.x
        self.y_initial = player.rect.y
        self.player = player
        self.direction = player.direction

    def remove(self):
        self.player.inventaire.remove_internal(self)

    def move(self):
        if self.direction == "bas":
            self.rect.y += self.velocity
        elif self.direction == "haut":
            self.rect.y -= self.velocity
        elif self.direction == "gauche":
            self.rect.x -= self.velocity
        elif self.direction == "droite":
            self.rect.x += self.velocity

        if self.rect.x > 1024 or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > 728:
            self.remove()
        elif self.rect.x-self.x_initial > 160 or self.x_initial-self.rect.x > 160:
            self.remove()
        elif self.rect.y-self.y_initial > 160 or self.y_initial-self.rect.y > 160:
            self.remove()

class Eventail(pygame.sprite.Sprite):
    def __init__(self, player):
        self.nom = "eventail"
        self.image = pygame.Surface([10,10])
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.nb_util = 2
        self.velocity = 5
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.x_initial = player.rect.x
        self.y_initial = player.rect.y
        self.player = player
        self.direction = player.direction

    def remove(self):
        self.player.inventaire.remove_internal(self)

    def move(self):
        if self.direction == "bas":
            self.rect.y += self.velocity
        elif self.direction == "haut":
            self.rect.y -= self.velocity
        elif self.direction == "gauche":
            self.rect.x -= self.velocity
        elif self.direction == "droite":
            self.rect.x += self.velocity

        if self.rect.x > 1024 or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > 728:
            self.remove()
        elif self.rect.x-self.x_initial > 240 or self.x_initial-self.rect.x > 240:
            self.remove()
        elif self.rect.y-self.y_initial > 240 or self.y_initial-self.rect.y > 240:
            self.remove()

class Ventilateur(pygame.sprite.Sprite):
    def __init__(self, player):
        self.nom = "ventilateur"
        self.image = pygame.Surface((10,10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.nb_util = 1
        self.velocity = 5
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.x_initial = player.rect.x
        self.y_initial = player.rect.y
        self.player = player
        self.direction = player.direction

    def remove(self):
        self.player.inventaire.remove_internal(self)

    def move(self):
        if self.direction == "bas":
            self.rect.y += self.velocity
        elif self.direction == "haut":
            self.rect.y -= self.velocity
        elif self.direction == "gauche":
            self.rect.x -= self.velocity
        elif self.direction == "droite":
            self.rect.x += self.velocity

        if self.rect.x > 1024 or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > 728:
            self.remove()
        elif self.rect.x-self.x_initial > 320 or self.x_initial-self.rect.x > 320:
            self.remove()
        elif self.rect.y-self.y_initial > 320 or self.y_initial-self.rect.y > 320:
            self.remove()

class Miel(pygame.sprite.Sprite):
    def __init__(self):
        self.nom = "0x miel"
        self.image = pygame.Surface((10,10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()