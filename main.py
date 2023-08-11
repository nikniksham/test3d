import math
import time

import pygame


class Camera:
    def __init__(self):
        self.rot = [0, 0, 0]
        self.pos = [0, 0, 0]
        self.dist_to_canvas = 10  # дистанция, на которую прямоугольник проекции удалён от камеры
        self.canvas_size = [32, 18]
        self.screen_size = [1280, 720]

    def trans_points(self, point):
        point = [point[0] + self.pos[0], point[1] + self.pos[1], point[2] + self.pos[2]]
        point = self.rotate(point)
        return point

    def rotate(self, point):
        # matr = multiply_matrix(get_matrix_for_x(self.rot), get_matrix_for_y(self.rot))
        # matr = multiply_matrix(matr, get_matrix_for_z(self.rot))
        matr = multiply_matrix(get_matrix_for_y(self.rot), get_matrix_for_x(self.rot))
        matr = multiply_matrix(matr, get_matrix_for_z(self.rot))
        point = multiply_matrix(matr, [[point[0]], [point[1]], [point[2]]])
        point = [point[0][0], point[1][0], point[2][0]]
        return point

    def camera_rot_to_radian(self):
        return [self.rot[0] * math.pi / 180, self.rot[1] * math.pi / 180, self.rot[2] * math.pi / 180]

    def move(self, vel):
        # mx, my, mz = rot_mov
        #
        # z_mov = vel[0] * math.cos(my if abs(my) > abs(mz) else mz)
        # y_mov = vel[0] * math.sin(mx if abs(mx) > abs(mz) else mz)
        # x_mov = vel[0] * math.sin(mx if abs(mx) > abs(my) else my)
        # print(rot_mov)
        #
        # self.pos = [self.pos[0] + vel[0] * x_mov, self.pos[1] + y_mov,
        #             self.pos[2] + z_mov]
        mov = self.rotate(vel)
        # print(mov, self.rot)
        self.pos = [self.pos[0] + mov[2], self.pos[1] + mov[1], self.pos[2] + mov[0]]
        # time.sleep(0.1)


class Polygon:
    def __init__(self, p1, p2, p3, color=(255, 255, 255)):
        self.points = [p1, p2, p3]
        self.color = color
        self.bold = bool

    def draw(self, surface, camera, helper):
        draw_points = []
        draw_points2 = []
        for point in self.points:
            x, y, z = camera.trans_points(point)
            if z <= 0:
                continue
            point = [x * camera.dist_to_canvas / z, y * camera.dist_to_canvas / z, camera.dist_to_canvas]
            draw_points.append(point)
            draw_points2.append(helper.trans_point([point[0] * camera.screen_size[0]/camera.canvas_size[0], point[1] * camera.screen_size[1]/camera.canvas_size[1]]))
        if len(draw_points2) > 2:
            pygame.draw.polygon(surface, self.color, draw_points2)


class Line:
    def __init__(self, p1, p2, color=(255, 255, 255), bold=1):
        self.points = [p1, p2]
        self.color = color
        self.bold = bold

    def draw(self, surface, camera, helper):
        draw_points = []
        draw_points2 = []
        for point in self.points:
            x, y, z = camera.trans_points(point)
            if z <= 0:
                continue
            point = [x * camera.dist_to_canvas / z, y * camera.dist_to_canvas / z, camera.dist_to_canvas]
            draw_points.append(point)
            draw_points2.append(helper.trans_point([point[0] * camera.screen_size[0]/camera.canvas_size[0], point[1] * camera.screen_size[1]/camera.canvas_size[1]]))
        if len(draw_points2) > 1:
            pygame.draw.line(surface, self.color, draw_points2[0], draw_points2[1], self.bold)


class DrawHelper:
    def __init__(self, surface, camera):
        self.surface = surface
        self.camera = camera

    def trans_point(self, point):
        point = [point[0] + self.camera.screen_size[0]/2, self.camera.screen_size[1] - (point[1] + self.camera.screen_size[1]/2)]
        return point


def get_matrix_for_x(camera_rot):
    alpha, beta, gamma = camera_rot
    return [[math.cos(alpha), -math.sin(alpha), 0],
            [math.sin(alpha), math.cos(alpha), 0],
            [0, 0, 1]]


def get_matrix_for_y(camera_rot):
    alpha, beta, gamma = camera_rot
    return [[math.cos(beta), 0, -math.sin(beta)],
            [0, 1, 0],
            [math.sin(beta), 0, math.cos(beta)]]


def get_matrix_for_z(camera_rot):
    alpha, beta, gamma = camera_rot
    return [[1, 0, 0],
            [0, math.cos(gamma), -math.sin(gamma)],
            [0, math.sin(gamma), math.cos(gamma)]]


def multiply_matrix(matr1, matr2):
    result = []
    for row in matr1:
        new_row = []
        for ind_column in range(len(matr2[0])):
            new_row.append(sum([row[i] * matr2[i][ind_column] for i in range(len(row))]))
        result.append(new_row)
    return result

pygame.init()
display_surface = pygame.display.set_mode((1280, 720))

pygame.display.set_caption('3d')

testPoly = Polygon([-10, -10, 20], [10, -10, 20], [0, 10, 20])
camera = Camera()
helper = DrawHelper(display_surface, camera)

vAf = [-10, 10, 20]
vBf = [10, 10, 20]
vCf = [10, -10, 20]
vDf = [-10, -10, 20]

