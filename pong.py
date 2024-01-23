import pygame

# Initialize the modules in pygame
pygame.init()

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

# Game exit flag
done = False

while not done:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Game logic

    # Drawing code
    screen.fill((0, 0, 0))

    pygame.display.update()