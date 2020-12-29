import os

# Set the windows position
os.environ['SDL_VIDEO_WINDOW_POS'] = '400, 200'
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import shaders
import drawing
import pyrr
import improvedGraphics
import numpy as np


# Class window
class game:

    def __init__(self, width, height, title):
        # Initialise the glfw library

        pygame.init()

        # Setting up the pygame window
        pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)


        pygame.event.set_grab(True)
        pygame.mouse.set_visible(True)
        #pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
        pygame.mouse.set_cursor(*pygame.cursors.diamond)


        pygame.display.set_caption(title)

        self.new_graphic_settings = improvedGraphics.graphic(width, height)


        self.clock = pygame.time.Clock()

    def run(self):

        done = False


        # Loop
        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT or(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    done = True
                if event.type == pygame.VIDEORESIZE:
                    # Resizes window
                    self.new_graphic_settings.window_resize(event.w, event.h)


            keys_pressed = pygame.key.get_pressed()


            self.new_graphic_settings.player_move(keys_pressed)




            #self.new_graphic_settings.display_instanced()
            self.new_graphic_settings.display()

            pygame.display.flip()

            self.clock.tick(60)

        # Ends pygame
        pygame.quit()



new_game = game(1280, 720, "Main")
new_game.run()
