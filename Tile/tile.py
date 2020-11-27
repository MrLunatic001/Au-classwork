import pygame, copy, os, csv

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
YELLOW = (200, 200, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GREY = (192,192,192)


# Loading sprites

# Defining some lists to hold the sprites

down = list()
left = list()
right = list()
up = list()
keys = list()
portals = list()
enemy_kim = list()

for i in range(9):
    down.append(pygame.transform.scale(pygame.image.load('movement/' + 'down' + str(i) + '.png'), (60, 60)))
    left.append(pygame.transform.scale(pygame.image.load('movement/' + 'left' + str(i) + '.png'), (60, 60)))
    right.append(pygame.transform.scale(pygame.image.load('movement/' + 'right' + str(i) + '.png'), (60, 60)))
    up.append(pygame.transform.scale(pygame.image.load('movement/' + 'up' + str(i) + '.png'), (60, 60)))
    keys.append(pygame.transform.scale(pygame.image.load('keys/' + 'keys' + str(i) + '.png'), (30, 30)))
    portals.append(pygame.transform.scale(pygame.image.load('portal/' + 'portal' + str(i) + '.png'), (100, 100)))
for i in range(3):
    enemy_kim.append(pygame.transform.scale(pygame.image.load('Enemies/' + 'kim' + str(i) + '.png'), (40, 40)))


# Defining Classes

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=BLUE):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


# Create class of game:

