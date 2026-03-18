import pygame as pg
import glm
from camera import Camera
from settings import *


class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app
        super().__init__(position, yaw, pitch)
        self.velocity_y = 0.0
        self.on_ground = False
        self.noclip = False
        self.in_water = False
        self.health = PLAYER_MAX_HEALTH
        self._prev_position = glm.vec3(self.position)

    def update(self):
        self._prev_position = glm.vec3(self.position)
        self.keyboard_control()
        self.mouse_control()
        self.apply_physics()
        super().update()

    def handle_event(self, event):
        voxel_handler = self.app.scene.world.voxel_handler

        # adding and removing voxels with clicks
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                voxel_handler.set_voxel()
            if event.button == 3:
                voxel_handler.switch_mode()
            if event.button == 4:
                voxel_handler.cycle_inventory(1)
            if event.button == 5:
                voxel_handler.cycle_inventory(-1)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_f:
                self.noclip = not self.noclip

            number_keys = {
                pg.K_1: 0, pg.K_2: 1, pg.K_3: 2, pg.K_4: 3, pg.K_5: 4,
                pg.K_6: 5, pg.K_7: 6, pg.K_8: 7, pg.K_9: 8,
            }
            if event.key in number_keys:
                voxel_handler.set_inventory_slot(number_keys[event.key])

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time * (0.55 if self.in_water and not self.noclip else 1.0)

        flat_forward = glm.normalize(glm.vec3(self.forward.x, 0, self.forward.z))
        flat_right = glm.normalize(glm.vec3(self.right.x, 0, self.right.z))

        if key_state[pg.K_z]:
            self.position += flat_forward * vel
        if key_state[pg.K_s]:
            self.position -= flat_forward * vel
        if key_state[pg.K_d]:
            self.position += flat_right * vel
        if key_state[pg.K_q]:
            self.position -= flat_right * vel

        if self.noclip:
            if key_state[pg.K_a]:
                self.move_up(vel)
            if key_state[pg.K_e]:
                self.move_down(vel)
        elif key_state[pg.K_SPACE]:
            if self.on_ground:
                self.velocity_y = JUMP_SPEED
                self.on_ground = False
            elif self.in_water:
                self.velocity_y = max(self.velocity_y, WATER_SWIM_UP_SPEED)

    def collides(self, position):
        world = self.app.scene.world
        px, py, pz = position

        skin = 0.03
        min_x = px - PLAYER_WIDTH + skin
        max_x = px + PLAYER_WIDTH - skin
        min_y = py + skin
        max_y = py + PLAYER_HEIGHT - skin
        min_z = pz - PLAYER_WIDTH + skin
        max_z = pz + PLAYER_WIDTH - skin

        for x in (min_x, max_x):
            for y in (min_y, max_y):
                for z in (min_z, max_z):
                    if world.is_solid_at(x, y, z):
                        return True
        return False

    def _update_water_state(self):
        feet_y = self.position.y + 0.05
        chest_y = self.position.y + PLAYER_HEIGHT * 0.6
        below_surface = chest_y < WATER_LINE
        self.in_water = below_surface and not self.app.scene.world.is_solid_at(
            self.position.x, feet_y, self.position.z
        )

    def apply_physics(self):
        if self.noclip:
            self.velocity_y = 0.0
            self.on_ground = False
            self.in_water = False
            return

        old_pos = glm.vec3(self._prev_position)
        self._update_water_state()

        # Horizontal collision separation
        test_x = glm.vec3(self.position.x, old_pos.y, old_pos.z)
        if self.collides(test_x):
            self.position.x = old_pos.x

        test_z = glm.vec3(self.position.x, old_pos.y, self.position.z)
        if self.collides(test_z):
            self.position.z = old_pos.z

        gravity = GRAVITY_WATER if self.in_water else GRAVITY
        max_fall = MAX_FALL_SPEED_WATER if self.in_water else MAX_FALL_SPEED
        self.velocity_y = max(self.velocity_y - gravity * self.app.delta_time, -max_fall)
        self.position.y += self.velocity_y

        if self.collides(self.position):
            if self.velocity_y < 0:
                self.on_ground = True
            self.position.y = old_pos.y
            self.velocity_y = 0.0
        else:
            self.on_ground = False
