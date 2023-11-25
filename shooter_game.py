#Создай собственный Шутер!
from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
   #конструктор класса
   def __init__(self, player_image, player_x, player_y, player_speed, w, h):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (65, 65))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       mw.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    fire_reload = 10
    live = 3
    
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        if keys[K_SPACE]:
            if self.fire_reload <= 0:
                self.fire()
                self.fire_reload = 30

        self.fire_reload -= 1
    
    def fire(self):
        shot = Shot('bullet.png',
                self.rect.x, self.rect.y, 4, 40, 40)
        shots.add(shot)

class Star(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.kill()

class Ufo(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.kill()
            global miss
            miss += 1

class Shot(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -100:
            self.kill()
            
class Boom(sprite.Sprite):
    def __init__(self, ufo_center, boom_sprites, booms) -> None:
        super().__init__() 
        #global booms, boom_sprites              
        self.frames = boom_sprites        
        self.frame_rate = 1   
        self.frame_num = 0
        self.image = boom_sprite[0]
        self.rect = self.image.get_rect()
        self.rect.center = ufo_center
        self.add(booms)
    
    def next_frame(self):
        self.image = self.frames[self.frame_num]
        self.frame_num += 1
        
    
    def update(self):
        self.next_frame()
        if self.frame_num == len(self.frames)-1:
            self.kill()

def create_star():
    star = Star('star.png',
                randint(0, win_width), -10, randint(3, 13), 30, 30)
    stars.add(star)

def create_ufo():
    ufo = Ufo('ufo.png',
                randint(0, win_width), -50, 4, 70, 50)
    ufos.add(ufo)

def sprites_load(folder:str, file_name:str, size:tuple, colorkey:tuple = None):    
    sprites = []
    load = True
    num = 1
    while load:
        try:
            print(num)
            spr = transform.scale(image.load(f'{folder}\\{file_name}{num}.png'),size)
            if colorkey: spr.set_colorkey((0,0,0))
            sprites.append(spr)
            num += 1

        except:
            load = False
    return sprites


shots = sprite.Group()
ufos = sprite.Group()
stars = sprite.Group()
meteors = sprite.Group()
booms = sprite.Group()


mixer.init()
fon_sound = mixer.Sound('fon1.mp3')
fire_sound = mixer.Sound('fire2.mp3')
boom_sound = mixer.Sound('boom1.mp3')
mixer.music.load('fon1.mp3')
fon_sound.set_volume(0.6)
fon_sound.play(-1)

ticks = 0
win_width = 800
win_height = 600
miss = 0


mw = display.set_mode((win_width, win_height))
display.set_caption('Космические рейнджеры')
clock = time.Clock()

fon = transform.scale(image.load('fon1.jpg'), (win_width, win_height))
game_over = transform.scale(image.load('GAME OVER.jpg'), (win_width, win_height))
ship = Player('player.png', win_width/2, win_height-80, 5, 50, 70)
boom_sprite = sprites_load('boom', 'boom', (100,100), (0,0,0))



game = True
finish = False

font.init()
font1 = font.Font(None, 36)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish :
        if ticks % 60 == 0:
            create_ufo()

        if ticks % 10 == 0:
            create_star()

        mw.blit(fon, (0, 0))

        ship.update()
        ship.reset()
        stars.update()
        shots.update()
        ufos.update()
        booms.update()

        collisions = sprite.groupcollide(shots, ufos, True, True)

        for ufo, shot in collisions.items():
            Boom(ufo.rect.center, boom_sprite, booms)
            #sound_boom.play()

        stars.draw(mw)
        shots.draw(mw)
        ufos.draw(mw)
        booms.draw(mw)
        
        mw.blit(
                font1.render('Пропущено:' + str(miss), 1,
                (255,255,255)), (10,10))

        mw.blit(
                font1.render('Жизни:' + str(ship.live), 1,
                (255,255,255)), (400,10))
        if miss >= 3:
            finish = True
    
    else:
        mw.blit(game_over, (0, 0))

    ticks += 1
    display.update()
    clock.tick(60)