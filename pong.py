import pygame

# Initialize the modules in pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

# Game flags
done = False
show_start = True

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

# initial score
score1 = 0
score2 = 0
WIN_SCORE = 5
won_by = 0

# define font
font = pygame.font.Font(pygame.font.get_default_font(), 50)

def handleGameLogic():
    global paddle1_y, paddle2_y, ball_x, ball_y, ball_vx, ball_vy, score1, score2, show_start
    # Paddle movement
    if 0 <= paddle1_y + paddle1_vy <= 400:
        paddle1_y += paddle1_vy
    if 0 <= paddle2_y + paddle2_vy <= 400:
        paddle2_y += paddle2_vy
    
    # Update ball position    
    ball_x += ball_vx
    ball_y += ball_vy
    
    # Check for scoring
    if ball_x < 0:
        score2 += 1
        ball_x = 350
        ball_y = 250
        ball_vx = 6
        ball_vy = 6
        show_start = True
    elif ball_x > 700:
        score1 += 1
        ball_x = 350
        ball_y = 250
        ball_vx = -6
        ball_vy = -6
        show_start = True
    
    # Check ball collision against upper and lower walls
    if ball_y < 10 or ball_y > 490:
        ball_vy *= -1

    # Check ball collision against left and right paddles
    if ball_x < 25 and paddle1_y <= ball_y <= paddle1_y + 100:
        ball_vx *= -1
    elif ball_x > 675 and paddle2_y <= ball_y <= paddle2_y + 100:
        ball_vx *= -1

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
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            show_start = False
            won_by = 0

    # Game logic
    if not show_start:
        handleGameLogic()
    if score1 >= WIN_SCORE or score2 >= WIN_SCORE:
        show_start = True
        score1 = 0
        score2 = 0
        won_by = 1 if score1 > score2 else 2

    # Drawing code
    screen.fill(BLACK)
    
    if show_start:
        initial_text = "Press SPACE to start"
        text_x = 100
        if won_by > 0:
            initial_text = f"Player {won_by} won!"
            text_x = 190
        text = font.render(initial_text, 1, WHITE)
        screen.blit(text, (text_x, 200))
    
    # Draw the paddle
    pygame.draw.rect(screen, WHITE, [0, paddle1_y, 10, 100])
    pygame.draw.rect(screen, WHITE, [690, paddle2_y, 10, 100])
    
    # draw the net
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    
    # draw the ball
    pygame.draw.circle(screen, WHITE, [ball_x, ball_y], 10)
    
    # draw the scores
    text1 = font.render(str(score1), 1, WHITE)
    text2 = font.render(str(score2), 1, WHITE)
    screen.blit(text1, (250, 10))
    screen.blit(text2, (420, 10))

    pygame.display.update()
    clock.tick(60)
    
pygame.quit()