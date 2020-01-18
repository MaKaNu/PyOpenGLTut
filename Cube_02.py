import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

#       THE CUBE
#
#      2_________ 1
#      /|       /|
#    6/_|______/5|
#     |3|______|_| 0
#     | /      | /
#    7|/_______|/4

verticies = (
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


def Cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0]/display[1]), 6, 50.0)

    glTranslatef(0.0, 0.0, -10.0)

    glRotatef(25, 2, 1, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-1.0, 0.0, 0.0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(1.0, 0.0, 0.0)
                if event.key == pygame.K_UP:
                    glTranslatef(0.0, 1.0, 0.0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0.0, -1.0, 0.0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0.0, 0.0, 1.0)
                if event.button == 5:
                    glTranslatef(0.0, 0.0, -1.0)

        # glRotatef(1, 3, 1, 1) #Rotate Automatic
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)


main()
