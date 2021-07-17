import pygame
import random
import os
from time import sleep


WIDTH = 480
HEIGHT = 600
# частота кадров в секунду
FPS = 60
# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BlueViolet = (138, 43, 226)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.image.set_colorkey(BLACK)
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        # слева направо
        # self.rect.x += 5
        # if self.rect.left > WIDTH:
        #     self.rect.right = 0
        # сверху вниз
        # self.rect.y += 5
        # if self.rect.top > HEIGHT:
        #     self.rect.bottom = 0
        self.speedx = 0
        self.rect.x += self.speedx
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # создаем новых мобов, когда старые пропадают с экрана
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(BlueViolet)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()




# создаем игру и окно
pygame.init()
# для звука
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My game')
# clock нужно для проверки, что игра работает нужной частотой кадров
clock = pygame.time.Clock()



game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'arts')
player_img = pygame.image.load(os.path.join(img_folder, 'starship.png')).convert()

# спрайты движущиеся обьекты
# группы
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
# цикл for может находится внутри цикла while, т.к. мобы создаются один раз, т.е. 8 штук
# потом они просто будут при исчезновении заменяться новыми. т.е.
# в один момент времени будут только 8 мобов
for i in range(1, 8):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)





# Цикл игры

# Ввод процесса (события)
# Обновление
# Визуализация (сборка)
# это все будет внутри while

running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT:
        #         player.speedx = -8
        #     if event.key == pygame.K_RIGHT:
        #         player.speedx = 8
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Обновление т.е. все спрайты вызываются с помощью этого метода.
    # у всех спрайтов есть метод update, они то и здесь и вызываются
    all_sprites.update()

    # проверяем, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, False)

    if hits:
        # sleep(5)
        running = False
    # Проверка, не попадала ли пуля мобу
    # здесь возвращается пересечения мобов и пулей
    hits_bullet = pygame.sprite.groupcollide(mobs, bullets, True, True)
    # каждый убитый моб заменяется новым
    for hit in hits_bullet:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # Рендеринг или простыми словами прорисовка
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()


pygame.quit()

