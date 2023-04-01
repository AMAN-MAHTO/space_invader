import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.current_time = 0
        self.last_fire_time = 0
        self.player_speed = 3
        player_ship = pygame.image.load("assets/pixel_ship_yellow.png")
        self.image = player_ship
        self.rect = self.image.get_rect(midbottom = (screen_weidth//2,screen_height))
        
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.player_speed
        if keys[pygame.K_s] and self.rect.bottom < screen_height:
            self.rect.y += self.player_speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.player_speed
        if keys[pygame.K_d] and self.rect.right < screen_weidth:
            self.rect.x += self.player_speed
    
    def fire(self):
        keys = pygame.key.get_pressed()
        print(self.current_time,self.last_fire_time)
        if keys[pygame.K_SPACE] and self.current_time - self.last_fire_time > 200:
            bullet.add(Bullet(player,(self.rect.center)))
            self.last_fire_time = pygame.time.get_ticks()
            

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.move()
        self.fire()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,type,axis):
        super().__init__()
        yellow_bullet = pygame.image.load("assets/pixel_laser_yellow.png")
        self.image = yellow_bullet
        self.rect = self.image.get_rect(center = axis)
    
    def move(self):
        self.rect.y -= 4

    def delete(self):
        if self.rect.bottom < 0:
            self.kill()

    def update(self):
        self.move()
        self.delete()

#constant
screen_weidth = 550
screen_height = 820

#game init
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_weidth,screen_height))

#group
player = pygame.sprite.GroupSingle()
player.add(Player())

bullet = pygame.sprite.Group()

enemy = pygame.sprite.Group()


#baground
bg_surf = pygame.image.load("assets/background-black.png")
bg_surf = pygame.transform.scale(bg_surf,(screen_weidth,screen_height))
bg_rect  = bg_surf.get_rect(topleft = (0,0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
            pygame.quit()
            exit()

    #background
    screen.blit(bg_surf,bg_rect)        

    player.draw(screen)
    player.update()

    bullet.draw(screen)
    bullet.update()

    
    pygame.display.update()
    clock.tick(60)