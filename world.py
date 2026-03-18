from settings import *
from world_objects.chunk import Chunk
from voxel_handler import VoxelHandler
from world_objects.mobs import MobManager


class World:
    def __init__(self, app):
        self.app = app
        self.chunks = [None for _ in range(WORLD_VOL)]
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype='uint8')
        self.build_chunks()
        self.build_chunk_mesh()
        self.voxel_handler = VoxelHandler(self)
        self.mob_manager = MobManager(self)
        self.daylight = 1.0

    def update(self):
        self.voxel_handler.update()
        self.mob_manager.update()
        self.daylight = MIN_DAYLIGHT + (1.0 - MIN_DAYLIGHT) * (0.5 + 0.5 * glm.sin(2.0 * glm.pi() * self.app.time / DAY_LENGTH_SEC))

    def build_chunks(self):
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    # put the chunk voxels in a separate array
                    self.voxels[chunk_index] = chunk.build_voxels()

                    # get pointer to voxels
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def render(self):
        for chunk in self.chunks:
            chunk.render()
        self.mob_manager.render()

    def get_voxel_id_at(self, x, y, z):
        wx, wy, wz = int(x), int(y), int(z)
        cx, cy, cz = wx // CHUNK_SIZE, wy // CHUNK_SIZE, wz // CHUNK_SIZE
        if not (0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D):
            return 0

        chunk_index = cx + WORLD_W * cz + WORLD_AREA * cy
        lx, ly, lz = wx % CHUNK_SIZE, wy % CHUNK_SIZE, wz % CHUNK_SIZE
        voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
        return int(self.voxels[chunk_index][voxel_index])

    def is_solid_at(self, x, y, z):
        return self.get_voxel_id_at(x, y, z) != 0
