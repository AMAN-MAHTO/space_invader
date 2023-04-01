import pygame
from sys import exit
from random import randrange,choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.current_time = 0
        self.last_fire_time = 0
        self.player_speed = 3
        player_ship = pygame.image.load("assets/pixel_ship_yellow.png")
        self.image = player_ship
        self.rect = self.image.get_rect(midbottom = (screen_weidth//2,screen_height))
        self.mask = pygame.mask.from_surface(self.image)
        
    
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
        mouse_input = pygame.mouse.get_pressed(num_buttons=3)
        if (mouse_input[0] or keys[pygame.K_SPACE]) and self.current_time - self.last_fire_time > 200:
            bullet_player_group.add(Bullet_player((self.rect.midtop)))
            self.last_fire_time = pygame.time.get_ticks()
        
            

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.move()
        self.fire()

class Bullet_player(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        yellow_bullet = pygame.image.load("assets/pixel_laser_yellow.png")
        self.image = yellow_bullet
        self.rect = self.image.get_rect(midbottom = position)
        self.type = "player_bullet"
        
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

class Bullet_enemy(pygame.sprite.Sprite):
    def __init__(self,position,color = 'yellow'):
        super().__init__()
        self.enemy_bullet_speed = 4
        green_bullet = pygame.image.load("assets/pixel_laser_green.png")
        blue_bullet = pygame.image.load("assets/pixel_laser_blue.png")
        red_bullet = pygame.image.load("assets/pixel_laser_red.png")
        
        if color =='red':
            self.image = red_bullet
        elif color == "blue":
            self.image =blue_bullet
        else:
            self.image = green_bullet
        self.rect = self.image.get_rect(center = position)
        self.type = "enemy_bullet"
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.rect.y += self.enemy_bullet_speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.enemy_speed = 1
        self.current_time = 0
        self.last_fire_time = 0
        blue_ship = pygame.image.load("assets/pixel_ship_blue_small.png")
        green_ship = pygame.image.load("assets/pixel_ship_green_small.png")
        red_ship = pygame.image.load("assets/pixel_ship_red_small.png")
        
        self.image,self.color = choice([(blue_ship,'blue'),(red_ship,'red'),(green_ship,'green')])
        self.rect = self.image.get_rect(midbottom = (randrange(35,screen_weidth-20,50),0) )
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.y += self.enemy_speed

    def delete(self):
        global score
        if pygame.sprite.spritecollide(self,bullet_player_group,False):
            if pygame.sprite.spritecollide(self,bullet_player_group,True,pygame.sprite.collide_mask):
                score += 10
                self.kill()
        if self.rect.top > screen_height:
            self.kill()

    def fire(self):
        if self.current_time - self.last_fire_time > 3000:
            bullet_enemy_group.add(Bullet_enemy((self.rect.center),color = self.color))
            self.last_fire_time = pygame.time.get_ticks()

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.move()
        self.delete()
        self.fire()


def collision():
    global life
    if pygame.sprite.spritecollide(player.sprite,bullet_enemy_group,False):
        if pygame.sprite.spritecollide(player.sprite,bullet_enemy_group,True,pygame.sprite.collide_mask):
            if life< 1:
                enemy_group.empty()
                bullet_enemy_group.empty()
                bullet_player_group.empty()
                
                return False
            else:
                life -= 1
                return True
        return True
        
    else:
        return True
#-------#
screen_weidth = 550
screen_height = 850
game_active = True
life = 5
score = 0

#game init
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_weidth,screen_height))

#font
text_font = pygame.font.Font(None,34)


#group
player = pygame.sprite.GroupSingle()
player.add(Player())

bullet_enemy_group = pygame.sprite.Group()
bullet_player_group = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()


#baground
bg_surf = pygame.image.load("assets/background-black.png")
bg_surf = pygame.transform.scale(bg_surf,(screen_weidth,screen_height))
bg_rect  = bg_surf.get_rect(topleft = (0,0))

#spawing timer
enemy_spawing_time = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_spawing_time,2000)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
                pygame.quit()
                exit()
        if game_active:
            if event.type == enemy_spawing_time:
                enemy_group.add(Enemy())
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True


    #background
    screen.blit(bg_surf,bg_rect)
    print(life)
          
    if game_active:
        bullet_enemy_group.draw(screen)
        bullet_enemy_group.update()

        bullet_player_group.draw(screen)
        bullet_player_group.update()

        player.draw(screen)
        player.update() 

        enemy_group.draw(screen)
        enemy_group.update()

        score_text = text_font.render(f"Score: {score}",False,'red')
        score_rect = score_text.get_rect(center = (225,20))
        screen.blit(score_text,score_rect)
        life_text = text_font.render(f"life: {life}",False,'red')
        life_rect = life_text.get_rect(center = (50,20))
        screen.blit(life_text,life_rect)
        game_active = collision()
    else:
        screen.blit(score_text,score_rect)
        life_rect = life_text.get_rect(center = (50,20))
        life = 3
        score =0
       
            
    
    pygame.display.update()
    clock.tick(60)