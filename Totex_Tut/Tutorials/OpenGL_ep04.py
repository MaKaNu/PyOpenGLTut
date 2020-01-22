import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np


# Creates a Trinagle strip with the modern shader function pipeline

vertex_src = """
# version 400

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;

out vec3 v_color;

void main()
{
    gl_Position = vec4(a_position, 1.0);
    v_color = a_color;
}
"""

fragment_src = """
# version 400

in vec3 v_color;
out vec4 out_color;

void main()
{
    out_color = vec4(v_color, 1.0);
}
"""


# Window resize callback
def window_resize(window, width, height):
    glViewport(0, 0, width, height)


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

# Set window resize callback
glfw.set_window_size_callback(window, window_resize)

# make the context current
glfw.make_context_current(window)

# Print the version of OpenGL
print('The System Supports OpenGL Version: ' + str(glGetString(GL_VERSION)))

vertices = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            -0.5,  0.5, 0.0, 0.0, 0.0, 1.0,
            0.5,  0.5, 0.0, 1.0, 1.0, 1.0]

vertices = np.array(vertices, dtype=np.float32)

shader = compileProgram(
    compileShader(vertex_src, GL_VERTEX_SHADER),
    compileShader(fragment_src, GL_FRAGMENT_SHADER))

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Create Vertex Pointer using the layout location
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

# Create Vertex Color Pointer using the layout location
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

glUseProgram(shader)

# Set the BG Color
glClearColor(0, 0.1, 0.1, 1)

# The main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated mem
glfw.terminate()
