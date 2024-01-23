import pygame

# Initialize the modules in pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
    screen.fill(BLACK)
    # Some example shapes
    pygame.draw.rect(screen, WHITE, [50, 50, 20, 20])
    pygame.draw.line(screen, WHITE, [100, 100], [150, 150], 5)
    pygame.draw.circle(screen, WHITE, [60, 250], 40)

    pygame.display.update()