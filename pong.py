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

# Initial position of paddles
paddle1_y = 200
paddle2_y = 200

while not done:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Game logic

    # Drawing code
    screen.fill(BLACK)
    # Draw the paddle
    pygame.draw.rect(screen, WHITE, [0, paddle1_y, 10, 100])
    pygame.draw.rect(screen, WHITE, [690, paddle2_y, 10, 100])

    pygame.display.update()