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

# ground_vertices = (

#     (-10, -1, 20),
#     (10, -1, 20),
#     (10, -1, -100),
#     (-10, -1, -100),
#     )


# def ground():
#     glBegin(GL_QUADS)
#     for vertex in ground_vertices:
#         glColor3fv((0, 0.5, 0.5))
#         glVertex3fv(vertex)
#     glEnd()


def set_vertices(max_distance, min_distance=-20, camera_x=0, camera_y=0):

    camera_x = 1 * int(camera_x)
    camera_y = 1 * int(camera_y)

    x_value_change = rd.randrange(camera_x - 75, camera_x + 75)
    y_value_change = rd.randrange(camera_y - 75, camera_y + 75)
    z_value_change = rd.randrange(-1 * max_distance, min_distance)

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

    max_dist = 100

    gluPerspective(45, (display[0]/display[1]), 0.1, max_dist)

    glTranslatef(0,0, -40.0)

    # glRotatef(25, 2, 1, 0)

    cur_x = 0
    cur_y = 0

    x_vel = 0
    y_vel = 0

    game_speed = 2
    player_speed = 2

    cube_dict = {}

    for x in range(75):
        cube_dict[x] = set_vertices(max_dist)

    # object_passed = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_vel = player_speed
                if event.key == pygame.K_RIGHT:
                    x_vel = -player_speed
                if event.key == pygame.K_UP:
                    y_vel = -player_speed
                if event.key == pygame.K_DOWN:
                    y_vel = player_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_vel = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_vel = 0

        x = glGetDoublev(GL_MODELVIEW_MATRIX)

        camera_x = x[3][0]
        camera_y = x[3][1]
        camera_z = x[3][2]

        cur_x += x_vel
        cur_y += y_vel

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glTranslatef(x_vel, y_vel, game_speed)

        # ground()

        for each_cube in cube_dict:
            Cube(cube_dict[each_cube])

        # delete_list = []

        for each_cube in cube_dict:
            if camera_z <= cube_dict[each_cube][0][2]:
                print("Passed a Cube!")
                # delete_list.append(each_cube)
                new_max = int(-1 * (camera_z - (max_dist * 2)))
                cube_dict[each_cube] = set_vertices(new_max,
                                                    int(camera_z) - max_dist,
                                                    cur_x,
                                                    cur_y)
                print(camera_x)
                print(cur_x)

        pygame.display.flip()
        # pygame.time.wait(10)


main()
pygame.quit()
quit()
