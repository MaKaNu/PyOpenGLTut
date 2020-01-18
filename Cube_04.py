import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import random as rd

#       THE CUBE
#
#      2_________ 1
#      /|       /|
#    6/_|______/5|
#     |3|______|_| 0
#     | /      | /
#    7|/_______|/4

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
    (-1, -1, 1)
    )

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 5),
    (2, 3),
    (2, 6),
    (3, 7),
    (4, 5),
    (4, 7),
    (5, 6),
    (6, 7)
    )

surfaces = (
    (0, 1, 2, 3),
    (1, 2, 6, 5),
    (4, 5, 6, 7),
    (0, 3, 7, 4),
    (0, 1, 5, 4),
    (2, 3, 7, 6)
    )

colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
)

ground_vertices = (
    (-10, -1, 20),
    (10, -1, 20),
    (-10, -1, -100),
    (10, -1, -100),
    )


def ground():
    glBegin(GL_QUADS)
    for vertex in ground_vertices:
        glColor3fv((0, 0.5, 0.5))
        glVertex3fv(vertex)
    glEnd()


def set_vertices(max_distance):
    x_value_change = rd.randrange(-10, 10)
    y_value_change = 0  # rd.randrange(-10, 10)
    z_value_change = rd.randrange(-1 * max_distance, -20)

    new_vertices = []

    for vert in vertices:
        new_vert = []

        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change

        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)

        new_vertices.append(new_vert)
    return new_vertices


def Cube(vertices):
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    # glTranslatef(rd.randrange(-5, 5), rd.randrange(-5, 5), -40.0)

    # glRotatef(25, 2, 1, 0)
    x_vel = 0
    y_vel = 0

    max_dist = 100

    cube_dict = {}

    for x in range(20):
        cube_dict[x] = set_vertices(max_dist)

    # object_passed = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_vel = 0.3
                if event.key == pygame.K_RIGHT:
                    x_vel = -0.3
                if event.key == pygame.K_UP:
                    y_vel = -0.3
                if event.key == pygame.K_DOWN:
                    y_vel = 0.3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_vel = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_vel = 0

        x = glGetDoublev(GL_MODELVIEW_MATRIX)

        camera_x = x[3][0]
        camera_y = x[3][1]
        camera_z = x[3][2]

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glTranslatef(x_vel, y_vel, 0.5)

        ground()

        for each_cube in cube_dict:
            Cube(cube_dict[each_cube])
        pygame.display.flip()
        pygame.time.wait(10)


main()
pygame.quit()
quit()
