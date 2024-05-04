#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer #импортируем функцию для засекания времени, чтобы интерпретатор не искал эту функцию в pygame модуле time, даём ей другое название сами

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#шрифты и надписи
font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой
img_enemy = "ufo.png" # враг
img_bullet = "bullet.png" #пуля
img_ast = "asteroid.png" #астероид

score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
max_lost = 10 #проиграли, если пропустили столько
goal = 15 #столько кораблей нужно сбить для победы
life = 3  #очки жизни

#Класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)

       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed

       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):                                   #метод, отрисовывающий героя на окне
       window.blit(self.image, (self.rect.x, self.rect.y))

#Класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
   #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)

#класс спрайта-врага  
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#Создание спрайтов
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
#создание врагов
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
#создание группы пуль
bullets = sprite.Group()
#создание астероидов
asteroids = sprite.Group()
for i in range(1, 3):
   asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
   asteroids.add(asteroid)

finish = False # отвечает за ПРОХОЖДЕНИЕ 

#Игровой цикл
run = True # отвечает за работу ПРИЛОЖЕНИЯ (окно открыто)
rel_time = False #флаг, отвечающий за перезарядку
num_fire = 0  #переменная для подсчёта выстрелов  

while run:
   #событие нажатия на кнопку Закрыть
   for e in event.get():
       if e.type == QUIT:
           run = False
       elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                if num_fire  >= 5 and rel_time == False :
                    last_time = timer()
                    rel_time = True

   if not finish:
       window.blit(background,(0,0))  #обновляем фон
       
       #для спрайтов
       ship.update()                        #производим движения спрайтов
       monsters.update()
       ship.reset()                         #обновляем их в новом местоположении при каждой итерации цикла
       monsters.draw(window)
       bullets.update()
       bullets.draw(window)
       asteroids.update()
       asteroids.draw(window)
       #перезарядка
       if rel_time == True:
           now_time = timer() #считываем время
       
           if now_time - last_time < 3: #пока не прошло 3 секунды выводим информацию о перезарядке
               reload = font2.render('Wait, reload...', 1, (150, 0, 0))
               window.blit(reload, (260, 460))
           else:
               num_fire = 0   #обнуляем счётчик пуль
               rel_time = False #сбрасываем флаг перезарядки
               
       #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
       #уменьшение кол-ва жизней, при столкновении с врагом
       if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
           sprite.spritecollide(ship, monsters, True)
           sprite.spritecollide(ship, asteroids, True)
           life = life -1 
        #выигрыш:
       if score >= goal:
           finish = True
           window.blit(win, (200, 200))
        #проигрыш:
       if life == 0 or lost >= max_lost:
           finish = True
           window.blit(lose, (200, 200))
       text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))
       text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50)) 
       
       #задаём разный цвет в зависимости от количества жизней
       if life == 3:
           life_color = (0, 150, 0)
       if life == 2:
           life_color = (150, 150, 0)
       if life == 1:
           life_color = (150, 0, 0)

       text_life = font1.render(str(life), 1, life_color)
       window.blit(text_life, (650, 10))

       display.update()
   #цикл срабатывает каждые 0.05 секунд
   time.delay(50)