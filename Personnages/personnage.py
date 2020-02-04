import pygame
successes, failures = pygame.init() # Initialisation des modules de pygame
print("{0} successes and {1} failures".format(successes, failures))
from Objets.objets import *

# Définition de couleurs constantes en RVB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Dimensions de l'écran
SCREEN_WIDTH = 1024
SCREEN_HEIGTH = 728

class Player(pygame.sprite.Sprite): # Création d'une classe pour maintenir les objets plus organisés
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32)) # Taille de la surface contenant l'objet
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # crée un rectangle de la taille de l'image
        self.change_x = 0
        self.change_y = 0
        self.pointdevie = 3
        self.etat = "sain"

    def update(self):
        #déplacement droite/gauche
        self.rect.x += self.change_x

        #detection de collisions
        block_hit_list = pygame.sprite.spritecollide(self, active_sprite_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        #déplacement haut bas
        self.rect.y += self.change_y

        # detection de collisions
        block_hit_list = pygame.sprite.spritecollide(self, active_sprite_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.top = block.rect.bottom

    #mouvement vers la gauche
    def go_left(self):
        self.change_x = -self.Vitesse()

    #mouvement vers la droite
    def go_right(self):
        self.change_x = self.Vitesse()

    #mouvement vers le haut
    def go_up(self):
        self.change_y = -self.Vitesse()

    #mouvement vers le bas
    def go_down(self):
        self.change_y = self.Vitesse()

    #arret mouvement droite/gauche
    def stop_x(self):
        self.change_x = 0

    #arret mouvement haut/bas
    def stop_y(self):
        self.change_y = 0

    #changement de l'état de santé suite a une piqûre
    def Empoisonnement(self):
        timer = pygame.time.Clock.get_time()
        while pygame.time.Clock.get_time() <= timer+10:
            if self.pointdevie == 3:
                self.etat = "empoisonné"
            elif self.pointdevie == 2:
                self.etat = "gravement empoisonné"
            else :
                self.etat = "mort"
        self.etat = 'sain'

    #changement de l'état de santé suite au ramassage d'une caisse de soin
    def Guerison(self):
        self.etat = "sain"

    #il subit une piqûre
    def EstPique(self):
        self.Empoisonnement()
        self.pointdevie -= 1

    #retourne le nombre de points de vie
    def PointDeVie(self):
        return self.pointdevie

    #retourne l'état de santé
    def Etat(self):
        return self.etat

    #def Image(self):
        #return self.image

    #vitesse en fonction de l'état de santé
    def Vitesse(self):
        if self.etat == "sain":
            return 4
        elif self.etat == "empoisonné":
            return 2
        else :
            return 1

    #retourne True si le héro est mort
    def EstMort(self):
        return self.etat == "mort"


#classe des murs invisibles
class Wall(pygame.sprite.Sprite):
    #murs invisibles
    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width,height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()


# Définition de la résolution de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))

#changement du nom de la fenetre
pygame.display.set_caption("Air bee 'n bees")

# Création d'une horloge pour vérifier que les programmes sont mis à jour à une vitesse fixe
clock = pygame.time.Clock()

# Frames per second.
FPS = 60

#création du joueur
player = Player()

#placement du joueur
player.rect.x = SCREEN_HEIGTH/2
player.rect.y = SCREEN_WIDTH/2

#variable de la boucle du jeu
running = True

#création d'un bloc
wall = Wall(100,100)
wall.rect.x = 200
wall.rect.y = 300

wall2 = Wall(5,150)
wall2.rect.x = 0
wall2.rect.y = 0

#liste de sprites (murs)
active_sprite_list = pygame.sprite.Group()
active_sprite_list.add(wall)
active_sprite_list.add(wall2)

#boucle du jeu
while running:
    dt = clock.tick(FPS) / 1000  # Returns milliseconds between each call to 'tick'. The convert time to seconds. Détermine la vitesse du perso
    screen.fill(BLACK)  # Fill the screen with background color

    for event in pygame.event.get(): # Boucle gérant les évènements entrés par l'utilisateur (ex : déplacer la souris, appuyer sur une touche...)
        if event.type == pygame.QUIT: # Si l'évènement est de fermer la fenêtre, alors la fenêtre se ferme
            running = False
        elif event.type == pygame.KEYDOWN: # Si l'évènement est d'appuyer sur une touche du clavier, alors le rectangle (notre objet) bouge en fonction
            if event.key == pygame.K_z:
                player.go_up()
            elif event.key == pygame.K_s:
                player.go_down()
            elif event.key == pygame.K_q:
                player.go_left()
            elif event.key == pygame.K_d:
                player.go_right()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_z or event.key == pygame.K_s:
                player.stop_y()
            elif event.key == pygame.K_q or event.key == pygame.K_d:
                player.stop_x()

    #mise a jour du joueur
    player.update()

    #détection sortie horizontale
    if player.rect.right > SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH
    elif player.rect.left < 0:
        player.rect.left = 0

    #détection sortie verticale
    if player.rect.y + 32 > SCREEN_HEIGTH:
        player.rect.y = SCREEN_HEIGTH - 32
    elif player.rect.y < 0:
        player.rect.y = 0


    screen.blit(player.image, player.rect) # L'ordinateur dessine l'écran
    screen.blit(wall.image, wall.rect)
    screen.blit(wall2.image, wall2.rect)
    pygame.display.update()  # Or pygame.display.flip(), l'ordinateur met à jour l'écran pour l'utilisateur

print("Exited the game loop. Game will quit...")
quit()  # Not actually necessary since the script will exit anyway.