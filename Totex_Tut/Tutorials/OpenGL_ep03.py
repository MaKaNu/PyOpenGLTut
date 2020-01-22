import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np


# Creates a Trinagle with the modern shader function pipeline (deprecated)

vertex_src = """
# version 400

in vec3 a_position;
in vec3 a_color;

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

# Print the version of OpenGL
print('The System Supports OpenGL Version: ' + str(glGetString(GL_VERSION)))

# Create Vertices (x, y, z, r, g, b)
vertices = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            0.0,  0.5, 0.0, 0.0, 0.0, 1.0]

vertices = np.array(vertices, dtype=np.float32)

# Create shader Programm
shader = compileProgram(
    compileShader(vertex_src, GL_VERTEX_SHADER),
    compileShader(fragment_src, GL_FRAGMENT_SHADER))

# Create Vertex Buffer Object with one Buffer
VBO = glGenBuffers(1)
# Bind the OpenGLArraybuffer to the VBO
glBindBuffer(GL_ARRAY_BUFFER, VBO)
# Send the Data    target          datasize     data        Usage
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Create Vertex Pointer using the shader programm
position = glGetAttribLocation(shader, "a_position")
glEnableVertexAttribArray(position)
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

# Create Vertex Color Pointer using the shader programm
color = glGetAttribLocation(shader, "a_color")
glEnableVertexAttribArray(color)
glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

glUseProgram(shader)

# Set the BG Color
glClearColor(0, 0.1, 0.1, 1)

# The main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    glDrawArrays(GL_TRIANGLES, 0, 3)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated mem
glfw.terminate()
