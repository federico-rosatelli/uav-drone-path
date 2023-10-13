import math

def importGrid(filename:str) -> (list,list):
    """
    Import Grid Max & Min coordinates from file `filename`.\n
    Import Obstacles coordinates and dimensions from the same file
    """
    rd = open(filename).readlines()
    dimensions = rd[0].split(" ")
    dimensions = [[int(i) for i in dimensions[k].split(",")] for k in range(len(dimensions))]
    obstacles = [rd[i].split(" ") for i in range(1,len(rd))]
    obstacles = [[[int(i) for i in obst[k].split(",")]for k in range(len(obst))]for obst in obstacles]
    return dimensions, obstacles


def createGrid(dimensions,obstacles):
    data = {}
    notData = [[] for _ in obstacles]
    for x in range(dimensions[1][0]+1):
        for y in range(dimensions[1][1]+1):
            for z in range(dimensions[1][2]+1):
                accettable = True
                for i in range(len(obstacles)):
                    obst = obstacles[i]
                    if not((x < obst[0][0] or x > obst[1][0]) or (y < obst[0][1] or y > obst[1][1]) or (z < obst[0][2] or z > obst[1][2])):
                        notData[i].append((x,y,z))
                        accettable = False
                if accettable:
                    data[(x,y,z)] = []
                    for i in range(3):
                        i -= 1
                        for k in range(3):
                            k -= 1
                            for j in range(3):
                                j -= 1
                                if (x+i >= 0 and x+i <= dimensions[1][0]) and (y+k >= 0 and y+k <= dimensions[1][1]) and (z+j >= 0 and z+j <= dimensions[1][2]) and ((x,y,z) != (x+i,y+k,z+j)):
                                    accettable = True
                                    for obst in obstacles:
                                        if not((x+i < obst[0][0] or x+i > obst[1][0]) or (y+k < obst[0][1] or y+k > obst[1][1]) or (z+j < obst[0][2] or z+j > obst[1][2])):
                                            accettable = False
                                    if accettable:    
                                        cost = math.sqrt(abs(i)+abs(k)+abs(j))
                                            #cost = 1
                                        data[(x,y,z)].append(((x+i,y+k,z+j),cost))
    return data,notData