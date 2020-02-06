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
        elif object.nom == "soin" and self.pointdevie == 3:
            self.pointdevie = 3
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

        self.nbMielNeed = 1

        player.rect.x = 300
        player.rect.y = 300

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

        cahier = Cahier(player)
        cahier.rect.x = 220
        cahier.rect.y = 100

        miel = Miel()
        miel.rect.x = 550
        miel.rect.y = 180

        self.props_list.add_internal(cahier)
        self.props_list.add_internal(miel)

class Level_02(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        self.nbMielNeed = 2

        # liste contenant width, height, x, and y des murs
        level = [[50, 440, 0, 0],
                 [50, 228, 0, 500],
                 [820, 120, 0, 0],
                 [700, 120, 0, 608],
                 [264, 120, 760, 608],
                 [60, 548, 640, 180],
                 [260, 100, 640, 180],
                 [50, 360, 300, 360],
                 [180, 120, 300, 320],
                 [200, 360, 760, 180],
                 [250, 60, 0, 120],
                 [500, 50, 0, 180],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        eventail = Eventail(player)
        eventail.rect.x = 620
        eventail.rect.y = 470

        miel = Miel()
        miel.rect.x = 870
        miel.rect.y = 60

        self.props_list.add_internal(eventail)
        self.props_list.add_internal(miel)

class Level_03(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        self.nbMielNeed = 3

        # liste contenant width, height, x, and y des murs
        level = [[30, 440, 998, 0],
                 [30, 228, 998, 500],
                 [50, 500, 0, 0],
                 [50, 168, 0, 560],
                 [320, 60, 0, 0],
                 [70, 620, 560, 0],
                 [200, 60, 560, 250],
                 [60, 370, 760, 250],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        miel = Miel()
        miel.rect.x = 400
        miel.rect.y = 40

        self.props_list.add_internal(miel)

class Level_04(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        self.nbMielNeed = 4

        # liste contenant width, height, x, and y des murs
        level = [[482, 50, 0, 0],
                 [482, 50, 542, 0],
                 [724, 478, 150, 125],
                 [1024, 50, 0, 678],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        cahier = Cahier(player)
        cahier.rect.x = 512
        cahier.rect.y = 628

        miel = Miel()
        miel.rect.x = 60
        miel.rect.y = 60

        self.props_list.add_internal(cahier)
        self.props_list.add_internal(miel)

class Level_05(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        self.nbMielNeed = 5

        # liste contenant width, height, x, and y des murs
        level = [[482, 50, 0, 678],
                 [482, 50, 542, 678],
                 [700, 50, 0, 0],
                 [264, 50, 760, 0],
                 [244, 50, 780, 0],
                 [80, 280, 402, 448],
                 [450, 60, 402, 448],
                 [60, 280, 602, 228],
                 [880, 30, 144, 110],
                 [264, 110, 760, 0],
                 [50, 370, 94, 110],
                 [200, 150, 330, 228],
                 [180, 370, 94, 228],
                 [40, 280, 890, 140],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        ventilo = Ventilateur(player)
        ventilo.rect.x = 300
        ventilo.rect.y = 300

        miel = Miel()
        miel.rect.x = 970
        miel.rect.y = 460

        self.props_list.add_internal(ventilo)
        self.props_list.add_internal(miel)

class Level_06(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        self.nbMielNeed = 6

        # liste contenant width, height, x, and y des murs
        level = [[370, 50, 0, 678],
                 [594, 50, 430, 678],
                 [50, 510, 974, 0],
                 [50, 158, 974, 570],
                 [244, 50, 780, 0],
                 [70, 580, 780, 148],
                 [50, 150, 430, 578],
                 [280, 50, 150, 578],
                 [300, 340, 500, 180],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        soin = Soin()
        soin.rect.x = 550
        soin.rect.y = 650

        eventail = Eventail(player)
        eventail.rect.x = 480
        eventail.rect.y = 380

        miel = Miel()
        miel.rect.x = 910
        miel.rect.y = 630

        self.props_list.add_internal(soin)
        self.props_list.add_internal(eventail)
        self.props_list.add_internal(miel)

class Level_07(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        self.nbMielNeed = 7

        # liste contenant width, height, x, and y des murs
        level = [[50, 588, 0, 0],
                 [50, 70, 0, 648],
                 [50, 588, 974, 0],
                 [50, 70, 974, 648],
                 [1024, 80, 0, 0],
                 [1024, 80, 0, 648],
                 [60, 428, 130, 270],
                 [60, 208, 130, 0],
                 [60, 520, 290, 0],
                 [60, 208, 290, 580],
                 [60, 550, 820, 150],
                 [320, 170, 430, 350],
                 [60, 300, 430, 0],
                 [60, 140, 690, 150],
                 [120, 60, 720, 150],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        soin = Soin()
        soin.rect.x = 390
        soin.rect.y = 405

        cahier = Cahier(player)
        cahier.rect.x = 780
        cahier.rect.y = 405

        miel = Miel()
        miel.rect.x = 590
        miel.rect.y = 575

        self.props_list.add_internal(soin)
        self.props_list.add_internal(cahier)
        self.props_list.add_internal(miel)

class Level_08(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        self.nbMielNeed = 8

        # liste contenant width, height, x, and y des murs
        level = [[50, 618, 0, 0],
                 [50, 50, 0, 678],
                 [920, 50, 0, 0],
                 [44, 50, 980, 0],
                 [1024, 50, 0, 678],
                 [50, 728, 974, 0],
                 [50, 324, 315, 0],
                 [50, 324, 315, 404],
                 [50, 324, 655, 0],
                 [50, 324, 655, 404],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        ventilo = Ventilateur(player)
        ventilo.rect.x = 512
        ventilo.rect.y = 100

        ventilo2 = Ventilateur(player)
        ventilo2.rect.x = 512
        ventilo2.rect.y = 628

        miel = Miel()
        miel.rect.x = 950
        miel.rect.y = 650

        self.props_list.add_internal(ventilo)
        self.props_list.add_internal(ventilo2)
        self.props_list.add_internal(miel)

class Level_09(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        self.nbMielNeed = 9

        # liste contenant width, height, x, and y des murs
        level = [[636, 50, 0, 678],
                 [328, 50, 696, 678],
                 [50, 728, 0, 0],
                 [610, 50, 0, 0],
                 [354, 50, 670, 0],
                 [50, 200, 586, 528],
                 [300, 50, 586, 480],
                 [50, 220, 836, 310],
                 [50, 425, 670, 0],
                 [430, 150, 100, 480],
                 [50, 180, 150, 0],
                 [50, 300, 150, 240],
                 [170, 300, 300, 0],
                 [230, 180, 300, 360],
                 [160, 65, 530, 360],
                 [150, 200, 530, 100],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        eventail = Eventail(player)
        eventail.rect.x = 300
        eventail.rect.y = 650

        miel = Miel()
        miel.rect.x = 800
        miel.rect.y = 610

        self.props_list.add_internal(eventail)
        self.props_list.add_internal(miel)

class Level_10(Level):

    def __init__(self, player):

        # Appelle le constructeur du parent
        Level.__init__(self, player)

        self.nbMielNeed = 10

        # liste contenant width, height, x, and y des murs
        level = [[100, 50, 0, 678],
                 [864, 50, 160, 678],
                 [482, 50, 0, 0],
                 [482, 125, 542, 0],
                 [50, 728, 0, 0],
                 [50, 728, 974, 0],
                 [850, 25, 0, 600],
                 [190, 100, 0, 500],
                 [25, 430, 150, 0],
                 [25, 430, 250, 0],
                 [700, 25, 324, 500],
                 [200, 25, 342, 100],
                 [25, 200, 342, 100],
                 [200, 25, 250, 405],
                 [25, 220, 425, 200],
                 [450, 25, 425, 200],
                 ]

        # parcours la liste ci-dessus et ajoute les murs
        for wall in level:
            block = Wall(wall[0], wall[1])
            block.rect.x = wall[2]
            block.rect.y = wall[3]
            block.player = self.player
            self.wall_list.add(block)

        ventilo = Ventilateur(player)
        ventilo.rect.x = 100
        ventilo.rect.y = 80

        miel = Miel()
        miel.rect.x = 505
        miel.rect.y = 60

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
    level_courant = 9
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
        if level_courant == 0:
            if player.rect.y == 0 and player.nbMiel == current_level.nbMielNeed:
                level_courant += 1
                current_level = level_list[level_courant]
                player.rect.x = 710
                player.rect.y = 696
                player.level = current_level
                # changement du nom de la fenetre
                pygame.display.set_caption("Air bee 'n bees - Level " + str(level_courant + 1))
        elif level_courant == 1:
            if player.rect.x == 0 and player.nbMiel == current_level.nbMielNeed:
                level_courant += 1
                current_level = level_list[level_courant]
                player.rect.x = 992
                player.rect.y = 455
                player.level = current_level
                # changement du nom de la fenetre
                pygame.display.set_caption("Air bee 'n bees - Level " + str(level_courant + 1))
        elif level_courant == 2:
            if player.rect.x == 0 and player.nbMiel == current_level.nbMielNeed:
                level_courant += 1
                current_level = level_list[level_courant]
                player.rect.x = 992
                player.rect.y = 348
                player.level = current_level
                # changement du nom de la fenetre
                pygame.display.set_caption("Air bee 'n bees - Level " + str(level_courant + 1))
        elif level_courant == 3:
            if player.rect.y == 0 and player.nbMiel == current_level.nbMielNeed:
                level_courant += 1
                current_level = level_list[level_courant]
                player.rect.x = 498
                player.rect.y = 696
                player.level = current_level
                # changement du nom de la fenetre
                pygame.display.set_caption("Air bee 'n bees - Level " + str(level_courant + 1))
        elif level_courant == 4:
            if player.rect.y == 0 and player.nbMiel == current_level.nbMielNeed:
                level_courant += 1
                current_level = level_list[level_courant]
                player.rect.x = 384
                player.rect.y = 696
                player.level = current_level
                # changement du nom de la fenetre
                pygame.display.set_caption("Air bee 'n bees - Level " + str(level_courant + 1))
        elif level_courant == 5:
            if player.rect.x == 992 and player.nbMiel == current_level.nbMielNeed:
                level_courant += 1
                current_level = level_list[level_courant]
                player.rect.x = 0
                player.rect.y = 602
                player.level = current_level
                # changement du nom de la fenetre
                pygame.display.set_caption("Air bee 'n bees - Level " + str(level_courant + 1))
        elif level_courant == 6:
            if player.rect.x == 992 and player.nbMiel == current_level.nbMielNeed:
                level_courant += 1
                current_level = level_list[level_courant]
                player.rect.x = 0
                player.rect.y = 632
                player.level = current_level
                # changement du nom de la fenetre
                pygame.display.set_caption("Air bee 'n bees - Level " + str(level_courant + 1))
        elif level_courant == 7:
            if player.rect.y == 0 and player.nbMiel == current_level.nbMielNeed:
                level_courant += 1
                current_level = level_list[level_courant]
                player.rect.x = 650
                player.rect.y = 696
                player.level = current_level
                # changement du nom de la fenetre
                pygame.display.set_caption("Air bee 'n bees - Level " + str(level_courant + 1))
        elif level_courant == 8:
            if player.rect.y == 0 and player.nbMiel == current_level.nbMielNeed:
                level_courant += 1
                current_level = level_list[level_courant]
                player.rect.x = 114
                player.rect.y = 696
                player.level = current_level
                # changement du nom de la fenetre
                pygame.display.set_caption("Air bee 'n bees - Level " + str(level_courant + 1))
        #elif level_courant == 9:
            #if player.rect.y == 0 and player.nbMiel == current_level.nbMielNeed:
                # fin du jeu

        screen.blit(player.image, player.rect)
        current_level.draw(screen)
        pygame.display.update()  #l'ordinateur met à jour l'écran pour l'utilisateur

    print("Exited the game loop. Game will quit...")
    quit()

if __name__ == '__main__':
    main()