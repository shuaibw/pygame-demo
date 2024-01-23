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

# Clock to control the screen update speed
clock = pygame.time.Clock()

# Initial position of paddles
paddle1_y = 200
paddle2_y = 200

# initial paddle speed
paddle1_vy = 0
paddle2_vy = 0

# Initial position of ball
ball_x = 350
ball_y = 250

# Initial speed of ball
ball_vx = 6
ball_vy = 6

while not done:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        elif event.type == pygame.KEYDOWN: # key pressed
            # paddle 1
            if event.key == pygame.K_w:
                paddle1_vy = -8
            elif event.key == pygame.K_s:
                paddle1_vy = 8
            # paddle 2
            elif event.key == pygame.K_UP:
                paddle2_vy = -8
            elif event.key == pygame.K_DOWN:
                paddle2_vy = 8
        elif event.type == pygame.KEYUP: # key released
            # paddle 1
            if event.key == pygame.K_w or event.key == pygame.K_s:
                paddle1_vy = 0
            # paddle 2
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                paddle2_vy = 0

    # Game logic
    
    # Paddle movement
    if 0 <= paddle1_y + paddle1_vy <= 400:
        paddle1_y += paddle1_vy
    if 0 <= paddle2_y + paddle2_vy <= 400:
        paddle2_y += paddle2_vy
        
    # Check ball collision against upper and lower walls
    if 10 <= ball_y + ball_vy <= 490:
        ball_y += ball_vy
    else:
        ball_vy *= -1

    # Check ball collision against left and right walls
    if 10 <= ball_x + ball_vx <= 690:
        ball_x += ball_vx
    else:
        ball_vx *= -1

    # Drawing code
    screen.fill(BLACK)
    
    # Draw the paddle
    pygame.draw.rect(screen, WHITE, [0, paddle1_y, 10, 100])
    pygame.draw.rect(screen, WHITE, [690, paddle2_y, 10, 100])
    
    # draw the net
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    
    # draw the ball
    pygame.draw.circle(screen, WHITE, [ball_x, ball_y], 10)

    pygame.display.update()
    clock.tick(60)
    
pygame.quit()