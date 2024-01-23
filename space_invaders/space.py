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

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    
    def update(self):
        speed = 8
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

# sprite group
spaceship_group = pygame.sprite.Group()


#create player
spaceship = Spaceship(screen_width//2, screen_height - 100)
spaceship_group.add(spaceship)
run = True
while run:

    clock.tick(fps)

    #draw background
    screen.blit(bg, (0,0))

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    # update spaceship
    spaceship_group.update()
    
    # draw sprite group
    spaceship_group.draw(screen)

    #update display window
    pygame.display.update()
    
pygame.quit()