# pylint: disable=no-member
import pygame as pg
import moderngl as mgl
import glm


class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/stone.jpg')
        self.textures[1] = self.get_texture(path='textures/stone.jpg')
        self.textures[2] = self.get_texture(path='textures/stone.jpg')
        self.textures['cat'] = self.get_texture(
            path='objects/cat/20430_cat_diff_v1.jpg')

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