class game():

    def __init__(self, initial_store_list, restart_list):
        self.LEVEL_COUNTER = 1
        self.storage_levels = initial_store_list
        self.restart_list = restart_list

    # Class Wall

    def level(self, current_level, LIVES):

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

        # Class Keys

        class key(pygame.sprite.Sprite):
            def __init__(self, x, y):
                super().__init__()
                self.image = keys[0]
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.sprite_key_count = 0

            def update(self):
                self.image = keys[self.sprite_key_count]
                if self.sprite_key_count + 1 < 9:
                    self.sprite_key_count += 1
                else:
                    self.sprite_key_count = 0

        # Portal Class
        class portal(pygame.sprite.Sprite):
            def __init__(self, x, y):
                super().__init__()
                self.image = portals[0]
                self.portal_count = 0
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y

            def update(self):
                self.image = portals[self.portal_count]
                if self.portal_count + 1 < 9:
                    self.portal_count += 1
                else:
                    self.portal_count = 0

        # Player Class

        class player(pygame.sprite.Sprite):
            # Set up attributes for the class player
            global down, up, left, right, main_player, wall_group

            def __init__(self, x, y, width, height, live):
                super().__init__()
                self.speed_y = 0
                self.speed_x = 0
                self.health = live
                self.money = 0
                self.score = 0
                self.width = width
                self.height = height
                self.image = down[0]
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.keys = 0

            # Defining functions

            def add_key(self):
                self.keys += 1

            def reset_keys(self):
                self.keys = 0

            def get_items(self):
                return self.health, self.money, self.score, self.keys

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

            def loose_life(self):
                self.health -= 1

            def update(self):
                # Check x coordinates first
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

        # Enemy class inherites Player class
        class Enemy(player):
            def __init__(self, x, y, colour, width, height):
                super().__init__(x, y, width, height, 3)
                self.image = enemy_kim[0]
                self.image_count = 0

            def update(self):
                self.image = enemy_kim[self.image_count]
                if self.image_count + 1 < 3:
                    self.image_count += 1
                else:
                    self.image_count = 0

        # Create an All Sprites Group object

        all_sprites_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        wall_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        portal_group = pygame.sprite.Group()
        key_group = pygame.sprite.Group()

        up_counter = 0
        down_counter = 0
        right_counter = 0
        left_counter = 0

        # Set the width and height of the screen [width, height]
        size = (1200, 1000)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Tile")
        font = pygame.font.SysFont('Calibri', 20, True, False)

        # Loop until the user clicks the close button.
        done = False

        score = ""
        health = ""
        money = ""

        # Instantiate walls
        y = 0
        x = 0
        main_player_x = 0
        main_player_y = 0
        counter = 1
        # Iterates through each character in the wall template.
        for element in current_level:
            # If the character is "/", make a wall at that position, if not, skip the position.
            for block in element:
                if block == "/":
                    new_wall = wall(RED, x, y)
                    all_sprites_group.add(new_wall)
                    wall_group.add(new_wall)
                elif block == "K":
                    new_key = key(x, y)
                    key_group.add(new_key)
                    all_sprites_group.add(new_key)
                elif block == "E":
                    new_enemy = Enemy(x, y, YELLOW, 40, 40)
                    all_sprites_group.add(new_enemy)
                    enemy_group.add(new_enemy)
                elif block == "P":
                    main_player = player(x, y, 30, 30, LIVES)
                    all_sprites_group.add(main_player)
                    player_group.add(main_player)

                counter += 1
                x += 40
                # If the number of walls reaches 25 (maximum width of the window), go to the next line
                if counter > 25:
                    counter = 1
                    y += 40
                    x = 0

        # Portal spawned is False
        spawned = False

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # Return code when while loop ends
        RETURN_CODE = 0

        # -------- Main Program Loop -----------
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
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
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        main_player.stop_y()
                    elif event.key == pygame.K_DOWN:
                        main_player.stop_y()
                    elif event.key == pygame.K_RIGHT:
                        main_player.stop_x()
                    elif event.key == pygame.K_LEFT:
                        main_player.stop_x()

                # Checks if any key is pressed and update the player movement accordingly
                pressed = pygame.key.get_pressed()
                if pressed is not None:
                    if pressed[pygame.K_UP]:
                        main_player.move_up()

                    elif pressed[pygame.K_DOWN]:
                        main_player.move_down()

                    elif pressed[pygame.K_RIGHT]:
                        main_player.move_right()

                    elif pressed[pygame.K_LEFT]:
                        main_player.move_left()

            # --- Game logic should go here
            keys_collide_list = pygame.sprite.spritecollide(main_player, key_group, True)
            for i in keys_collide_list:
                main_player.add_key()

            # Checks if all 3 keys are collected

            if main_player.get_items()[3] == 3:
                if not spawned:
                    counter = 0
                    x = 0
                    y = 0
                    spawned = True

                    # Spawns a portal for the player to get to the next level
                    for el in current_level:
                        for bl in el:
                            if bl == "P":
                                new_portal = portal(x, y)
                                all_sprites_group.add(new_portal)
                                portal_group.add(new_portal)
                            counter += 1
                            x += 40
                            # If the number of walls reaches 25 (maximum width of the window), go to the next line
                            if counter > 25:
                                counter = 1
                                y += 40
                                x = 0

            # Ends the level if player touches the portal
            if pygame.sprite.groupcollide(player_group, portal_group, True, True):
                done = True

                RETURN_CODE = 3

            # Checks if player collides with enemy
            if pygame.sprite.spritecollide(main_player, enemy_group, False):
                # Player looses health
                main_player.loose_life()
                done = True
                RETURN_CODE = 1
            # Checks if player is dead
            if main_player.get_items()[0] <= 0:
                done = True
                RETURN_CODE = 2

            # Background Colour

            screen.fill(BLACK)

            # --- Drawing code should go here
            all_sprites_group.update()
            all_sprites_group.draw(screen)

            # Text to be rendered
            score_text = font.render("Score: " + str(main_player.get_items()[2]), True, WHITE)
            health_text = font.render("Lives: " + str(main_player.get_items()[0]), True, WHITE)
            money_text = font.render("Money: " + str(main_player.get_items()[1]), True, WHITE)
            keys_text = font.render("Keys: " + str(main_player.get_items()[3]) + "/3", True, WHITE)
            level_text = font.render("Level: " + str(self.LEVEL_COUNTER), True, WHITE)
            screen.blit(score_text, [1050, 300])
            screen.blit(health_text, [1050, 350])
            screen.blit(money_text, [1050, 400])
            screen.blit(keys_text, [1050, 450])
            screen.blit(level_text, [1050, 250])

            # Updates player sprite
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                main_player.set_image(left[left_counter])
                if left_counter + 1 < 9:
                    left_counter += 1
                else:
                    left_counter = 0
            elif pressed[pygame.K_RIGHT]:
                main_player.set_image(right[right_counter])
                if right_counter + 1 < 9:
                    right_counter += 1
                else:
                    right_counter = 0
            elif pressed[pygame.K_UP]:
                main_player.set_image(up[up_counter])
                if up_counter + 1 < 9:
                    up_counter += 1
                else:
                    up_counter = 0
            elif pressed[pygame.K_DOWN]:
                main_player.set_image(down[down_counter])
                if down_counter + 1 < 9:
                    down_counter += 1
                else:
                    down_counter = 0

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(60)

        if RETURN_CODE == 1:
            self.level(current_level, main_player.get_items()[0])
        elif RETURN_CODE == 2:
            self.loose()
        elif RETURN_CODE == 3:
            if len(self.storage_levels) == 0:
                self.win()
            else:
                self.LEVEL_COUNTER += 1
                self.level(self.storage_levels.pop(), main_player.get_items()[0])

    def start(self):

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        done = False
        # Set the width and height of the screen [width, height]
        size = (1200, 1000)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Welcome!")
        font = pygame.font.SysFont('Calibri', 50, True, False)
        start_button = button(YELLOW, 470, 600, 300, 150, "Start")

        # -------- Main Program Loop -----------
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if start_button.isOver(mouse_position):
                        start_button.color = (255, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()
                    if start_button.isOver(mouse_position):
                        done = True

            # --- Game logic should go here

            # Background Colour

            screen.fill(BLACK)

            # --- Drawing code should go here
            welcome_message = font.render("Welcome to the Tile Game", True, WHITE)
            screen.blit(welcome_message, [380, 400])

            start_button.draw(screen)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(60)

        self.level(self.storage_levels.pop(), 3)

    def loose(self):

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        done = False
        # Set the width and height of the screen [width, height]
        size = (1200, 1000)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Game Over!")
        font = pygame.font.SysFont('Calibri', 50, True, False)
        restart_button = button(GREEN, 470, 600, 300, 150, "Restart")
        quit_button = button(RED, 470, 800, 300, 150, "Quit")

        # -------- Main Program Loop -----------
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if quit_button.isOver(mouse_position):
                        quit_button.color=(255,0,0)
                    elif restart_button.isOver(mouse_position):
                        restart_button.color = (0, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()
                    if quit_button.isOver(mouse_position):
                        pygame.quit()
                    elif restart_button.isOver(mouse_position):
                        done = True

            # --- Game logic should go here

            # Background Colour

            screen.fill(BLACK)

            # --- Drawing code should go here
            loose_message = font.render("You loose!", True, RED)
            screen.blit(loose_message, [500, 400])

            restart_button.draw(screen)
            quit_button.draw(screen)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(60)

        # Refill the levels list:
        self.storage_levels = copy.deepcopy(self.restart_list)
        self.LEVEL_COUNTER = 1
        self.level(self.storage_levels.pop(), 3)

    def win(self):
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        done = False
        # Set the width and height of the screen [width, height]
        size = (1200, 1000)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Congratulations!")
        font = pygame.font.SysFont('Calibri', 50, True, False)
        restart_button = button(GREEN, 470, 600, 300, 150, "Restart")
        quit_button = button(RED, 470, 800, 300, 150, "Quit")

        # -------- Main Program Loop -----------
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if quit_button.isOver(mouse_position):
                        quit_button.color = (255, 0, 0)
                    elif restart_button.isOver(mouse_position):
                        restart_button.color = (0, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()
                    if quit_button.isOver(mouse_position):
                        pygame.quit()
                    elif restart_button.isOver(mouse_position):
                        done = True

            # --- Game logic should go here

            # Background Colour

            screen.fill(BLACK)

            # --- Drawing code should go here
            loose_message = font.render("Congratulations, you win!", True, YELLOW)
            screen.blit(loose_message, [400, 400])

            restart_button.draw(screen)
            quit_button.draw(screen)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(60)

        # Refill the levels list:
        self.storage_levels = copy.deepcopy(self.restart_list)
        self.LEVEL_COUNTER = 1
        self.level(self.storage_levels.pop(), 3)


levels = list()
restart = list()

# Scans through the levels directory and stores them in the levels/ restart list

for root, dirs, files in os.walk('levels'):
    for file in files:
        temp_counter = 0
        temp_array = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                      ""]

        # Opens csv file
        with open("levels/" + file) as csvfile:
            csvreader = csv.reader(csvfile)

            # Reads row in csv file
            for row in csvreader:
                temp_string = ""
                # Stores each letter in each row in a temeporary string
                for letter in row:
                    temp_string += letter
                # Appends it to a level array
                temp_array[temp_counter] = temp_string
                temp_counter += 1
            # Appends the array to the level list
            levels.append(temp_array)
            restart.append(temp_array)

# Starts the game

new_game = game(levels, restart)
new_game.start()
