import pygame

# Initializing pygame
pygame.init()

# Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = pygame.Rect((300, 250, 50, 50))

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), player)

    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        player.move_ip(-1, 0) # Move left (x coord)
    elif key[pygame.K_d]:
        player.move_ip(1, 0) # Move right (x coord)
    elif key[pygame.K_w]:
        player.move_ip(0, -1)
    elif key[pygame.K_s]:
        player.move_ip(0, 1)
    for event in pygame.event.get():        # Game handler
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

pygame.quit()

