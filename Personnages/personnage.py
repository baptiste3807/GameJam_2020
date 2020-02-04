import pygame
successes, failures = pygame.init() # Initialisation des modules de pygame
print("{0} successes and {1} failures".format(successes, failures))


screen = pygame.display.set_mode((1024, 768)) # Définition de la résolution de l'écran
clock = pygame.time.Clock() # Création d'une horloge pour vérifier que les programmes sont mis à jour à une vitesse fixe
FPS = 60  # Frames per second.

BLACK = (0, 0, 0) # Couleur en RVB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite): # Création d'une classe pour maintenir les objets plus organisés
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32)) # Taille de la surface contenant l'objet
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.velocity = [0, 0]

    def update(self):
        self.rect.move_ip(*self.velocity)

player = Player()

running = True
while running:
    dt = clock.tick(FPS) / 1000  # Returns milliseconds between each call to 'tick'. The convert time to seconds. Détermine la vitesse du perso
    screen.fill(BLACK)  # Fill the screen with background color

    for event in pygame.event.get(): # Boucle gérant les évènements entrés par l'utilisateur (ex : déplacer la souris, appuyer sur une touche...)
        if event.type == pygame.QUIT: # Si l'évènement est de fermer la fenêtre, alors la fenêtre se ferme
            running = False
        elif event.type == pygame.KEYDOWN: # Si l'évènement est d'appuyer sur une touche du clavier, alors le rectangle (notre objet) bouge en fonction
            if player.rect.x > 0 and player.rect.y >0 or player.rect.x > 0 and player.rect.y < 728 or player.rect.x < 1024 and player.rect.y > 0 or player.rect.x < 1024 and player.rect.y < 728 :
                if event.key == pygame.K_z:
                    player.velocity[1] = -200 * dt  # Modification de la valeur afin que le rectangle bouge (en Y)
                    player.image.fill(RED)
                elif event.key == pygame.K_s:
                    player.velocity[1] = 200 * dt
                    player.image.fill(BLUE)
                elif event.key == pygame.K_q:
                    player.velocity[0] = -200 * dt
                    player.image.fill(GREEN)
                elif event.key == pygame.K_d:
                    player.velocity[0] = 200 * dt
                    player.image.fill(WHITE)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_z or event.key == pygame.K_s:
                player.velocity[1] = 0
            elif event.key == pygame.K_q or event.key == pygame.K_d:
                player.velocity[0] = 0

    player.update()

    screen.blit(player.image, player.rect) # L'ordinateur dessine l'écran
    pygame.display.update()  # Or pygame.display.flip(), l'ordinateur met à jour l'écran pour l'utilisateur

print("Exited the game loop. Game will quit...")
quit()  # Not actually necessary since the script will exit anyway.