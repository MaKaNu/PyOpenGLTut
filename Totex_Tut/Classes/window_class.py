import glfw


class Window:
    def __init__(self, width: int, height: int, title: str):
        # Initialize GLFW Lib
        if not glfw.init():
            raise Exception("GLFW can not be initialzed!")

        # Create a Window
        self._window = glfw.create_window(width, height, title, None, None)

        # Check if Window is created
        if not self._window:
            glfw.terminate()
            raise Exception("GLFW window can not be created!")

        # set Window Position
        glfw.set_window_pos(self._window, 400, 200)

        # make the context current
        glfw.make_context_current(self._window)

    def main_loop(self):
        # The main application loop
        while not glfw.window_should_close(self._window):
            glfw.poll_events()

            glfw.swap_buffers(self._window)

        # terminate glfw, free up allocated mem
        glfw.terminate()


if __name__ == "__main__":
    win = Window(1280, 720, "My OpenGL window")
    win.main_loop
