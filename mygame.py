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
        # площадь, которую будет занимать спрайт делаем кругом, чтобы максимально уточнить точку столкновения с другими спрайтами
        self.radius = 20
        # для проверки, насколько целесообразны размеры ректангла
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
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
        shoot_sound.play()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image_orig = pygame.transform.scale(self.image_orig, (int(self.image_orig.get_width() * .70), int(self.image_orig.get_width() * .70)))
        # как я понял, мы копируем изображение, чтобы изображение для создания мобов оставался неизменным
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        # площадь, которую будет занимать спрайт делаем кругом,
        # чтобы максимально уточнить точку столкновения с другими спрайтами
        self.radius = int(self.rect.width * .85 / 2)
        # для проверки, насколько целесообразны размеры ректангла
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        # эта функция нужна для вращения. если с момента последнего обновления прошло более 50 миллисекунд, то происходит вращение
        if now - self.last_update > 50:
            self.last_update = now
            # зафиксируем новое положение моба. чтобы оно следующее вращение начал с такой позации
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.rotate()
        # создаем новых мобов, когда старые пропадают с экрана
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    # с помощью метода blit мы рисуем новую поверхность(т.е. это не спрайт, спрайты с ним не будут взаимодействовать.
    surf.blit(text_surface, text_rect)





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
sound_folder = os.path.join(game_folder, 'sounds_rpg_space')
player_img = pygame.image.load(os.path.join(img_folder, 'starship.png')).convert()
background_img = pygame.image.load(os.path.join(img_folder, 'starfield.png')).convert()
background_rect = background_img.get_rect()
meteor_img = pygame.image.load(os.path.join(img_folder, 'meteorBrown_big4.png')).convert()
bullet_img = pygame.image.load(os.path.join(img_folder, 'laserGreen10.png')).convert()
# звуки
# звук выстрела
shoot_sound = pygame.mixer.Sound(os.path.join(sound_folder, 'Laser_Shoot.wav'))
# звук фоновая музыка
# сначала загружаем музыку
pygame.mixer.music.load(os.path.join(sound_folder, 'BossMain.wav'))
# устанавливаем громкость музыки, чтобы оно не перекрывало другие звуки. сейчас установлено 40% от своей
# метод play() опубликована чуть ниже, рядом с score
pygame.mixer.music.set_volume(0.4)
# звуки взрывов
explosion_sound = []
for snd in ['Hit_Hurt.wav', 'Explosion37.wav']:
    explosion_sound.append(pygame.mixer.Sound(os.path.join(sound_folder, snd)))

meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big4.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
meteor_images = []
for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_folder, img)).convert())

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
# этот цикл for для создания мобов до игрового цикла
# потом внутри игрового цикла тоже есть цикл for, чтобы добавлять новых мобов вместо умерших
for i in range(8):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)

score = 0

# включаем музыку фоновую
# она загружена и определена выше
# loops означает насколько часто воспроизводится песня. значение -1 повторяет музыку бесконечно
pygame.mixer.music.play(loops=-1)




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
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)

    if hits:
        # sleep(5)
        running = False
    # Проверка, не попадала ли пуля мобу
    # здесь возвращается пересечения мобов и пулей
    hits_bullet = pygame.sprite.groupcollide(mobs, bullets, True, True)
    # каждый убитый моб заменяется новым
    for hit in hits_bullet:
        # за каждый убитый моб присваиваются очки, чем больше мод, тем меньше score, т.к. легче попасть
        score += 50 - hit.radius
        random.choice(explosion_sound).play()
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        # print(score)

    # Рендеринг или простыми словами прорисовка
    screen.fill(BLACK)
    screen.blit(background_img, background_rect)
    all_sprites.draw(screen)
    # рисуем счет для игры
    # получается мы рисуем буквы на нашем экране screen
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()


pygame.quit()

