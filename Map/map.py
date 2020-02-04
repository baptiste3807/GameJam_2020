import pygame
successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures".format(successes, failures))

screen = pygame.display.set_mode((750, 597))  # a modifier en fonction de la taille de la map
clock = pygame.time.Clock()
FPS = 60
BLACK = (0,0,0)

image = pygame.image.load("map.png").convert()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    screen.blit(image, (0,0))
    pygame.display.flip()
    pygame.display.update()

print("Exited the game loop. Game will quit...")
quit()


