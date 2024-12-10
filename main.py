"""
This module contains the main entry point for the graphics engine.
It defines the GraphicsEngine class and initializes the Pygame library.
"""
# pylint: disable=no-member
import sys
import pygame as pg
import moderngl as mgl


class GraphicsEngine:
    """
    This class serves as the main entry point for the graphics engine.
    It initializes the Pygame library and creates a ModernGL context.
    """

    def __init__(self, win_size=(1600, 900)):

        pg.init()
        self.win_size = win_size
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.win_size, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()
        self.clock = pg.time.Clock()

    def check_events(self):
        """
        This method processes all Pygame events (e.g. closing the window)
        and exits the program if necessary.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def render(self):
        """
        This method clears the screen and swaps the buffers to display the rendered scene.
        """
        self.ctx.clear(color=(0.1, 0.1, 0.2))
        pg.display.flip()

    def run(self):
        """
        This method runs the main loop of the graphics engine.
        It checks for events and renders the scene on each iteration.
        """
        while True:
            self.check_events()
            self.render()
            self.clock.tick(60)


if __name__ == "__main__":
    app = GraphicsEngine()
    app.run()
