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

#classe du joueur
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
        self.direction = "droite"
        self.liste_souffle = pygame.sprite.Group()
        self.inventaire = []
        self.main_droite = pygame.sprite.Group()
        self.nbMiel = 0
        self.objet_souffle = pygame.sprite.Group()

    def update(self):
        #déplacement droite/gauche
        self.rect.x += self.change_x

        #detection de collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.level.wall_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        #déplacement haut bas
        self.rect.y += self.change_y

        # detection de collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.level.wall_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

        #ramassage objets
        object_hit_list = pygame.sprite.spritecollide(self, self.level.props_list, False)
        for block in object_hit_list:
            if self.change_x > 0 or self.change_x < 0 or self.change_y > 0 or self.change_y < 0:
                if len(self.inventaire) < 1 or block.nom == "miel" or block.nom == "soin":
                    self.Ramasse(block)
                    self.contenu()
                    block.rect.x = 10000
                    block.rect.y = 10000


    #mouvement vers la gauche
    def go_left(self):
        self.change_x = -self.Vitesse()
        self.direction = "gauche"

    #mouvement vers la droite
    def go_right(self):
        self.change_x = self.Vitesse()
        self.direction = "droite"

    #mouvement vers le haut
    def go_up(self):
        self.change_y = -self.Vitesse()
        self.direction = "haut"

    #mouvement vers le bas
    def go_down(self):
        self.change_y = self.Vitesse()
        self.direction = "bas"

    #arret mouvement droite/gauche
    def stop_x(self):
        self.change_x = 0

    #arret mouvement haut/bas
    def stop_y(self):
        self.change_y = 0

    # utilisation de l'air
    def souffle(self):
        self.liste_souffle.add_internal(Souffle(self))

    def obj1(self):
        if len(self.inventaire) > 0:
            if self.inventaire[0].nom == "ventilateur":
                self.main_droite.add_internal(Ventilateur(self))
                if self.inventaire[0].nb_util > 1:
                    self.inventaire[0].nb_util -= 1
                else :
                    del self.inventaire[0]
            elif self.inventaire[0].nom == "cahier":
                self.main_droite.add_internal(Cahier(self))
                if self.inventaire[0].nb_util > 1:
                    self.inventaire[0].nb_util -= 1
                else :
                    del self.inventaire[0]
            elif self.inventaire[0].nom == "eventail":
                self.main_droite.add_internal(Eventail(self))
                if self.inventaire[0].nb_util > 1:
                    self.inventaire[0].nb_util -= 1
                else :
                    del self.inventaire[0]

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

    #permet de ramasser un objet passé en paramètres
    def Ramasse(self, object):
        if object.nom == "miel":
            self.nbMiel += 1;
        elif object.nom == "soin" and self.pointdevie < 3:
            self.pointdevie += 1
        else :
            self.inventaire.insert(0, object)
            if len(self.inventaire) > 2:
                self.inventaire.pop(2)

    #affiche tout ce que l'inventaire du joueur contient
    def contenu(self):
        print("L'inventaire contient : \n")
        for obj in self.inventaire:
            print(obj.nom)
        print("Vous avez ")
        print(self.nbMiel)
        print(" pots de miel")


