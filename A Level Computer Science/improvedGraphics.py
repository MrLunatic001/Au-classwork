from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import shaders
import pygame
import pyrr
import numpy
import math
import objectLoader
from textureLoader import load_textures
from camera import Camera
import os


class graphic():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.first_mouse = True
        self.models = []
        self.object_locations = []
        self.object_counter = 0

        self.compile_shader()
        self.create_object()
        self.initialise_camera()
        self.initalise_buffers()
        self.projection()

    def initialise_camera(self):
        self.cam = Camera()
        self.lastX, self.lastY = self.width / 2, self.height / 2
        self.first_mouse = True

    def textures(self):

        self.texture = glGenTextures(4)


    def projection(self):
        # Use shader
        glUseProgram(self.shader)

        # Create background colour

        glClearColor(0, 0.2, 0.1, 1)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Matrixes

        # Perpective projection
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, self.width / self.height, 0.1, 100)


        # Get locations
        self.model_location = glGetUniformLocation(self.shader, "model")
        self.projection_location = glGetUniformLocation(self.shader, "projection")
        self.view_loc = glGetUniformLocation(self.shader, "view")
        self.switcher_loc = glGetUniformLocation(self.shader, "switcher")

        glUniformMatrix4fv(self.projection_location, 1, GL_FALSE, projection)


    def display(self):

        # Specify Colour or Texture
        glUniform1i(self.switcher_loc, 0)

        # Draw
        for i in range(0, len(self.models)):
            if self.models[i][2]:
                pass
            else:
                glBindVertexArray(self.VAO[i])
                glBindTexture(GL_TEXTURE_2D, self.texture[i])
                glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.object_locations[i])
                glDrawArrays(GL_TRIANGLES, 0, len(self.models[i][0]))

    def compile_shader(self):
        # Compile shaders

        self.shader = compileProgram(compileShader(shaders.vertex_src, GL_VERTEX_SHADER),
                                     compileShader(shaders.fragment_src, GL_FRAGMENT_SHADER))



    def initalise_buffers(self):
        # Vertex Array Object
        self.VAO = glGenVertexArrays(len(self.models))
        VBO = glGenBuffers(len(self.models))

        for i in range(0, len(self.models)):
            glBindVertexArray(self.VAO[i])

            glBindBuffer(GL_ARRAY_BUFFER, VBO[i])
            glBufferData(GL_ARRAY_BUFFER, self.models[i][1].nbytes, self.models[i][1], GL_STATIC_DRAW)

            # Layer 1 (Position)
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.models[i][1].itemsize * 8, ctypes.c_void_p(0))

            # Layer 2 (Texture)
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.models[i][1].itemsize * 8, ctypes.c_void_p(12))



    def window_resize(self, width, height):
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
        glUniformMatrix4fv(self.projection_location, 1, GL_FALSE, projection)


    def player_move(self, keys_pressed):
        if keys_pressed[pygame.K_w]:
            self.cam.process_keyboard("FORWARD", 1)
        if keys_pressed[pygame.K_a]:
            self.cam.process_keyboard("LEFT", 1)
        if keys_pressed[pygame.K_s]:
            self.cam.process_keyboard("BACKWARD", 1)
        if keys_pressed[pygame.K_d]:
            self.cam.process_keyboard("RIGHT", 1)

        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] <= 0:
            pygame.mouse.set_pos((self.width - 1, mouse_pos[1]))
            self.lastX = self.width - 2

        elif mouse_pos[0] >= self.width - 1:
            pygame.mouse.set_pos((1, mouse_pos[1]))
            self.lastX = 1
        else:
            self.mouse_look(mouse_pos[0], mouse_pos[1])

        # Fill background colours
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Move camera
        self.view = self.cam.get_view_matrix()

        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, self.view)

    def mouse_look(self, x, y):

        pygame.mouse.set_pos(self.width / 2, self.height / 2)

        self.lastX = self.width / 2
        self.lastY = self.height / 2

        x_offset = x - self.lastX
        y_offset = self.lastY - y

        self.lastX = x
        self.lastY = y

        if self.first_mouse:
            self.cam.process_mouse_movement(0, 0)
            self.first_mouse = False
        else:
            self.cam.process_mouse_movement(x_offset, y_offset)

    def make_object(self, object_path, texture_path, position):
        self.models.append(objectLoader.ObjLoader.load_model(object_path))
        load_textures(texture_path, self.texture[self.object_counter])
        self.object_counter += 1
        self.object_locations.append(pyrr.matrix44.create_from_translation(pyrr.Vector3(position)))

    def create_object(self):
        self.textures()

        self.make_object("Objects/cube.obj", "Textures/wooden_box.png", [6, 1, 0])
        self.make_object("Objects/teapot.obj", "Textures/blue.jpg", [0, 0, 0])
        self.make_object("Objects/dragonlore.obj", "Textures/dragon_lore.bmp", [-6, 10, 0])
        self.make_object("Objects/floor.obj", "Textures/Brick_Block.png", [0, 0, 0])

