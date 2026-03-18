import random
import glm
from settings import *
from meshes.cube_mesh import CubeMesh


class Mob:
    def __init__(self, world, hostile=False, position=None):
        self.world = world
        self.app = world.app
        self.hostile = hostile
        self.position = glm.vec3(position) if position is not None else self._spawn_position()
        self.velocity_y = 0.0
        self.direction = glm.normalize(glm.vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)))
        self.target_timer = random.uniform(1.0, 4.0)
        self.attack_timer = 0.0

    def _spawn_position(self):
        base = self.app.player.position
        radius = random.uniform(10.0, 28.0)
        angle = random.uniform(0.0, 6.28)
        x = base.x + glm.cos(angle) * radius
        z = base.z + glm.sin(angle) * radius
        for y in range(CHUNK_SIZE * WORLD_H - 2, 2, -1):
            if self.world.is_solid_at(x, y, z):
                return glm.vec3(x, y + 1.05, z)
        return glm.vec3(base.x + 6.0, WATER_LINE + 2, base.z + 6.0)

    def _update_direction(self, dt):
        self.target_timer -= dt
        if self.target_timer <= 0:
            self.target_timer = random.uniform(1.0, 4.0)
            self.direction = glm.normalize(glm.vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)))

        if self.hostile:
            to_player = self.app.player.position - self.position
            dist = glm.length(to_player)
            if dist < 18.0 and dist > 0.001:
                self.direction = glm.normalize(glm.vec3(to_player.x, 0, to_player.z))

    def _move_horizontal(self, dt):
        speed = MOB_SPEED_HOSTILE if self.hostile else MOB_SPEED_PASSIVE
        move = self.direction * speed * self.app.delta_time
        candidate = self.position + move
        if not self.world.is_solid_at(candidate.x, self.position.y, candidate.z):
            self.position = candidate

    def _apply_gravity(self):
        self.velocity_y = max(self.velocity_y - GRAVITY * self.app.delta_time, -MAX_FALL_SPEED)
        candidate_y = self.position.y + self.velocity_y

        if self.velocity_y < 0 and self.world.is_solid_at(self.position.x, candidate_y - 1.0, self.position.z):
            self.position.y = int(candidate_y)
            self.velocity_y = 0.0
        else:
            self.position.y = candidate_y

    def _attack_player(self, dt):
        if not self.hostile:
            return
        self.attack_timer -= dt
        if self.attack_timer > 0:
            return

        dist = glm.length(self.app.player.position - self.position)
        if dist < 1.5:
            self.attack_timer = MOB_ATTACK_COOLDOWN
            self.app.player.health = max(0, self.app.player.health - MOB_DAMAGE)

    def update(self, dt):
        self._update_direction(dt)
        self._move_horizontal(dt)
        self._apply_gravity()
        self._attack_player(dt)


class MobManager:
    def __init__(self, world):
        self.world = world
        self.app = world.app
        self.mesh = CubeMesh(self.app)
        self.mobs = []
        self._spawn_initial_mobs()

    def _spawn_initial_mobs(self):
        for _ in range(MOB_COUNT_PASSIVE):
            self.mobs.append(Mob(self.world, hostile=False))
        for _ in range(MOB_COUNT_HOSTILE):
            self.mobs.append(Mob(self.world, hostile=True))

    def _despawn_and_respawn(self):
        player_pos = self.app.player.position
        kept = []
        for mob in self.mobs:
            if glm.length(mob.position - player_pos) < MOB_DESPAWN_DIST:
                kept.append(mob)
        self.mobs = kept

        while len([m for m in self.mobs if not m.hostile]) < MOB_COUNT_PASSIVE:
            self.mobs.append(Mob(self.world, hostile=False))
        while len([m for m in self.mobs if m.hostile]) < MOB_COUNT_HOSTILE:
            self.mobs.append(Mob(self.world, hostile=True))

    def update(self):
        dt = max(0.001, self.app.delta_time * 0.001)
        for mob in self.mobs:
            mob.update(dt)
        self._despawn_and_respawn()

    def render(self):
        program = self.mesh.program
        for mob in self.mobs:
            program['mode_id'] = 1 if mob.hostile else 0
            m_model = glm.translate(glm.mat4(), mob.position)
            m_model = glm.scale(m_model, glm.vec3(0.8, 1.2, 0.8))
            program['m_model'].write(m_model)
            self.mesh.render()
