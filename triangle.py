def find_vertices(y,sorted_x,sorted_y):
    """
    Returns vertices which has the point which
    you gave the Y in between
    
    Returns vertices in format (x1,y1,x2,y2)
    """
    
    vertices = []

    idxs = [(0,1),(1,2),(0,2)]
    
    for (idx1,idx2) in idxs:
        if y >= sorted_y[idx1] and y <= sorted_y[idx2] and sorted_y[idx1] != sorted_y[idx2]:
            vertices.append((sorted_x[idx1],sorted_y[idx1],
                             sorted_x[idx2],sorted_y[idx2]))

    if len(vertices) == 3:
        vertices = vertices[1:]

    return vertices


calc_inverse_slope = lambda v: (v[2] - v[0]) / (v[3] - v[1])
calc_y_change = lambda v,y: y - v[1]
def find_x_start_x_end(v1,v2,y):
    """
    Returns x_start and x_end for the given vertices
    and the y point
    """
    
    v1_slope = calc_inverse_slope(v1)
    v2_slope = calc_inverse_slope(v2)
    
    v1_y_change = calc_y_change(v1,y)
    v2_y_change = calc_y_change(v2,y)

    x_start = v1[0] + v1_slope * v1_y_change
    x_end = v2[0] + v2_slope * v2_y_change

    return x_start,x_end


def calc_triangle_points(x: tuple[int],y: tuple[int]):
    if len(x) != 3 or len(y) != 3:
        raise ValueError("both len(x) and len(y) should be 3")

    
    points = []


    max_y = int(max(y))
    min_y = int(min(y))
    
    if min_y == max_y:
        max_x = max(x)
        min_x = min(x)

        for x in range(min_x,max_x+1):
            points.append((x,min_y))

        return points

    sorted_pairs = sorted(zip(x,y),key = lambda pair: pair[1])
    
    sorted_x,sorted_y = zip(*sorted_pairs)
    

    for y_ in range(min_y,max_y+1):
        vertices = find_vertices(y_,sorted_x,sorted_y)
        v1,v2 = vertices[0],vertices[1]

        x_start,x_end = find_x_start_x_end(v1,v2,y_)
        x_start,x_end = sorted([x_start,x_end])
        x_start,x_end = int(x_start),int(x_end)

        for x_ in range(x_start,x_end+1):
            points.append((x_,y_))


    return points
