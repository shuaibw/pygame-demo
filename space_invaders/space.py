import pygame
import random

pygame.init()

#define fps
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invanders')

# define game variables
rows = 5
cols = 5
last_alien_shot = pygame.time.get_ticks()

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
        self.last_shot = pygame.time.get_ticks()
    
    def update(self):
        speed = 8
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed
            
        # shoot bullets
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_shot > 500:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now
            
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
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        random_id = str(random.randint(1, 5))
        self.image = pygame.image.load(f"img/alien{random_id}.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.current_direction = 1
        self.move_counter = 0
        
    def update(self):
        self.rect.x += self.current_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.current_direction *= -1
            self.move_counter*= -1
            
# Create alien bullet class
class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
    def update(self):
        self.rect.y += 2
        if self.rect.bottom > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False):
            spaceship.health_remaining -= 1
            self.kill()

# sprite group
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()

#create player
spaceship = Spaceship(screen_width//2, screen_height - 100, 3)
spaceship_group.add(spaceship)

#create aliens
for row in range(rows):
    for col in range(cols):
        alien = Aliens(100 + col * 100, 100 + row * 70)
        alien_group.add(alien)

run = True
while run:

    clock.tick(fps)

    #draw background
    screen.blit(bg, (0,0))

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # create random alien bullets
    current_time = pygame.time.get_ticks()
    aliens_exist = len(alien_group.sprites()) > 0
    num_alien_bullets = len(alien_bullet_group.sprites())
    if current_time - last_alien_shot > 1000 and aliens_exist and num_alien_bullets < 5:
        attacking_alien = random.choice(alien_group.sprites())
        alien_bullet = AlienBullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shot = current_time
    
    # update spaceship
    spaceship_group.update()
    
    #update sprite groups
    bullet_group.update()
    alien_group.update()
    alien_bullet_group.update()
    
    # draw sprite group
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)

    #update display window
    pygame.display.update()
    
pygame.quit()