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
        player_ship = pygame.image.load("assets/pixel_ship_yellow.png").convert_alpha()
        self.image = player_ship
        self.rect = self.image.get_rect(midbottom = (screen_weidth//2,screen_height))
        self.mask = pygame.mask.from_surface(self.image)

        self.fire_sound = pygame.mixer.Sound("sound/pewpew_9.wav")
        self.mouse_down = 0
        self.space_down = 0
    
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
        mouse_input_down = pygame.mouse.get_pressed()
        
        if (mouse_input_down[0] or keys[pygame.K_SPACE]) and self.current_time - self.last_fire_time > 200 and self.mouse_down == False and self.space_down == False :
            bullet_player_group.add(Bullet_player((self.rect.center)))
            self.fire_sound.play()
            self.last_fire_time = pygame.time.get_ticks()
            self.mouse_down = True
        self.mouse_down = mouse_input_down[0]
        self.space_down = keys[pygame.K_SPACE]
        
        
            
    def reposition(self):
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
        yellow_bullet = pygame.image.load("assets/pixel_laser_yellow.png").convert_alpha()
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
        green_bullet = pygame.image.load("assets/pixel_laser_green.png").convert_alpha()
        blue_bullet = pygame.image.load("assets/pixel_laser_blue.png").convert_alpha()
        red_bullet = pygame.image.load("assets/pixel_laser_red.png").convert_alpha()
        
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
        blue_ship = pygame.image.load("assets/pixel_ship_blue_small.png").convert_alpha()
        green_ship = pygame.image.load("assets/pixel_ship_green_small.png").convert_alpha()
        red_ship = pygame.image.load("assets/pixel_ship_red_small.png").convert_alpha()
        
        self.image,self.color = choice([(blue_ship,'blue'),(red_ship,'red'),(green_ship,'green')])
        self.rect = self.image.get_rect(midbottom = (randrange(35,screen_weidth-20,50),0) )
        self.mask = pygame.mask.from_surface(self.image)

        self.enemy_fire_sound = pygame.mixer.Sound("sound/pewpew_2.wav")
        self.enemy_fire_sound.set_volume(0.4)

    
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
            self.enemy_fire_sound.play()
            self.last_fire_time = pygame.time.get_ticks()

    def update(self):
        
        self.current_time = pygame.time.get_ticks()
        self.rect.y += self.enemy_speed
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
text_font = pygame.font.Font("font/game_font.ttf",15)
game_over_text = text_font.render("Press space to start the battle",False,'red')
game_over_rect = game_over_text.get_rect(center = (screen_weidth//2,screen_height//2))


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

                player.sprite.reposition()


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
        if score%10 == 0 and score != 0 and current_score != updated_score:
            
            enemy_spawing_time_constant -= 0.5
            enemy_speed += 0.17
            enemy_bullet_speed += 0.3

            player_bullet_speed += 0.3
            player_speed += 0.17
            updated_score = score


        score_text = text_font.render(f"Score: {score}",False,'red')
        score_rect = score_text.get_rect(center = (225,20))
        screen.blit(score_text,score_rect)
        life_text = text_font.render(f"life: {life}",False,'red')
        life_rect = life_text.get_rect(center = (70,20))
        screen.blit(life_text,life_rect)
        
        game_active = player_alive()   
        
    else:
        
        screen.blit(game_over_text,game_over_rect)
        screen.blit(life_text,life_rect)
        screen.blit(score_text,score_rect)
        
       
            
    
    pygame.display.update()
    clock.tick(60)