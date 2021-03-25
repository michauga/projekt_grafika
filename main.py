import pygame
import os
import math
from matrix_multiplication import matrix_multiplication

os.environ["SDL_VIDEO_CENTERED"] = '1'
black, white, red, green, blue = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)
width, height = 1920, 1080

zoom_in = 1.1
zoom_out = 0.9

pygame.init()
pygame.display.set_caption("Grafika komputerowa projekt 1")
screen = pygame.display.set_mode((width, height))

angle = 0.1
cube_position = [width // 2, height // 2]
vertex_size = 3
step = 0.4
points = [n for n in range(8)]
points2 = [n for n in range(8)]
points3 = [n for n in range(8)]
points4 = [n for n in range(8)]

points[0] = [[-4], [-1], [-7], [1]]
points[1] = [[-2], [-1], [-7], [1]]
points[2] = [[-2], [1], [-7], [1]]
points[3] = [[-4], [1], [-7], [1]]
points[4] = [[-4], [-1], [-9], [1]]
points[5] = [[-2], [-1], [-9], [1]]
points[6] = [[-2], [1], [-9], [1]]
points[7] = [[-4], [1], [-9], [1]]

points2[0] = [[4], [-1], [-7], [1]]
points2[1] = [[2], [-1], [-7], [1]]
points2[2] = [[2], [1], [-7], [1]]
points2[3] = [[4], [1], [-7], [1]]
points2[4] = [[4], [-1], [-9], [1]]
points2[5] = [[2], [-1], [-9], [1]]
points2[6] = [[2], [1], [-9], [1]]
points2[7] = [[4], [1], [-9], [1]]

points3[0] = [[-4], [-1], [-3], [1]]
points3[1] = [[-2], [-1], [-3], [1]]
points3[2] = [[-2], [1], [-3], [1]]
points3[3] = [[-4], [1], [-3], [1]]
points3[4] = [[-4], [-1], [-5], [1]]
points3[5] = [[-2], [-1], [-5], [1]]
points3[6] = [[-2], [1], [-5], [1]]
points3[7] = [[-4], [1], [-5], [1]]

points4[0] = [[4], [-1], [-3], [1]]
points4[1] = [[2], [-1], [-3], [1]]
points4[2] = [[2], [1], [-3], [1]]
points4[3] = [[4], [1], [-3], [1]]
points4[4] = [[4], [-1], [-5], [1]]
points4[5] = [[2], [-1], [-5], [1]]
points4[6] = [[2], [1], [-5], [1]]
points4[7] = [[4], [1], [-5], [1]]

cubes = [points, points2, points3, points4]
camera = [[0], [0], [5], [1]]

def distance_to_observer(points):
    d = math.sqrt(math.pow(points[0][0][0] - camera[0][0], 2) + math.pow(points[0][1][0] - camera[1][0], 2) + math.pow(points[0][2][0] - camera[2][0], 2))

    return d


def rotation_x(angle):
    rotation_x = [[1, 0, 0, 0],
                  [0, math.cos(angle), -math.sin(angle), 0],
                  [0, math.sin(angle), math.cos(angle), 0],
                  [0, 0, 0, 1]]
    return rotation_x

def rotation_y(angle):
    rotation_y = [[math.cos(angle), 0, math.sin(angle), 0],
                  [0, 1, 0, 0],
                  [-math.sin(angle), 0, math.cos(angle), 0],
                  [0, 0, 0, 1]
                  ]
    return rotation_y

def rotation_z(angle):
    rotation_z = [[math.cos(angle), -math.sin(angle), 0, 0],
                  [math.sin(angle), math.cos(angle), 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]
                  ]
    return rotation_z

def translation(Tx, Ty, Tz):
    translation = [
        [1, 0, 0, Tx],
        [0, 1, 0, Ty],
        [0, 0, 1, Tz],
        [0, 0, 0, 1]
    ]
    return translation

def scale(Sx, Sy, Sz):
    scale = [
        [Sx, 0, 0, 0],
        [0, Sy, 0, 0],
        [0, 0, Sz, 0],
        [0, 0, 0, 1]
    ]
    return scale

toScreen = [
    [width/10, 0, 0, width/10],
    [0, -height/10, 0, height/10],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

def connect_point(i, j, k, color):
    a = k[i]
    b = k[j]
    pygame.draw.line(screen, color, (a[0][0], a[1][0]), (b[0][0], b[1][0]), 2)

def draw_cube(projected_points, visible, color):
    for m in range(4):
        if visible[m] == 1 and visible[(m+1) % 4] == 1:
            connect_point(m, (m + 1) % 4, projected_points, color)
        if visible[m+4] == 1 and visible[(m+1) % 4 + 4] == 1:
            connect_point(m + 4, (m + 1) % 4 + 4, projected_points, color)
        if visible[m] == 1 and visible[m+4] == 1:
            connect_point(m, m + 4, projected_points, color)

def project_cube(points, color):
    index = 0
    projected_points = [j for j in range(len(points))]
    visible = [j for j in range(len(points))]
    for point in points:
        projected_2d = matrix_multiplication(toScreen, point)
        projected_points[index] = projected_2d
        z = 1 / (0 - projected_2d[2][0])
        if z < 0:
            visible[index] = 0
        else:
            visible[index] = 1
            projected_points[index][0][0] *= z
            projected_points[index][1][0] *= z
            projected_points[index][0][0] += cube_position[0]
            projected_points[index][1][0] += cube_position[1]
            # pygame.draw.circle(screen, color, (projected_points[index][0][0], projected_points[index][1][0]), vertex_size)
        index += 1
    draw_cube(projected_points, visible, color)

def recalculate_points(matrix, points):
    idx = 0
    for point in points:
        rotated_2d = matrix_multiplication(matrix, point)
        points[idx] = rotated_2d
        idx += 1

def recalculate_points_all(matrix):
    recalculate_points(matrix, points)
    recalculate_points(matrix, points2)
    recalculate_points(matrix, points3)
    recalculate_points(matrix, points4)


run = True
while run:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #zoom?
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
            recalculate_points_all(scale(1, 1, zoom_out))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
            recalculate_points_all(scale(1, 1, zoom_in))
        #rotations
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            recalculate_points_all(rotation_x(angle))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            recalculate_points_all(rotation_y(angle))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            recalculate_points_all(rotation_z(angle))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            recalculate_points_all(rotation_x(-angle))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            recalculate_points_all(rotation_y(-angle))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
            recalculate_points_all(rotation_z(-angle))
        #translations
            #forward, backward
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            recalculate_points_all(translation(0, 0, step))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            recalculate_points_all(translation(0, 0, -step))
            #up, down, left, right
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            recalculate_points_all(translation(0, -step, 0))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            recalculate_points_all(translation(0, step, 0))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            recalculate_points_all(translation(step, 0, 0))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            recalculate_points_all(translation(-step, 0, 0))

    d = distance_to_observer(points)
    d2 = distance_to_observer(points2)
    d3 = distance_to_observer(points3)
    d4 = distance_to_observer(points4)

    distances = {0: d, 1: d2, 2: d3, 3: d4}
    sorted_distances = dict(sorted(distances.items(), key=lambda item: item[1]))
    keys = sorted_distances.keys()
    order_index_list = list(keys)
    order_index_list.reverse()

    colors = [black, red, green, blue]
    for i in order_index_list:
        project_cube(cubes[i], colors[i])

    pygame.display.update()

pygame.quit()
