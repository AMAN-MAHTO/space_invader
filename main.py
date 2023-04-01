import pygame
from sys import exit
from random import randrange,choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global player_speed
        self.current_time = 0
        self.last_fire_time = 0
        self.player_speed = player_speed
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
        
            
    def repostion(self):
        self.rect = self.image.get_rect(midbottom = (screen_weidth//2,screen_height))
    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.move()
        self.fire()

class Bullet_player(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        global player_bullet_speed
        self.player_bullet_speed = player_bullet_speed
        yellow_bullet = pygame.image.load("assets/pixel_laser_yellow.png")
        self.image = yellow_bullet
        self.rect = self.image.get_rect(midbottom = position)
        self.type = "player_bullet"
        
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y -= self.player_bullet_speed
        if self.rect.bottom < 0:
            self.kill()

class Bullet_enemy(pygame.sprite.Sprite):
    def __init__(self,position,color = 'yellow'):
        super().__init__()
        global enemy_bullet_speed
        self.enemy_bullet_speed = enemy_bullet_speed
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
        global life
        self.rect.y += self.enemy_bullet_speed
        #if enemy bullet collide with player, life -1, bullet kill himself
        if pygame.sprite.spritecollide(self,player,False):
            if pygame.sprite.spritecollide(self,player,False,pygame.sprite.collide_mask):
                life -= 1
                self.kill()
                
        
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global enemy_speed
        self.enemy_speed = enemy_speed
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
        global score,life
        #if enemy collide with player bullet, kill himself, player score +10
        if pygame.sprite.spritecollide(self,bullet_player_group,False):
            if pygame.sprite.spritecollide(self,bullet_player_group,True,pygame.sprite.collide_mask):
                score += 10
                self.kill()
        #if enemy collide with player, kill himself, player life -1
        if pygame.sprite.spritecollide(self,player,False):
            if pygame.sprite.spritecollide(self,player,False,pygame.sprite.collide_mask):
                life -= 1
                self.kill()
        
        if self.rect.top > screen_height:
            life -= 1
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


def player_alive():
    global life
    if life< 1:
        enemy_group.empty()
        bullet_enemy_group.empty()
        bullet_player_group.empty()
        return False
        
    else:
        return True
        
#-------#
screen_weidth = 550
screen_height = 850
game_active = True
life = 5
score = 0
current_score = 0
updated_score = 1
level = 0
enemy_spawing_time_constant = 3
enemy_speed = 1
enemy_bullet_speed = 4

player_bullet_speed = 5
player_speed =3


#game init
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_weidth,screen_height))

#font
text_font = pygame.font.Font(None,34)
game_over_text = text_font.render("Press space to start the battle",False,'red')
game_over_rect = game_over_text.get_rect(center = (225,425))


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
pygame.time.set_timer(enemy_spawing_time,enemy_spawing_time_constant*1000)


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
                life = 3
                score =0
                player.sprite.repostion()


    #background
    screen.blit(bg_surf,bg_rect)
    if game_active:
        bullet_enemy_group.draw(screen)
        bullet_enemy_group.update()

        bullet_player_group.draw(screen)
        bullet_player_group.update()

        player.draw(screen)
        player.update() 

        enemy_group.draw(screen)
        enemy_group.update()

        current_score = score
        if score%50 == 0 and score != 0 and current_score != updated_score:
            print("level up")
            enemy_spawing_time_constant -= 0.3
            enemy_speed += 0.5
            enemy_bullet_speed += 0.2

            player_bullet_speed += 0.2
            player_speed += 0.5
            updated_score = score


        score_text = text_font.render(f"Score: {score}",False,'red')
        score_rect = score_text.get_rect(center = (225,20))
        screen.blit(score_text,score_rect)
        life_text = text_font.render(f"life: {life}",False,'red')
        life_rect = life_text.get_rect(center = (50,20))
        screen.blit(life_text,life_rect)
        
        game_active = player_alive()   
        
    else:
        
        screen.blit(game_over_text,game_over_rect)
        screen.blit(life_text,life_rect)
        screen.blit(score_text,score_rect)
        
       
            
    
    pygame.display.update()
    clock.tick(60)