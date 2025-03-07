"""
This module contains the main entry point for the graphics engine.
It defines the GraphicsEngine class and initializes the Pygame library.
"""
# pylint: disable=no-member
import sys
import pygame as pg
import moderngl as mgl
from scene import Scene
from camera import Camera
from light import Light
from mesh import Mesh


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
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        self.ctx = mgl.create_context()
        # self.ctx.front_face = 'cw'
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.clock = pg.time.Clock()
        self.light = Light()
        self.mesh = Mesh(self)
        self.camera = Camera(self)
        self.scene = Scene(self)
        self.time = 0
        self.delta_time = 0

    def check_events(self):
        """
        This method processes all Pygame events (e.g. closing the window)
        and exits the program if necessary.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                # self.scene.destroy()
                self.mesh.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        """
        This method clears the screen and swaps the buffers to display the rendered scene.
        """
        self.ctx.clear(color=(0.1, 0.1, 0.2))
        self.scene.render()
        pg.display.flip()

    def get_time(self):
        """
        Get the current time since the Pygame initialization.

        Returns
        -------
        float
            The current time in seconds.
        """
        self.time = pg.time.get_ticks() * 0.001
        return self.time

    def run(self):
        """
        This method runs the main loop of the graphics engine.
        It checks for events and renders the scene on each iteration.
        """
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)


if __name__ == "__main__":
    app = GraphicsEngine()
    app.run()
