from drawminal import DrawminalBoard
from triangle import calc_triangle_points
from projection import projection_and_rotate
from time import sleep
from math import pi,sqrt
import random
import sys,select,termios,tty

board = DrawminalBoard()
tris = []

cx = 0
cy = 0
cz = 0
focal = 90

yaw = 0
pitch = 0
roll = 0

def draw_tri(points,char):
    for (x,y) in points:
        board.replace(y,x,char)

def render_tri(points,char):
    points = calc_triangle_points(points[0],points[1])
    draw_tri(points,char)

def add_tri(p1,p2,p3,yaw,pitch,roll,focal,char,pivx,pivy,pivz):
    x = projection_and_rotate(p1,p2,p3,yaw,pitch,roll,focal,board.w,board.h,pivx,pivy,pivz)
    tris.append((x,char))

def calc_dist(p1,p2,p3,cx,cy,cz):
    center_x,center_y,center_z = [(p1[i] + p2[i] + p3[i]) / 3 for i in range(3)]

    dist = sqrt((cx - center_x) ** 2 + (cy - center_y) ** 2 + (cz - center_z) ** 2)

    return dist

def sort_tris(tris):
    dists = [calc_dist(*rotated + [cx,cy,cz]) for (tri,rotated),_ in tris]
    
    sorted_tris = sorted(tris,key=lambda tri: dists[tris.index(tri)])
    sorted_tris = reversed(sorted_tris)

    return sorted_tris

def render_tris(tris):
    sorted_tris = sort_tris(tris)
    for (tri,_),char in sorted_tris:
        render_tri(tri,char)

def add_tri_for_cube(p1_add,p2_add,p3_add,size,center,yaw,pitch,roll,focal,char):
    center_x,center_y,center_z = center
    size_half = size // 2

    add_tri((center_x + size_half * p1_add[0],center_y + size_half * p1_add[1],center_z + size_half * p1_add[2]),
            (center_x + size_half * p2_add[0],center_y + size_half * p2_add[1],center_z + size_half * p2_add[2]),
            (center_x + size_half * p3_add[0],center_y + size_half * p3_add[1],center_z + size_half * p3_add[2]),
            yaw,pitch,roll,focal,char,center[0],center[1],center[2])

def add_cube(center,size,yaw,pitch,roll,focal,chars):
    add_tri_for_cube((-1,-1,-1),(-1,+1,-1),(+1,-1,-1),size,center,yaw,pitch,roll,focal,chars[0])
    add_tri_for_cube((+1,+1,-1),(-1,+1,-1),(+1,-1,-1),size,center,yaw,pitch,roll,focal,chars[0])

    add_tri_for_cube((-1,-1,+1),(-1,+1,+1),(+1,-1,+1),size,center,yaw,pitch,roll,focal,chars[1]) 
    add_tri_for_cube((+1,+1,+1),(-1,+1,+1),(+1,-1,+1),size,center,yaw,pitch,roll,focal,chars[1])

    add_tri_for_cube((-1,-1,-1),(-1,+1,-1),(-1,-1,+1),size,center,yaw,pitch,roll,focal,chars[2]) 
    add_tri_for_cube((-1,+1,+1),(-1,+1,-1),(-1,-1,+1),size,center,yaw,pitch,roll,focal,chars[2])

    add_tri_for_cube((+1,-1,-1),(+1,+1,-1),(+1,-1,+1),size,center,yaw,pitch,roll,focal,chars[3])
    add_tri_for_cube((+1,+1,+1),(+1,+1,-1),(+1,-1,+1),size,center,yaw,pitch,roll,focal,chars[3])

    add_tri_for_cube((-1,-1,-1),(-1,-1,+1),(+1,-1,-1),size,center,yaw,pitch,roll,focal,chars[4])
    add_tri_for_cube((+1,-1,+1),(-1,-1,+1),(+1,-1,-1),size,center,yaw,pitch,roll,focal,chars[4])

    add_tri_for_cube((-1,+1,-1),(-1,+1,+1),(+1,+1,-1),size,center,yaw,pitch,roll,focal,chars[5])
    add_tri_for_cube((+1,+1,+1),(-1,+1,+1),(+1,+1,-1),size,center,yaw,pitch,roll,focal,chars[5])

while True:
    tris = []
    board.clear()

    add_cube((0,0,2000),board.w * board.h * 0.15,yaw,pitch,roll,focal,["-","●","@","&","#",">"])

    render_tris(tris)
    
    board.print_()
    
    sleep(0.05)
    
    roll += 0.1
    roll = roll % (2 * pi)

    yaw += 0.1
    yaw = yaw % (2 * pi)

    pitch += 0.1 
    pitch = pitch % (2 * pi)

