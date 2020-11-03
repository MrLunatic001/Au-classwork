import pygame
import random

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
width = 1100
height = 700
size = (width, height)
screen = pygame.display.set_mode(size)
INVADER_IMAGE = pygame.image.load('invader.jpeg')
INVADER_IMAGE = pygame.transform.scale(INVADER_IMAGE, (50, 50))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class invaders(pygame.sprite.Sprite):
    global width, height
    speed = 5


    def __init__(self, x, y):
        super().__init__()
        self.image = INVADER_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self):
        if self.rect.x + self.speed > width:
            self.rect.x = 0
            self.rect.y += 100
        else:
            self.rect.x += self.speed


class player(pygame.sprite.Sprite):
    global width, height
    speed = 0

    def __init__(self):
        super().__init__()
        self.speed = 0
        self.image = pygame.Surface([100, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = width / 2
        self.rect.y = height - height * 0.1 - 14

    def update_speed(self, speed):
        self.speed = speed

    def update(self):
        if self.rect.x + self.speed + 100 > width:
            self.rect.x = width - 100
        elif self.rect.x + self.speed < 0:
            self.rect.x = 0
        else:
            self.rect.x += self.speed


class bullet(pygame.sprite.Sprite):
    speed = -20

    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = width + 50
        self.rect.y = height

    def update(self):
        self.rect.y += self.speed

    def get_y(self):
        return self.rect.y


clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")
score = 0
gameover_message = myfont.render("Game Over!", True, RED)
win_message = myfont.render("You win!", True, GREEN)
gameover = False
win = False
life = 5
bullets = 50
invaders_group = pygame.sprite.Group()
all_sprites_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
for y in range(0, 250, 100):
    if y / 100 % 2 == 0:
        for x in range(200, width - 200, 100):
            invader = invaders(x, y)
            all_sprites_group.add(invader)
            invaders_group.add(invader)
    else:
        for x in range(250, width - 250, 100):
            invader = invaders(x, y)
            all_sprites_group.add(invader)
            invaders_group.add(invader)

player_group = player()
all_sprites_group.add(player_group)
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_group.update_speed(-10)  # speed set to -3
            elif event.key == pygame.K_RIGHT:  # - if the right key pressed
                player_group.update_speed(10)  # speed set to 3
            elif event.key == pygame.K_SPACE:
                if bullets != 0:
                    sbullet = bullet(player_group.rect.x, player_group.rect.y)
                    bullet_group.add(sbullet)
                    all_sprites_group.add(sbullet)
                    bullets -= 1
        elif event.type == pygame.KEYUP:  # - a key released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_group.update_speed(0)  # speed set to 0
    player_hit_group = pygame.sprite.groupcollide(bullet_group, invaders_group, True, True)
    if player_hit_group:
        for play in player_hit_group:
            score += 1
    score_text = myfont.render("Score: " + str(score), True, WHITE)
    bullet_text = myfont.render("Bullets: " + str(bullets), True, WHITE)
    gameover_group = pygame.sprite.spritecollide(player_group, invaders_group, True)

    for bul in bullet_group:
        if bul.get_y() < 0:
            bullet_group.remove(bul)
            all_sprites_group.remove(bul)

    all_sprites_group.update()
    screen.fill(BLACK)
    all_sprites_group.draw(screen)
    screen.blit(score_text, [20, 30])
    screen.blit(bullet_text, [20, 50])
    if gameover_group:
        life -= 1
    if life == 0:
        screen.blit(gameover_message, [width / 2, height / 2])
        gameover = True
        done = True
    if score == 20:
        win = True
        done = True
    life_text = myfont.render("Lifes: " + str(life), True, WHITE)
    screen.blit(life_text, [20, 70])
    pygame.display.flip()
    clock.tick(60)
while gameover:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = False
    screen.blit(gameover_message, [width / 2, height / 2])
    pygame.display.flip()
    clock.tick(60)
while win:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win = False
    screen.blit(win_message, [width / 2, height / 2])
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
exit()
