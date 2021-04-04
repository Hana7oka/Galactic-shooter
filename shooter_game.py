#Создай со
# 
# бственный Шутер!

from pygame import *
from random import randint

class Game_sprite(sprite.Sprite):
    def __init__(self, imagename , x,y, speed, x_size, y_size):
        super().__init__()
        self.image = transform.scale(image.load(imagename),(x_size,y_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed     
        
class Enemy(Game_sprite):
    def __init__(self):
        super().__init__('ufo.png', randint(0,600),-20,randint(1,4),65,80)
    def update(self):
        self.rect.y += randint(1,4)
        if self.rect.y > 500:
            self.rect.y = -100
            self.rect.x = randint(0,600)
            global lost
            lost += 1
        screen.blit(self.image,(self.rect.x,self.rect.y))
        
class Player(Game_sprite):
    def __init__(self):
        super().__init__('rocket.png', 330,435,10,65,80)
    def update(self, keypressed):
        if keypressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
        if keypressed[K_LEFT] and self.rect.x >0:
            self.rect.x -= self.speed
        screen.blit(self.image,self.rect)
    def fire(self):
        bullet = Bullet(self.rect.centerx - 4,self.rect.y)
        bullets.add(bullet)
class Bullet(Game_sprite):
    def __init__(self,x,y):
        super().__init__('bullet.png',x,y,-5,10,20)
    def update(self):
        self.rect.y += self.speed
        screen.blit(self.image,self.rect)
        if self.rect.y <= -20:
            self.kill()
screen = display.set_mode((700,500))
background = transform.scale(image.load('galaxy.jpg'),(700,500))
clock = time.Clock()
FPS = 60
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    enemy = Enemy()
    monsters.add(enemy)

player = Player()
finish = False
kill = 0
lost = 0
font.init()
f = font.Font(None, 30)
c = font.Font(None,30)
d = font.Font(None,30)
b = font.Font(None,30)
text_win = ('YOU WIN',1,(255,255,0))
text_lose = ('YOU LOSE',1,(255,0,0))
mixer.init()
mixer.music.load('fire.ogg')


game = True
while game:
    keypressed = key.get_pressed()
    clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                finish = True
                kill = 0
                lost = 0
                for m in monsters:
                    m.rect.y = -30  
                for b in bullets:
                    b.kill()
                player.rect.x = 330
                player.rect.y = 435   
                finish = False 
    if not finish:
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            kill+= 1
            monster = Enemy()
            monsters.add(monster)
        screen.blit(background,(0,0))
        bullets.update()
        player.update(keypressed)
        monsters.update()

        text_lose =  f.render('Пропущено:'+ str(lost), 1, (255,255,255))
        text_win= f.render('Уничтожено:'+ str(kill),1,(255,255,255))
        text_pop = f.render('YOU WIN',1,(255,255,0))
        text_lop = f.render('YOU LOSE',1,(255,0,0))
        podscazka = f.render('press escape to restart',1,(255,255,255))
        screen.blit(text_lose,(10,20))
        screen.blit(text_win,(10,50))
        if sprite.spritecollide(player,monsters,False) or lost >= 20:
            finish = True
            screen.fill((0,0,0))
            screen.blit(text_lop,(300,200))
            screen.blit(podscazka,(250,300))
        if kill >= 20:
            finish = True
            screen.fill((0,255,0))
            screen.blit(text_pop,(300,200))
            screen.blit(podscazka,(250,300))
    display.update()