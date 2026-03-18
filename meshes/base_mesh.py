import numpy as np


class BaseMesh:
    def __init__(self):
        # OpenGL context
        self.ctx = None
        # shader program
        self.program = None
        # vertex buffer data type format: "3f 3f"
        self.vbo_format = None
        # attribute names according to the format: ("in_position", "in_color")
        self.attrs: tuple[str, ...] = None
        # vertex array object
        self.vao = None

    def get_vertex_data(self) -> np.array: ...

    def get_vao(self):
        vertex_data = self.get_vertex_data()
        if vertex_data is None:
            return None

        if isinstance(vertex_data, np.ndarray):
            if vertex_data.size == 0 or vertex_data.nbytes == 0:
                return None
        elif hasattr(vertex_data, "__len__") and len(vertex_data) == 0:
            return None

        vbo = self.ctx.buffer(vertex_data)
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vbo_format, *self.attrs)], skip_errors=True
        )
        return vao

    def render(self):
        if self.vao is not None:
            self.vao.render()
