import glfw

# Initialize GLFW Lib
if not glfw.init():
    raise Exception("GLFW can not be initialzed!")

# Create a Window
window = glfw.create_window(1920, 1080, "My OpenGL Window", None, None)

# Check if Window is created
if not window:
    glfw.terminate()
    raise Exception("GLFW window can not be created!")

# set Window Position
glfw.set_window_pos(window, 0, 0)

# make the context current
glfw.make_context_current(window)

# The main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glfw.swap_buffers(window)

# terminate glfw, free up allocated mem
glfw.terminate()
