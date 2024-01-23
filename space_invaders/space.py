import pygame

pygame.init()

#define fps
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invanders')

#define colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

#load image
bg = pygame.image.load("img/bg.png")

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
    
    def update(self):
        speed = 8
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed
            
        # shoot bullets
        if key[pygame.K_SPACE]:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            
        #draw health bar
        pygame.draw.rect(screen, red, [self.rect.x, (self.rect.bottom + 10), self.rect.width, 15])
        if self.health_remaining > 0:
            remaining_health_fraction = self.health_remaining / self.health_start
            remaining_width = int(self.rect.width * remaining_health_fraction)
            pygame.draw.rect(screen, green, [self.rect.x, (self.rect.bottom + 10), remaining_width, 15])

# create bullet class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

# sprite group
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


#create player
spaceship = Spaceship(screen_width//2, screen_height - 100, 3)
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
    
    #update sprite groups
    bullet_group.update()
    
    # draw sprite group
    spaceship_group.draw(screen)
    bullet_group.draw(screen)

    #update display window
    pygame.display.update()
    
pygame.quit()