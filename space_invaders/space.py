import pygame

pygame.init()

#define fps
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invanders')


#load image
bg = pygame.image.load("img/bg.png")



run = True
while run:

    clock.tick(fps)

    #draw background
    screen.blit(bg, (0,0))

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display window
    pygame.display.update()
    
pygame.quit()