vAb = [-10, 10, 40]
vBb = [10, 10, 40]
vCb = [10, -10, 40]
vDb = [-10, -10, 40]

lines = [
    Line(vAf, vAb, (0, 255, 0)),
    Line(vBf, vBb, (0, 255, 0)),
    Line(vCf, vCb, (0, 255, 0)),
    Line(vDf, vDb, (0, 255, 0)),

    Line(vAb, vBb, (0, 0, 255)),
    Line(vAb, vDb, (0, 0, 255)),
    Line(vBb, vCb, (0, 0, 255)),
    Line(vCb, vDb, (0, 0, 255)),

    Line(vAf, vBf, (255, 0, 0)),
    Line(vAf, vDf, (255, 0, 0)),
    Line(vBf, vCf, (255, 0, 0)),
    Line(vCf, vDf, (255, 0, 0)),

    Line([-20, 0, 30], [20, 0, 30], (255, 0, 0), 3),
    Line([0, -20, 30], [0, 20, 30], (0, 255, 0), 3),
    Line([0, 0, 10], [0, 0, 50], (0, 0, 255), 3),
]

p0, p1 = (300, 300), (500, 300)
vel = [0, 0, 0]
rot = [0, 0, 0]

while True:
    display_surface.fill((0, 0, 0))

    testPoly.draw(display_surface, camera, helper)
    for line in lines:
        line.draw(display_surface, camera, helper)

    mov_rot = []
    for ro in camera.rot:
        ro %= (2 * math.pi)
        if ro > math.pi:
            ro -= math.pi * 2
        elif ro < -math.pi:
            ro += math.pi * 2
        mov_rot.append(ro)

    # print(camera.rot, mov_rot)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                vel[0] -= 0.01
            elif event.key == pygame.K_s:
                vel[0] += 0.01
            elif event.key == pygame.K_a:
                vel[2] += 0.01
            elif event.key == pygame.K_d:
                vel[2] -= 0.01

            # if event.key == pygame.K_a:
            #     vel[0] += 0.01
            # elif event.key == pygame.K_w:
            #     vel[1] -= 0.01
            # elif event.key == pygame.K_s:
            #     vel[1] += 0.01
            # elif event.key == pygame.K_d:
            #     vel[0] -= 0.01
            # elif event.key == pygame.K_q:
            #     vel[2] -= 0.01
            # elif event.key == pygame.K_e:
            #     vel[2] += 0.01
            #

            elif event.key == pygame.K_LEFT:
                rot[1] -= 0.001
            elif event.key == pygame.K_RIGHT:
                rot[1] += 0.001
            elif event.key == pygame.K_UP:
                # rot[2] -= math.cos(mov_rot[1]) * 0.001
                # rot[0] -= math.sin(mov_rot[1]) * 0.001
                rot[2] -= 0.001
                print(mov_rot, math.cos(mov_rot[1]), math.sin(mov_rot[1]))
            elif event.key == pygame.K_DOWN:
                rot[2] += 0.001
                # rot[2] += math.cos(mov_rot[1]) * 0.001
                # rot[0] += math.sin(mov_rot[1]) * 0.001
            elif event.key == pygame.K_r:
                rot[0] -= 0.001
            elif event.key == pygame.K_y:
                rot[0] += 0.001

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                vel[0] += 0.01
            elif event.key == pygame.K_s:
                vel[0] -= 0.01
            elif event.key == pygame.K_a:
                vel[2] -= 0.01
            elif event.key == pygame.K_d:
                vel[2] += 0.01

            # if event.key == pygame.K_a:
            #     vel[0] -= 0.01
            # elif event.key == pygame.K_d:
            #     vel[0] += 0.01
            # elif event.key == pygame.K_w:
            #     vel[1] += 0.01
            # elif event.key == pygame.K_s:
            #     vel[1] -= 0.01
            # elif event.key == pygame.K_q:
            #     vel[2] += 0.01
            # elif event.key == pygame.K_e:
            #     vel[2] -= 0.01
            #

            elif event.key == pygame.K_LEFT:
                rot[1] += 0.001
            elif event.key == pygame.K_RIGHT:
                rot[1] -= 0.001
            elif event.key == pygame.K_UP:
                rot[2] += 0.001
                # rot[2] += math.cos(mov_rot[1]) * 0.001
                # rot[0] += math.sin(mov_rot[1]) * 0.001
            elif event.key == pygame.K_DOWN:
                rot[2] -= 0.001
                # rot[2] -= math.cos(mov_rot[1]) * 0.001
                # rot[0] -= math.sin(mov_rot[1]) * 0.001
            elif event.key == pygame.K_r:
                rot[0] += 0.001
            elif event.key == pygame.K_y:
                rot[0] -= 0.001

    # print(rot)


    # camera.pos = [camera.pos[0] + vel[0], camera.pos[1] + vel[1], camera.pos[2] + vel[2]]
    camera.rot = [camera.rot[0] + rot[0], camera.rot[1] + rot[1], camera.rot[2] + rot[2]]
    print(camera.rot)
    # camera.rot = [0, camera.rot[1] + rot[1], camera.rot[2] + rot[2]]

    camera.move(vel)
    # print(camera.rot)
    # if pygame.mouse.get_pressed(3)[0]:
    #     camera.dist_to_canvas += 0.01
    # elif pygame.mouse.get_pressed(3)[2] and camera.dist_to_canvas > 0:
    #     camera.dist_to_canvas -= 0.01

    pygame.display.update()
