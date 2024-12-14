"""
This module contains classes and functions for rendering 3D graphics.
It includes the cube class, which is used to render a simple triangle and a simple cube.
"""
import numpy as np
import glm
import pygame as pg


class Triangle:
    """
    A simple triangle object that is rendered using a vertex array and a simple
    shader program.
    """

    def __init__(self, app):
        """
        Initialize the triangle object.

        Parameters
        ----------
        app : GraphicsEngine
            The graphics engine that is used to render the triangle.
        """
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()

    def render(self):
        """
        Render the triangle.
        """
        self.vao.render()

    def destroy(self):
        """
        Clean up after the triangle object is no longer needed.
        """
        self.vao.release()
        self.vbo.release()
        self.shader_program.release()

    def get_vao(self):
        """
        Create a vertex array object.

        Returns
        -------
        vao : mgl.VertexArray
            The vertex array object.
        """
        vao = self.ctx.vertex_array(
            self.shader_program, [(self.vbo, '3f', 'in_position')])
        return vao

    def get_vertex_data(self):
        """
        Get the vertex data for the triangle.

        Returns
        -------
        vertex_data : numpy.ndarray
            The vertex data, which is a 3D array of floats.
        """
        vertex_data = [(-0.5, -0.5, 0), (0.5, -0.5, 0), (0, 0.5, 0)]
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data

    def get_vbo(self):
        """
        Create a vertex buffer object.

        Returns
        -------
        vbo : mgl.Buffer
            The vertex buffer object.
        """
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        """
        Load and compile a shader program.

        Parameters
        ----------
        shader_name : str
            The name of the shader program.

        Returns
        -------
        program : mgl.Program
            The shader program.
        """
        with open(f'shaders/{shader_name}.vert', 'rt', encoding='utf-8') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag', 'rt', encoding='utf-8') as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
        return program


class Cube:
    """
    A simple cube object that is rendered using a vertex array and a simple
    """

    def __init__(self, app):
        """
        Initialize the cube object.

        Parameters
        ----------
        app : GraphicsEngine
            The graphics engine that is used to render the cube.
        """
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture(path='textures/stone.jpg')
        self.on_init()

    def get_texture(self, path):
        """
        Get the texture for the cube.

        Returns
        -------
        texture : mgl.Texture
            The texture.
        """
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(
        ), components=3, data=pg.image.tostring(texture, 'RGB'))
        return texture

    def update(self):
        """
        Update the cube object.
        """
        m_model = glm.rotate(self.m_model, self.app.time, glm.vec3(0, 1, 0))
        self.shader_program['m_model'].write(m_model)

    def get_model_matrix(self):
        """
        Get the model matrix for the cube.

        Returns
        -------
        model_matrix : numpy.ndarray
            The model matrix, which is a 4x4 array of floats.
        """
        model_matrix = glm.mat4()
        return model_matrix

    def on_init(self):
        """
        Initialize the cube object.
        """
        self.shader_program['u_texture_0'] = 0
        self.texture.use()
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)

    def render(self):
        """
        Render the cube.
        """
        self.update()
        self.vao.render()

    def destroy(self):
        """
        Clean up after the cube object is no longer needed.
        """
        self.vao.release()
        self.vbo.release()
        self.shader_program.release()

    def get_vao(self):
        """
        Create a vertex array object.

        Returns
        -------
        vao : mgl.VertexArray
            The vertex array object.
        """
        vao = self.ctx.vertex_array(
            self.shader_program, [(self.vbo, '2f 3f', 'in_texcoord_0', 'in_position')])
        return vao

    def get_vertex_data(self):
        """
        Get the vertex data for the cube.

        Returns
        -------
        vertex_data : numpy.ndarray
            The vertex data, which is a 3D array of floats.
        """
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        indices = [(0, 2, 3), (0, 1, 2), (1, 7, 2),
                   (1, 6, 7), (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0), (3, 7, 4),
                   (3, 2, 7), (0, 6, 1), (0, 5, 7)]

        text_cord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        text_cord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]

        text_cord_data = self.get_data(text_cord, text_cord_indices)
        vertex_data = self.get_data(vertices, indices)
        vertex_data = np.hstack((text_cord_data, vertex_data))
        return vertex_data

    @staticmethod
    def get_data(vertices, indices):
        """
        Get the vertex data for the cube.

        Returns
        -------
        vertex_data : numpy.ndarray
            The vertex data, which is a 3D array of floats.
        """
        data = [vertices[i] for triangle in indices for i in triangle]
        return np.array(data, dtype='f4')

    def get_vbo(self):
        """
        Create a vertex buffer object.

        Returns
        -------
        vbo : mgl.Buffer
            The vertex buffer object.
        """
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        """
        Load and compile a shader program.

        Parameters
        ----------
        shader_name : str
            The name of the shader program.

        Returns
        -------
        program : mgl.Program
            The shader program.
        """
        with open(f'shaders/{shader_name}.vert', 'rt', encoding='utf-8') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag', 'rt', encoding='utf-8') as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
        return program
