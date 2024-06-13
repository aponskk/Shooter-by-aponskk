
from pygame import *
from random import randint


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))

display.set_caption("Shoter eshkere")
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()

font1 = font.SysFont("Arial", 70)
font2 = font.SysFont("Arial", 36)
win = font1.render('ТЫ ВЫИГРАЛ', True, (255, 215, 0))
lose = font1.render('ТЫ ПРОИГРАЛ', True, (255, 215, 0))
minus_life = font2.render("МИНУС 1 ЖИЗНЬ", True, (255, 0, 0))


class Game_Sprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, height, width):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (height, width))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    

class Player(Game_Sprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, -15, 20, 15)
        bullets.add(bullet)

class Bullet(Game_Sprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    



lost = 0
score = 0
max_lost = 5




class Enemy(Game_Sprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

text_lose = font2.render("Пропущено:" + str(lost), 1, (255,255,255))



player = Player('rocket.png', 5, win_height - 100, 20, 80, 100)

monsters = sprite.Group()

for i in range(5):
    monster = Enemy("ufo.png", randint(0, 620), -50 , randint(1,  2), 80, 50)
    monsters.add(monster)

asteroids = sprite.Group()

for b in range(3):
    asteroid = Enemy("asteroid.png", randint(0, 620), - 50, randint(1, 2), 80, 50)
    asteroids.add(asteroid)   

FPS = 60
clock = time.Clock()
bullets = sprite.Group()

life = 3

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
        


    if not finish:
        window.blit(background,(0,0))
        sprite_list = sprite.groupcollide(bullets, monsters, True, True)

        for c in sprite_list:
            score += 1
            monster = Enemy("ufo.png", randint(0, 620), -50 , randint(1, 2), 80, 50)
            monsters.add(monster)

        if lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, asteroids, True):
            life -= 1
            window.blit(minus_life, (200, 200))

        if life <= 0:
            finish = True
            window.blit(lose, (200,200))
        
        if score >= 10:
            finish = True
            window.blit(win, (200, 200))

        
        text = font2.render("Счет:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_life = font2.render("Жизни:" + str(life), 1, (255, 255, 255))
        window.blit(text_life, (590, 10))
        player.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        player.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        display.update()
    time.delay(50)