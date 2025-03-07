from model import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def addObject(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.addObject
        n, s = 80, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, -s, z)))

        add(Cat(app, pos=(0, -1, -10)))

    def render(self):
        for obj in self.objects:
            obj.render()
