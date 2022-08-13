import math
import random

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

stars = [
    # Nothing
]

view_distance = 5

display_size = (800, 600)

def render_stars():

    glBegin(GL_POINTS)
    for star in stars:
        glVertex3fv(star)
    glEnd()

def create_star_map_default():
    global stars
    # The camera is 5 away from the stars, so we generate 200 stars randomly
    # and then scale them to be 5 away from the point (0, 0, -5).
    """stars = (
        ( 1,-1,-1),
        ( 1, 1,-1),
        (-1, 1,-1),
        (-1,-1,-1),
        ( 1,-1, 1),
        ( 1, 1, 1),
        (-1,-1, 1),
        (-1, 1, 1)
    )"""
    for _ in range(200):
        rand_pt = (
            random.randint(-100, 100),
            random.randint(-100, 100),
            random.randint(-100, 100)
        )
        # We can't have stars being AT the origin.
        # The triggers for stars whose coordinates "happen" to sum to 0 also,
        # but it's an acceptable loss.
        if rand_pt[0] + rand_pt[1] + rand_pt[2] == 0:
            continue
        dist = math.sqrt(rand_pt[0] ** 2 + rand_pt[1] ** 2 + rand_pt[2] ** 2)
        dist_scaled = dist / view_distance
        star = (
            rand_pt[0] / dist_scaled,
            rand_pt[1] / dist_scaled,
            rand_pt[2] / dist_scaled - view_distance
        )
        stars.append(star)

def init():
    pygame.init()
    pygame.display.set_mode(display_size, DOUBLEBUF|OPENGL)

def tick():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    glRotatef(0.25, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    render_stars()
    pygame.display.flip()
    pygame.time.wait(10)

def mainloop():
    while True:
        tick()

def main():
    init()
    create_star_map_default()
    gluPerspective(45, (display_size[0]/display_size[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -view_distance)
    mainloop()

if __name__ == '__main__':
    main()
