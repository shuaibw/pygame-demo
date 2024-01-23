import pygame
from pygame import mixer
import random

pygame.init()
mixer.init()

#define fps
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invanders')

#load sounds
explosion_fx = pygame.mixer.Sound("img/explosion.wav")
explosion_fx.set_volume(0.5)

explosion2_fx = pygame.mixer.Sound("img/explosion2.wav")
explosion2_fx.set_volume(0.5)

laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.5)

# define game variables
rows = 5
cols = 5
last_alien_shot = pygame.time.get_ticks()
show_start = True
game_over = 0 # 0 = not over, 1 = win, -1 = loss

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
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now
            
        #draw health bar
        pygame.draw.rect(screen, red, [self.rect.x, (self.rect.bottom + 10), self.rect.width, 15])
        if self.health_remaining > 0:
            remaining_health_fraction = self.health_remaining / self.health_start
            remaining_width = int(self.rect.width * remaining_health_fraction)
            pygame.draw.rect(screen, green, [self.rect.x, (self.rect.bottom + 10), remaining_width, 15])
        elif self.health_remaining <= 0:
            explosion_group.add(Explosion(self.rect.centerx, self.rect.centery, "xl"))
            self.kill()

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
            explosion_fx.play()
            explosion_group.add(Explosion(self.rect.centerx, self.rect.centery, "lg"))

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
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            spaceship.health_remaining -= 1
            self.kill()
            explosion2_fx.play()
            explosion_group.add(Explosion(self.rect.centerx, self.rect.centery, "sm"))

#create explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"img/exp{num}.png")
            if size == "sm":
                img = pygame.transform.scale(img, (20, 20))
            if size == "lg":
                img = pygame.transform.scale(img, (40, 40))
            if size == "xl":
                img = pygame.transform.scale(img, (150, 150))
            self.images.append(img)
            
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
        
    def update(self):
        explosion_speed = 3
        self.counter += 1
        
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

# sprite group
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group() 

#create player
spaceship = Spaceship(screen_width//2, screen_height - 100, 3)
spaceship_group.add(spaceship)

#create aliens
for row in range(rows):
    for col in range(cols):
        alien = Aliens(100 + col * 100, 100 + row * 70)
        alien_group.add(alien)

def draw_text(text, text_col, x, y):
    font = pygame.font.Font(None, 40)
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
run = True
while run:

    clock.tick(fps)
    
    #update display window
    pygame.display.update()
    
    #draw background
    screen.blit(bg, (0,0))

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if show_start and event.key == pygame.K_SPACE:
                show_start = False
                
    if show_start:
        draw_text("SPACE INVADERS", white, 180, screen_height//2 - 100)
        draw_text("Press SPACE to start", white, 160, screen_height//2 + 50)
        continue
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
    explosion_group.update()
    
    # draw sprite group
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)
    
pygame.quit()