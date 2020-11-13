import pygame, sys, random
# use up arrow, down arrow, w key and s key to move both paddels
def ball_animation():
    global speed_x,speed_y, player_score, opponent_score,dead
    if dead == True:
        pygame.time.delay(500)
    dead = False
    ball.x += speed_x
    ball.y += speed_y
    if ball.top <= 0 or ball.bottom >= height:
        speed_y *= -1
    if ball.left <= 0 :
        speed_x *= -1
        opponent_score += 1
        ball_restart()
    if ball.right >= width:
        speed_x *= -1
        player_score += 1
        ball_restart()
    if ball.colliderect(player) or ball.colliderect(opponent):
        speed_x *= -1

def player_animation():
    if player.top <= 0:
        player.top = 0
    if player.bottom >= height:
        player.bottom = height

def opponent_animation():
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= height:
        opponent.bottom = height

def logic():
    global player_speed, opponent_speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += moving_speed
            if event.key == pygame.K_UP:
                player_speed -= moving_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= moving_speed
            if event.key == pygame.K_UP:
                player_speed += moving_speed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                opponent_speed += moving_speed
            if event.key == pygame.K_w:
                opponent_speed -= moving_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                opponent_speed -= moving_speed
            if event.key == pygame.K_w:
                opponent_speed += moving_speed

def ball_restart():
    global speed_y, speed_x, dead
    ball.center = (width/2,height/2)
    speed_y *= random.choice((1,-1))
    speed_x *= random.choice((1,-1))
    dead = True

def score():
    global player_score, opponent_score
    player_text = font.render(str(player_score),True,white)
    screen.blit(player_text, [width/4,height/7])
    opponent_text = font.render(str(opponent_score),True,white)
    screen.blit(opponent_text, [width/4 + width/2,height/7])
pygame.init()
white = (255,255,255)
black = (0,0,0)
grey = (200,200,200)
width = 1100
height = 700
size = (width,height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
done = False
dead = False
clock = pygame.time.Clock()
ball= pygame.Rect(width/2-15,height/2-15,30,30)
player = pygame.Rect(width - 20, height/2 - 70, 10,140)
opponent = pygame.Rect(10,height/2 - 70, 10, 140)
speed_x = 16 * random.choice((1,-1))
speed_y = 16 * random.choice((1,-1))
opponent_speed = 0
player_speed = 0
player_score = 0
opponent_score = 0
moving_speed = 10
font = pygame.font.SysFont('Calibri', 100, True, False)

while not done:

    logic()
    ball_animation()
    player.y += player_speed
    opponent.y += opponent_speed

    player_animation()
    opponent_animation()

    if dead == True:
        player = pygame.Rect(width - 20, height/2 - 70, 10,140)
        opponent = pygame.Rect(10,height/2 - 70, 10, 140)
    screen.fill(black)
    pygame.draw.rect(screen,grey, player)
    pygame.draw.rect(screen,grey, opponent)
    pygame.draw.ellipse(screen,grey, ball)
    pygame.draw.aaline(screen, grey, (width/2,0),(width/2,height))
    score()


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
exit()