#classe des murs invisibles
class Wall(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width,height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

#super classe des niveaux
class Level(object):

    def __init__(self, player):

        self.wall_list = pygame.sprite.Group()
        self.props_list = pygame.sprite.Group()
        self.player = player
        self.nbMielNeed = 0

    # Met a jour tous les composants du niveau
    def update(self):

        self.wall_list.update()
        self.props_list.update()

    def draw(self, screen):

        # dessine toutes les listes de sprites
        self.wall_list.draw(screen)
        self.props_list.draw(screen)


class Level_01(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        player.rect.x = 300
        player.rect.y = 300
        self.nbMielNeed = 1

        # liste contenant width, height, x, and y des murs
        level = [[100, 330, 400, 0],
                 [100, 330, 400, 398],
                 [50, 728, 0, 0],
                 [735, 50, 0, 0],
                 [244, 50, 780, 0],
                 [1024, 50, 0, 678],
                 [50, 728, 974, 0],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        ventilo = Ventilateur(player)
        ventilo.rect.x = 600
        ventilo.rect.y = 300

        miel = Miel()
        miel.rect.x = 800
        miel.rect.y = 610

        self.props_list.add_internal(ventilo)
        self.props_list.add_internal(miel)

class Level_02(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        player.rect.x = 300
        player.rect.y = 300
        self.nbMielNeed = 2

        # liste contenant width, height, x, and y des murs
        level = [[100, 330, 400, 0],
                 [100, 330, 400, 398],
                 [50, 728, 100, 0],
                 [735, 50, 0, 0],
                 [244, 50, 780, 0],
                 [1024, 50, 0, 678],
                 [50, 728, 974, 0],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        cahier = Cahier(player)
        cahier.rect.x = 600
        cahier.rect.y = 300

        miel = Miel()
        miel.rect.x = 800
        miel.rect.y = 610

        self.props_list.add_internal(cahier)
        self.props_list.add_internal(miel)

class Level_03(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        player.rect.x = 300
        player.rect.y = 300
        self.nbMielNeed = 3

        # liste contenant width, height, x, and y des murs
        level = [[100, 330, 400, 0],
                 [100, 330, 400, 398],
                 [50, 728, 0, 0],
                 [735, 50, 0, 0],
                 [244, 50, 780, 0],
                 [1024, 50, 0, 678],
                 [50, 728, 974, 0],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        ventilo = Ventilateur(player)
        ventilo.rect.x = 600
        ventilo.rect.y = 300

        miel = Miel()
        miel.rect.x = 800
        miel.rect.y = 610

        self.props_list.add_internal(ventilo)
        self.props_list.add_internal(miel)

class Level_04(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        player.rect.x = 300
        player.rect.y = 300
        self.nbMielNeed = 4

        # liste contenant width, height, x, and y des murs
        level = [[100, 330, 400, 0],
                 [100, 330, 400, 398],
                 [50, 728, 100, 0],
                 [735, 50, 0, 0],
                 [244, 50, 780, 0],
                 [1024, 50, 0, 678],
                 [50, 728, 974, 0],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        ventilo = Ventilateur(player)
        ventilo.rect.x = 600
        ventilo.rect.y = 300

        miel = Miel()
        miel.rect.x = 800
        miel.rect.y = 610

        self.props_list.add_internal(ventilo)
        self.props_list.add_internal(miel)

class Level_05(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        player.rect.x = 300
        player.rect.y = 300
        self.nbMielNeed = 5

        # liste contenant width, height, x, and y des murs
        level = [[100, 330, 400, 0],
                 [100, 330, 400, 398],
                 [50, 728, 0, 0],
                 [735, 50, 0, 0],
                 [244, 50, 780, 0],
                 [1024, 50, 0, 678],
                 [50, 728, 974, 0],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        ventilo = Ventilateur(player)
        ventilo.rect.x = 600
        ventilo.rect.y = 300

        miel = Miel()
        miel.rect.x = 800
        miel.rect.y = 610

        self.props_list.add_internal(ventilo)
        self.props_list.add_internal(miel)

class Level_06(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        player.rect.x = 300
        player.rect.y = 300
        self.nbMielNeed = 6

        # liste contenant width, height, x, and y des murs
        level = [[100, 330, 400, 0],
                 [100, 330, 400, 398],
                 [50, 728, 100, 0],
                 [735, 50, 0, 0],
                 [244, 50, 780, 0],
                 [1024, 50, 0, 678],
                 [50, 728, 974, 0],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        ventilo = Ventilateur(player)
        ventilo.rect.x = 600
        ventilo.rect.y = 300

        miel = Miel()
        miel.rect.x = 800
        miel.rect.y = 610

        self.props_list.add_internal(ventilo)
        self.props_list.add_internal(miel)

class Level_07(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        player.rect.x = 300
        player.rect.y = 300
        self.nbMielNeed = 7

        # liste contenant width, height, x, and y des murs
        level = [[100, 330, 400, 0],
                 [100, 330, 400, 398],
                 [50, 728, 0, 0],
                 [735, 50, 0, 0],
                 [244, 50, 780, 0],
                 [1024, 50, 0, 678],
                 [50, 728, 974, 0],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        ventilo = Ventilateur(player)
        ventilo.rect.x = 600
        ventilo.rect.y = 300

        miel = Miel()
        miel.rect.x = 800
        miel.rect.y = 610

        self.props_list.add_internal(ventilo)
        self.props_list.add_internal(miel)

class Level_08(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        player.rect.x = 300
        player.rect.y = 300
        self.nbMielNeed = 8

        # liste contenant width, height, x, and y des murs
        level = [[100, 330, 400, 0],
                 [100, 330, 400, 398],
                 [50, 728, 100, 0],
                 [735, 50, 0, 0],
                 [244, 50, 780, 0],
                 [1024, 50, 0, 678],
                 [50, 728, 974, 0],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        ventilo = Ventilateur(player)
        ventilo.rect.x = 600
        ventilo.rect.y = 300

        miel = Miel()
        miel.rect.x = 800
        miel.rect.y = 610

        self.props_list.add_internal(ventilo)
        self.props_list.add_internal(miel)

class Level_09(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        player.rect.x = 300
        player.rect.y = 300
        self.nbMielNeed = 9

        # liste contenant width, height, x, and y des murs
        level = [[100, 330, 400, 0],
                 [100, 330, 400, 398],
                 [50, 728, 0, 0],
                 [735, 50, 0, 0],
                 [244, 50, 780, 0],
                 [1024, 50, 0, 678],
                 [50, 728, 974, 0],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        ventilo = Ventilateur(player)
        ventilo.rect.x = 600
        ventilo.rect.y = 300

        miel = Miel()
        miel.rect.x = 800
        miel.rect.y = 610

        self.props_list.add_internal(ventilo)
        self.props_list.add_internal(miel)

class Level_10(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        player.rect.x = 300
        player.rect.y = 300
        self.nbMielNeed = 10

        # liste contenant width, height, x, and y des murs
        level = [[100, 330, 400, 0],
                 [100, 330, 400, 398],
                 [50, 728, 100, 0],
                 [735, 50, 0, 0],
                 [244, 50, 780, 0],
                 [1024, 50, 0, 678],
                 [50, 728, 974, 0],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        ventilo = Ventilateur(player)
        ventilo.rect.x = 600
        ventilo.rect.y = 300

        miel = Miel()
        miel.rect.x = 800
        miel.rect.y = 610

        self.props_list.add_internal(ventilo)
        self.props_list.add_internal(miel)


def main():
    # Définition de la résolution de l'écran
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))

    # Création d'une horloge pour vérifier que les programmes sont mis à jour à une vitesse fixe
    clock = pygame.time.Clock()

    # images par seconde
    FPS = 60

    #création du joueur
    player = Player()

    #Liste des niveaux
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))
    level_list.append(Level_04(player))
    level_list.append(Level_05(player))
    level_list.append(Level_06(player))
    level_list.append(Level_07(player))
    level_list.append(Level_08(player))
    level_list.append(Level_09(player))
    level_list.append(Level_10(player))

    # choisit le niveau en cours
    level_courant = 0
    current_level = level_list[level_courant]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    active_sprite_list.add(player)

    # changement du nom de la fenetre
    pygame.display.set_caption("Air bee 'n bees - Level " + str(level_courant + 1))

    #variable de la boucle du jeu
    running = True

    #boucle du jeu
    while running:
        dt = clock.tick(FPS) / 1000  # Retourne le nombre de millisecondes entre chaque "tick" de l'horloge
        screen.fill(BLACK)  # remplis l'écran avec une couleur de fond
        for souffle in player.liste_souffle:
            souffle.move()
        player.liste_souffle.draw(screen)

        for object in player.main_droite:
            object.move()
        player.main_droite.draw(screen)

        for event in pygame.event.get(): # Boucle gérant les évènements entrés par l'utilisateur (ex : déplacer la souris, appuyer sur une touche...)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN: # Si l'évènement est d'appuyer sur une touche du clavier, alors le rectangle (notre objet) bouge en fonction
                if event.key == pygame.K_UP:
                    player.go_up()
                elif event.key == pygame.K_DOWN:
                    player.go_down()
                elif event.key == pygame.K_LEFT:
                    player.go_left()
                elif event.key == pygame.K_RIGHT:
                    player.go_right()
                elif event.key == pygame.K_k:
                    player.souffle()
                elif event.key == pygame.K_l:
                    player.obj1()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.stop_y()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
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

        #détection fin de niveau
        if player.rect.y == 0 and player.nbMiel == current_level.nbMielNeed:
            level_courant += 1
            current_level = level_list[level_courant]
            player.rect.x = 300
            player.rect.y = 300
            player.level = current_level
            # changement du nom de la fenetre
            pygame.display.set_caption("Air bee 'n bees - Level " + str(level_courant + 1))

        screen.blit(player.image, player.rect)
        current_level.draw(screen)
        pygame.display.update()  #l'ordinateur met à jour l'écran pour l'utilisateur

    print("Exited the game loop. Game will quit...")
    quit()

if __name__ == '__main__':
    main()