import pygame as pg
import random
import math
import time

pg.init()

clock = pg.time.Clock()

sw = 1280  # 16/9 aspect ration i think
sh = 720
sc = (sw / 2, sh / 2)
screen_color = (34, 137, 134)

pg.display.set_caption("3D")
win = pg.display.set_mode((sw, sh))
win.fill(screen_color)


def pythag(vec_in):
    total = 0
    for i in vec_in:
        total += i * i

    return math.sqrt(total)


class Camera(object):
    def __init__(self):
        self.field_of_view = math.cos(math.radians(35))
        # fov = 35 degrees / distance from top to middle of screen is 35 degrees
        # i might need to change it to 102.4/2 degrees because i have 9/16 aspect ratio
        # this is because if vertical total degrees is 70, horizontal total degrees is 102.4 i think
        self.location = [0, -30, 0]
        self.pointing_vec = [0, 0, 1]
        self.angle_x = 0
        self.angle_y = 0
        self.angles_to_pointing_vec()
        self.quads_to_draw = []
        self.moving_forward = False
        self.moving_back = False
        self.moving_left = False
        self.moving_right = False

    def angles_to_pointing_vec(self):
        self.pointing_vec[1] = math.sin(math.radians(self.angle_y))
        second_circle_radius = math.cos(math.radians(self.angle_y))
        self.pointing_vec[0] = math.cos(math.radians(self.angle_x)) * second_circle_radius
        self.pointing_vec[2] = math.sin(math.radians(self.angle_x)) * second_circle_radius

        if not pythag(self.pointing_vec) == 1 and False:  # i think this if is irrelevant now
            crash = 0
            print("crash")
            print(self.pointing_vec)
            print(pythag(self.pointing_vec))
            print(1 / crash)

    def movement(self):
        did_i_move = False
        if self.moving_forward:
            self.location[0] += math.cos(math.radians(self.angle_x))
            self.location[2] += math.sin(math.radians(self.angle_x))
            did_i_move = True

        return did_i_move

    def draw(self, win):
        for i in self.quads_to_draw:
            pg.draw.polygon(win, (50, 100, 200), i, 1)


