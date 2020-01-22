import glfw
from OpenGL.GL import *
import numpy as np
from math import sin, cos

# Creates a Trinagle with the fixed function pipeline (deprecated)

# Initialize GLFW Lib
if not glfw.init():
    raise Exception("GLFW can not be initialzed!")

# Create a Window
window = glfw.create_window(800, 600, "My OpenGL Window", None, None)

# Check if Window is created
if not window:
    glfw.terminate()
    raise Exception("GLFW window can not be created!")

# set Window Position
glfw.set_window_pos(window, 400, 200)

# make the context current
glfw.make_context_current(window)

vertices = [-0.5, -0.5, 1.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0]

colors = [1.0, 0.0, 0.0,
          0.0, 1.0, 0.0,
          0.0, 0.0, 1.0]

vertices = np.array(vertices, dtype=np.float32)
colors = np.array(colors, dtype=np.float32)

glEnableClientState(GL_VERTEX_ARRAY)
glVertexPointer(3, GL_FLOAT, 0, vertices)

glEnableClientState(GL_COLOR_ARRAY)
glColorPointer(3, GL_FLOAT, 0, colors)


# Set the BG Color
glClearColor(0, 0.1, 0.1, 1)

# The main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    ct = glfw.get_time()  # returns the elapsed time, since init was called

    glLoadIdentity()
    glScale(abs(sin(ct)), abs(sin(ct)), 1)
    glRotatef(sin(ct) * 45, 0, 0, 1)
    glTranslatef(sin(ct), cos(ct), 0)

    glDrawArrays(GL_TRIANGLES, 0, 3)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated mem
glfw.terminate()
