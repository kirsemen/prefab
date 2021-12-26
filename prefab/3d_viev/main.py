from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import sys
from ctypes import c_float, c_uint
from numpy import array as np_array
import glm

size = [1000, 500]

player_pos = glm.vec3(0, 0, -60)
player_angle = glm.vec2(0, 0)
player_size = 100
speed = 1

now_pos = [None, None]
perspective = True


def get_object_from_file(filename, types):
    _vertex, _faces = [], []
    with open(filename) as f:
        for line in f:
            if line.startswith('v '):
                _vertex.append([float(i) for i in line.split()[1:]])
            elif line.startswith('f'):
                _faces.append([int(face_.split('/')[0]) - 1 for face_ in line.split()[1:]])
    _faces_2 = []
    if types == "GL_TRIANGLES":
        _faces_2 = []
        for _face in _faces:
            i = 1
            while i + 1 <= len(_face) - 1:
                _faces_2.append([_face[0], _face[i], _face[i + 1]])
                i += 1
    elif types == "GL_LINES":
        _faces_2 = []
        for _face in _faces:
            i = 0
            while i + 1 <= len(_face) - 1:
                _faces_2.append([_face[i], _face[i + 1]])
                i += 1
            _faces_2.append([_face[i], _face[0]])
    return _vertex, _faces_2


def init():
    pygame.init()

    _screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL)
    _clock = pygame.time.Clock()

    glEnable(GL_DEPTH_TEST)



    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if perspective:
        gluPerspective(45, 1, 0.1, 200)
    else:
        glOrtho(-40, 40, -40, 40, -100, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glScalef(size[1] / size[0], 1, 1)

    _vertexVBO = GLuint()
    _indexEBO = GLuint()

    glGenBuffers(1, _vertexVBO)
    glBindBuffer(GL_ARRAY_BUFFER, _vertexVBO)
    glBufferData(GL_ARRAY_BUFFER, len(vertexes) * 4, (c_float * len(vertexes))(*vertexes),
                 GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glGenBuffers(1, _indexEBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, _indexEBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indexes) * 4, (c_uint * len(indexes))(*indexes),
                 GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    return _screen, _clock, _vertexVBO, _indexEBO


def event_update():
    global now_pos, player_pos, player_size
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                player_size *= 0.9
            elif event.button == 5:
                player_size *= 1.2
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        arr = glm.rotate(
            glm.rotate(
                glm.vec3(speed, 0, 0),
                glm.radians(player_angle[1]),
                glm.vec3(-1, 0, 0)
            ),
            glm.radians(player_angle[0]),
            glm.vec3(0, -1, 0)
        )
        player_pos -= arr
    if keys[pygame.K_a]:
        arr = glm.rotate(
            glm.rotate(
                glm.vec3(speed, 0, 0),
                glm.radians(player_angle[1]),
                glm.vec3(-1, 0, 0)
            ),
            glm.radians(player_angle[0]),
            glm.vec3(0, -1, 0)
        )
        player_pos += arr
    if keys[pygame.K_s]:
        arr = glm.rotate(
            glm.rotate(
                glm.vec3(0, 0, speed if perspective else -speed),
                glm.radians(player_angle[1]),
                glm.vec3(-1, 0, 0)
            ),
            glm.radians(player_angle[0]),
            glm.vec3(0, -1, 0)
        )
        player_pos -= arr
    if keys[pygame.K_w]:
        arr = glm.rotate(
            glm.rotate(
                glm.vec3(0, 0, speed if perspective else -speed),
                glm.radians(player_angle[1]),
                glm.vec3(-1, 0, 0)
            ),
            glm.radians(player_angle[0]),
            glm.vec3(0, -1, 0)
        )
        player_pos += arr
    if keys[pygame.K_e]:
        arr = glm.rotate(
            glm.rotate(
                glm.vec3(0, speed, 0),
                glm.radians(player_angle[1]),
                glm.vec3(-1, 0, 0)
            ),
            glm.radians(player_angle[0]),
            glm.vec3(0, -1, 0)
        )
        player_pos += arr
    if keys[pygame.K_q]:
        arr = glm.rotate(
            glm.rotate(
                glm.vec3(0, speed, 0),
                glm.radians(player_angle[1]),
                glm.vec3(-1, 0, 0)
            ),
            glm.radians(player_angle[0]),
            glm.vec3(0, -1, 0)
        )
        player_pos -= arr

    if pygame.mouse.get_pressed(3)[0]:
        if now_pos == [None, None]:
            now_pos = pygame.mouse.get_pos()
        else:
            player_angle[1] += (now_pos[1] - pygame.mouse.get_pos()[1]) * 0.2
            player_angle[0] += (now_pos[0] - pygame.mouse.get_pos()[0]) * 0.2
            now_pos = pygame.mouse.get_pos()
            player_angle[0] = player_angle[0] % 360
            player_angle[1] = min(max(player_angle[1], -90), 90)
    else:
        now_pos = [None, None]


def draw():
    glPushMatrix()
    glTranslate(0, 0, -player_size)
    glRotate(player_angle[1], 1, 0, 0)
    glRotate(player_angle[0], 0, 1, 0)
    glTranslate(*player_pos)

    glEnableClientState(GL_VERTEX_ARRAY)

    glBindBuffer(GL_ARRAY_BUFFER, vertexVBO)
    glVertexPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexEBO)
    glDrawElements(GL_LINES, len(indexes), GL_UNSIGNED_INT, None)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    glDisableClientState(GL_VERTEX_ARRAY)

    glPopMatrix()


vertexes, indexes = get_object_from_file("resources/t_34_obj.obj", "GL_LINES")

vertexes = list(np_array(vertexes).reshape(len(vertexes) * len(vertexes[0])))
indexes = list(np_array(indexes).reshape(len(indexes) * len(indexes[0])))

screen, clock, vertexVBO, indexEBO = init()

while True:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    event_update()
    draw()
    pygame.display.set_caption(str(clock.get_fps()))
    pygame.display.flip()
    clock.tick(60)
