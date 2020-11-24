import pygame

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Loading sprites

# Defining some lists to hold the sprites

down = list()
left = list()
right = list()
up = list()

for i in range(8):
    down.append(pygame.transform.scale(pygame.image.load('movement/'+'down'+str(i)+'.png'), (60, 60)))
    left.append(pygame.transform.scale(pygame.image.load('movement/'+'left'+str(i)+'.png'), (60, 60)))
    right.append(pygame.transform.scale(pygame.image.load('movement/'+'right'+str(i)+'.png'), (60, 60)))
    up.append(pygame.transform.scale(pygame.image.load('movement/'+'up'+str(i)+'.png'), (60, 60)))
# Defining Classes

# Class Wall

class wall(pygame.sprite.Sprite):
    # Set up attributes for the class wall
    width = 40
    height = 40

    def __init__(self, colour, x, y):
        super().__init__()
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_pos(self):
        return self.rect.right, self.rect.left, self.rect.top, self.rect.bottom


# Player Class


class player(pygame.sprite.Sprite):
    # Set up attributes for the class player
    global down, up, left, right

    def __init__(self, x, y,  width, height):
        super().__init__()
        self.speed_y = 0
        self.speed_x = 0
        self.health = 100
        self.money = 0
        self.score = 0
        self.width = width
        self.height = height
        self.image = down.__getitem__(0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # Defining functions

    def get_items(self):
        return self.health, self.money, self.score


    def get_pos(self):
        return self.rect.right, self.rect.left, self.rect.top, self.rect.bottom

    def set_right(self, x):
        self.rect.right = x



    def set_left(self, x):
        self.rect.left = x


    def set_top(self, x):
        self.rect.top = x

    def set_bottom(self, x):
        self.rect.bottom = x

    def set_image(self, image):
        self.image = image

    def move_up(self):
        self.speed_y = -20


    def move_down(self):
        self.speed_y = 20


    def move_right(self):
        self.speed_x = 20


    def move_left(self):
        self.speed_x = -20


    def stop_x(self):
        self.speed_x = 0

    def stop_y(self):
        self.speed_y = 0

    def update(self):
        #Check x coordinates first
        self.rect.x += self.speed_x
        collide_list = pygame.sprite.spritecollide(main_player, wall_group, False)
        if collide_list:
            for block in collide_list:
                if self.speed_x < 0:
                    main_player.set_left(block.get_pos()[0])
                elif self.speed_x > 0:
                    main_player.set_right(block.get_pos()[1])
                elif self.speed_y < 0:
                    main_player.set_top(block.get_pos()[3])
                elif self.speed_y > 0:
                    main_player.set_bottom(block.get_pos()[2])
        self.rect.y += self.speed_y
        collide_list = pygame.sprite.spritecollide(main_player, wall_group, False)
        if collide_list:
            for block in collide_list:
                if self.speed_y < 0:
                    main_player.set_top(block.get_pos()[3])
                elif self.speed_y > 0:
                    main_player.set_bottom(block.get_pos()[2])

#Enemy class inherites Player class
class Enemy(player):
    def __init__(self, x, y, colour, width, height):
        super().__init__(x, y, width, height)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(colour)



# Create an All Sprites Group object

all_sprites_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# Instantiate a player object

main_player = player(500, 500, 30, 30)
all_sprites_group.add(main_player)
enemy_1 = Enemy(50,50,YELLOW, 40, 40)
all_sprites_group.add(enemy_1)
enemy_group.add(enemy_1)
enemy_2 = Enemy(50, 900, YELLOW, 40, 40)
all_sprites_group.add(enemy_2)
enemy_group.add(enemy_2)
enemy_3 = Enemy(900, 900, YELLOW, 40, 40)
all_sprites_group.add(enemy_3)
enemy_group.add(enemy_3)
up_counter = 0
down_counter = 0
right_counter = 0
left_counter = 0

player_group.add(main_player)

# Set the width and height of the screen [width, height]
size = (1200, 1000)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
font = pygame.font.SysFont('Calibri', 20, True, False)

# Loop until the user clicks the close button.
done = False
template_wall =[ "/////////////////////////",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/00000000000000000000000/",
                 "/////////////////////////"]


score = ""
health = ""
money = ""

# Instantiate walls
y = 0
x = 0
counter = 1
# Iterates through each character in the wall template.
for element in template_wall:
    # If the character is "/", make a wall at that position, if not, skip the position.
    for block in element:
        if block == "/":
            new_wall = wall(RED, x, y)
            all_sprites_group.add(new_wall)
            wall_group.add(new_wall)

        counter += 1
        x += 40
        # If the number of walls reaches 25 (maximum width of the window), go to the next line
        if counter > 25:
            counter = 1
            y += 40
            x = 0




# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # User presses down a key
        if event.type == pygame.KEYDOWN:

            # Moves player
            if event.key == pygame.K_UP:
                main_player.move_up()

            elif event.key == pygame.K_DOWN:
                main_player.move_down()

            elif event.key == pygame.K_RIGHT:
                main_player.move_right()

            elif event.key == pygame.K_LEFT:
                main_player.move_left()

        # User releases a key
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                main_player.stop_y()
            elif event.key == pygame.K_DOWN:
                main_player.stop_y()
            elif event.key == pygame.K_RIGHT:
                main_player.stop_x()
            elif event.key == pygame.K_LEFT:
                main_player.stop_x()

    # --- Game logic should go here

    # Checks if player collides with wall, if true, set the play position 1 pixel next to the wall




    # --- Screen-clearing code goes here


    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)

    # --- Drawing code should go here
    all_sprites_group.update()
    all_sprites_group.draw(screen)
    score_text = font.render("Score: "+str(main_player.get_items()[2]), True, WHITE)
    health_text = font.render("Health: "+str(main_player.get_items()[0]), True, WHITE)
    money_text = font.render("Score: "+str(main_player.get_items()[1]), True, WHITE)
    screen.blit(score_text, [1050, 300])
    screen.blit(health_text, [1050, 350])
    screen.blit(money_text, [1050, 400])

    # Updates player sprite

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        main_player.set_image(left[left_counter])
        if left_counter + 1 < 8:
            left_counter += 1
        else:
            left_counter = 0
    elif keys[pygame.K_RIGHT]:
        main_player.set_image(right[right_counter])
        if right_counter + 1 < 8:
            right_counter += 1
        else:
            right_counter = 0
    elif keys[pygame.K_UP]:
        main_player.set_image(up[up_counter])
        if up_counter + 1 < 8:
            up_counter += 1
        else:
            up_counter = 0
    elif keys[pygame.K_DOWN]:
        main_player.set_image(down[down_counter])
        if down_counter + 1 < 8:
            down_counter += 1
        else:
            down_counter = 0



# --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
