from math import cos,sin

def rotate(p,yaw,pitch,roll):
    x,y,z = p 

    x_ = x * cos(yaw) + z * sin(yaw)
    y_ = y
    z_ = x * -sin(yaw) + z * cos(yaw)

    xn = x_
    yn = y_ * cos(pitch) + z_ * -sin(pitch)
    zn = y_ * sin(pitch) + z_ * cos(pitch)

    xr = xn * cos(roll) + yn * -sin(roll)
    yr = xn * sin(roll) + yn * cos(roll)
    zr = zn

    return [xr,yr,zr]

def project(p,focal,w,h):
    x,y,z = p
    
    x_ = focal*(x/z)
    y_ = focal*(y/z)

    y_ = -y_
    
    x_ += w/2
    y_ += h/2
    
    x_ = int(x_)
    y_ = int(y_)

    return (x_,y_)

def projection_and_rotate(p1,p2,p3,yaw,pitch,roll,focal,w,h,pivx,pivy,pivz):
    p1,p2,p3 = list(p1),list(p2),list(p3)

    new_points = []
    rotated = []

    for p in (p1,p2,p3):
        p[0] -= pivx; p[1] -= pivy; p[2] -= pivz 

    for p in (p1,p2,p3):
        p = rotate(p,yaw,pitch,roll)
        p[0] += pivx; p[1] += pivy; p[2] += pivz 
        rotated.append(p)

        p = project(p,focal,w,h)
        
        new_points.append(p)

    return list(zip(*new_points)),rotated
