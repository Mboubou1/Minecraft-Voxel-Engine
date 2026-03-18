from numba import njit
import numpy as np
import glm
import math

# OpenGL settings
MAJOR_VER, MINOR_VER = 3, 3
DEPTH_SIZE = 24
NUM_SAMPLES = 1  # antialiasing

# resolution
WIN_RES = glm.vec2(720, 480)

# world generation
SEED = 16

# ray casting
MAX_RAY_DIST = 6

# chunk
CHUNK_SIZE = 48
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE
CHUNK_SPHERE_RADIUS = H_CHUNK_SIZE * math.sqrt(3)

# world
WORLD_W, WORLD_H = 20, 2
WORLD_D = WORLD_W
WORLD_AREA = WORLD_W * WORLD_D
WORLD_VOL = WORLD_AREA * WORLD_H

# world center
CENTER_XZ = WORLD_W * H_CHUNK_SIZE
CENTER_Y = WORLD_H * H_CHUNK_SIZE

# camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 50
V_FOV = glm.radians(FOV_DEG)  # vertical FOV
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)  # horizontal FOV
NEAR = 0.1
FAR = 2000.0
PITCH_MAX = glm.radians(89)

# player
PLAYER_SPEED = 0.005
PLAYER_ROT_SPEED = 0.003
PLAYER_POS = glm.vec3(CENTER_XZ, CHUNK_SIZE, CENTER_XZ)
MOUSE_SENSITIVITY = 0.002
PLAYER_WIDTH = 0.35
PLAYER_HEIGHT = 1.8
GRAVITY = 0.0025
JUMP_SPEED = 0.055
MAX_FALL_SPEED = 0.09
PLAYER_MAX_HEALTH = 20

# colors
BG_COLOR = glm.vec3(0.58, 0.83, 0.99)

# textures / blocks
SAND = 1
GRASS = 2
DIRT = 3
STONE = 4
SNOW = 5
LEAVES = 6
WOOD = 7

# extra block ids (rendered by reusing texture-array layers)
COBBLESTONE = 8
PLANKS = 9
BRICK = 10
CLAY = 11
GLOWSTONE = 12

INVENTORY_BLOCK_IDS = [
    GRASS, DIRT, STONE, SAND, SNOW, LEAVES, WOOD,
    COBBLESTONE, PLANKS, BRICK, CLAY, GLOWSTONE,
]

BLOCK_NAMES = {
    GRASS: 'Herbe',
    DIRT: 'Terre',
    STONE: 'Pierre',
    SAND: 'Sable',
    SNOW: 'Neige',
    LEAVES: 'Feuilles',
    WOOD: 'Bois',
    COBBLESTONE: 'Pierre taillée',
    PLANKS: 'Planches',
    BRICK: 'Briques',
    CLAY: 'Argile',
    GLOWSTONE: 'Pierre lumineuse',
}

# terrain levels
SNOW_LVL = 54
STONE_LVL = 49
DIRT_LVL = 40
GRASS_LVL = 8
SAND_LVL = 7

# biomes
BIOME_PLAINS = 0
BIOME_DESERT = 1
BIOME_MOUNTAINS = 2
BIOME_SNOW = 3
BIOME_SWAMP = 4

# tree settings
TREE_PROBABILITY = 0.02
TREE_WIDTH, TREE_HEIGHT = 4, 8
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2

# day/night and lighting
DAY_LENGTH_SEC = 180.0
MIN_DAYLIGHT = 0.2

# water
WATER_LINE = 5.6
WATER_AREA = 5 * CHUNK_SIZE * WORLD_W

# cloud
CLOUD_SCALE = 25
CLOUD_HEIGHT = WORLD_H * CHUNK_SIZE * 2

# mobs
MOB_COUNT_PASSIVE = 8
MOB_COUNT_HOSTILE = 6
MOB_SPEED_PASSIVE = 0.01
MOB_SPEED_HOSTILE = 0.013
MOB_DAMAGE = 2
MOB_ATTACK_COOLDOWN = 1.2
MOB_DESPAWN_DIST = CHUNK_SIZE * 2
