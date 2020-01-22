import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr


# Creates a rotating 3D cube

vertex_src = """
# version 400

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;

uniform mat4 rotation;

out vec3 v_color;

void main()
{
    gl_Position = rotation * vec4(a_position, 1.0);
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

vertices = [-0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
            0.5,  0.5, 0.5, 0.0, 0.0, 1.0,
            -0.5,  0.5, 0.5, 1.0, 1.0, 1.0,

            -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
            0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
            0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
            -0.5,  0.5, -0.5, 1.0, 1.0, 1.0]

indices = [0, 1, 2, 2, 3, 0,    # Frontplate
           4, 5, 6, 6, 7, 4,    # Backplate
           4, 5, 1, 1, 0, 4,    # Lowerplate
           6, 7, 3, 3, 2, 6,    # Upperplate
           5, 6, 2, 2, 1, 5,    # Rightplate
           7, 4, 0, 0, 3, 7]    # Leftplate

vertices = np.array(vertices, dtype=np.float32)

indices = np.array(indices, dtype=np.uint32)

shader = compileProgram(
    compileShader(vertex_src, GL_VERTEX_SHADER),
    compileShader(fragment_src, GL_FRAGMENT_SHADER))

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

# Create Vertex Pointer using the layout location
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

# Create Vertex Color Pointer using the layout location
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

glUseProgram(shader)

# Set the BG Color
glClearColor(0, 0.1, 0.1, 1)

glEnable(GL_DEPTH_TEST)

rotation_location = glGetUniformLocation(shader, "rotation")

# The main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())

    glUniformMatrix4fv(rotation_location,
                       1,
                       GL_FALSE,
                       pyrr.matrix44.multiply(rot_x, rot_y))

    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated mem
glfw.terminate()