class Cube(object):
    def __init__(self, center):
        self.center = center
        self.side = 20
        self.close_sides = []
        self.three_d_poss = []
        self.two_d_poss = []
        self.get_3d_positions()

    def get_3d_positions(self):
        self.corner1_3d = (
            self.center[0] - self.side / 2, self.center[1] - self.side / 2, self.center[2] + self.side / 2)

        self.corner2_3d = (
            self.center[0] - self.side / 2, self.center[1] + self.side / 2, self.center[2] + self.side / 2)

        self.corner3_3d = (
            self.center[0] + self.side / 2, self.center[1] - self.side / 2, self.center[2] + self.side / 2)

        self.corner4_3d = (
            self.center[0] + self.side / 2, self.center[1] + self.side / 2, self.center[2] + self.side / 2)

        self.corner5_3d = (
            self.center[0] - self.side / 2, self.center[1] - self.side / 2, self.center[2] - self.side / 2)

        self.corner6_3d = (
            self.center[0] - self.side / 2, self.center[1] + self.side / 2, self.center[2] - self.side / 2)

        self.corner7_3d = (
            self.center[0] + self.side / 2, self.center[1] - self.side / 2, self.center[2] - self.side / 2)

        self.corner8_3d = (
            self.center[0] + self.side / 2, self.center[1] + self.side / 2, self.center[2] - self.side / 2)

        self.three_d_poss = [self.corner1_3d, self.corner2_3d, self.corner3_3d, self.corner4_3d, self.corner5_3d,
                             self.corner6_3d, self.corner7_3d, self.corner8_3d]

    def get_3_closest_sides(self, camera_location):

        close_corner = self.get_closest_corner(camera_location)

        self.close_sides = []

        for i in [(1, 3, 4, 2), (5, 7, 8, 6), (1, 5, 7, 3), (6, 2, 4, 8), (5, 6, 2, 1), (4, 3, 7, 8)]:
            if not self.contains(i, close_corner):
                self.close_sides.append(i)

    def get_closest_corner(self, camera_location):
        closest_corner = 1
        corner_distance = pythag(
            (self.three_d_poss[0][0] - camera_location[0], self.three_d_poss[0][1] - camera_location[1],
             self.three_d_poss[0][2] - camera_location[2]))
        counter = 1
        for i in self.three_d_poss:
            i_minus_camera_location = (i[0] - camera_location[0], i[1] - camera_location[1], i[2] - camera_location[2])
            math_stfz = pythag(i_minus_camera_location)
            if math_stfz <= corner_distance:
                closest_corner = counter
                corner_distance = math_stfz
            counter += 1
        return closest_corner

    def contains(self, vec_in, item_to_check_for):
        for i in vec_in:
            if i == item_to_check_for:
                return True

        return False

    def i_moved(self, camera_pointing, camera_location):
        self.get_3_closest_sides(camera_location)
        self.get_slope_and_degrees(camera_pointing, camera_location)

        quads_to_return = []

        # for i in self.close_sides:  set it to this later
        for i in [(1, 3, 4, 2), (5, 7, 8, 6), (1, 5, 7, 3), (6, 2, 4, 8), (5, 6, 2, 1), (4, 3, 7, 8)]:
            quads_to_return.append((self.two_d_poss[i[0] - 1], self.two_d_poss[i[1] - 1], self.two_d_poss[i[2] - 1],
                                    self.two_d_poss[i[3] - 1]))

        return quads_to_return

    def get_slope_and_degrees(self, camera_pointing, camera_location):
        self.two_d_poss = []
        for i in self.three_d_poss:
            s = (i[0] - camera_location[0], i[1] - camera_location[1], i[2] - camera_location[2])
            v = camera_pointing
            v_s_dot_product = s[0] * v[0] + s[1] * v[1] + s[2] * v[2]
            h_div_by_v = v_s_dot_product / (pythag(v) ** 2)
            h = (v[0] * h_div_by_v, v[1] * h_div_by_v, v[2] * h_div_by_v)
            s_from_h = (s[0] - h[0], s[1] - h[1], s[2] - h[2])
            u_x = -1 * v[2]
            u_y = 0
            u_z = v[0]
            u_from_h = (u_x, u_y, u_z)
            cos_angle_uhs_top = u_from_h[0] * s_from_h[0] + u_from_h[1] * s_from_h[1] + u_from_h[2] * s_from_h[2]
            cos_angle_uhs_bottom = pythag(u_from_h) * pythag(s_from_h)
            cos_angle_uhs = cos_angle_uhs_top / cos_angle_uhs_bottom
            angle_uhs = math.acos(cos_angle_uhs)
            slope = [cos_angle_uhs, math.sin(angle_uhs)]
            angle_vos = math.acos(v_s_dot_product / (pythag(v) * pythag(s)))
            return_x = angle_vos / math.sqrt(1 + ((slope[1] / slope[0]) ** 2))
            return_y = return_x * abs((slope[1] / slope[0]))

            #   this is where i need to do fov and stuff

            if slope[0] < 0:
                return_x *= -1

            if h[1] > s[1]:
                return_y *= -1

            scale_or_fov = 740

            return_y *= scale_or_fov
            return_x *= scale_or_fov

            if v_s_dot_product < 0:
                self.two_d_poss.append((sw / 2, 3000))  # fix this later
            else:
                self.two_d_poss.append((return_x + (sw / 2), return_y + (sh / 2)))

            # oh no i might need to convert stuff between radians and degrees maybe not tho
            # can i treat them the same?


def redraw_game_window():
    win.fill(screen_color)

    camera.draw(win)

    pg.draw.circle(win, (56, 85, 142), (sw / 2, sh / 2), 2)

    pg.display.update()


cubes = []

# cubes.append(Cube((150, 0, -20)))
# cubes.append(Cube((150, 0, 0)))
# cubes.append(Cube((150, 0, 20)))
# cubes.append(Cube((150, 20, 0)))
# cubes.append(Cube((150, -20, 0)))
# cubes.append(Cube((0, 200, 850)))
# cubes.append(Cube((200, 0, 350)))

for i in range(10):
    for ii in range(10):
        cubes.append(Cube((i * 20, 0, ii * 20)))

camera = Camera()


def camera_moved():
    camera.angles_to_pointing_vec()

    vec_contains_quadrilateral = []
    for i in cubes:
        vec_contains_quadrilateral += i.i_moved(camera.pointing_vec, camera.location)

    camera.quads_to_draw = vec_contains_quadrilateral


camera_moved()

running = True
while running:

    clock.tick(60)

    did_camera_move = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEMOTION:
            mouse_cords = ((pg.mouse.get_pos()[0] - sw / 2), pg.mouse.get_pos()[1] - sh / 2)
            camera.angle_y = (mouse_cords[1] / (sh / 2)) * 90
            camera.angle_x = (mouse_cords[0] / (sw / 2)) * 160 + .01  # if it is 0 it crashes so i added .01
            did_camera_move = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                camera.moving_forward = True

        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                camera.moving_forward = False

    if camera.movement():
        did_camera_move = True

    if did_camera_move:
        camera_moved()

    redraw_game_window()
