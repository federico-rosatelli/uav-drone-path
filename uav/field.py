"""
Field Module
"""
import json
import math
import os
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import triangulate


class Border:
    """
    Border is a class that allows you to create a virtual map of the borders of a country and/or area.
    It takes as input data from a csv file formatted as geographic coordinates
    """
    def __init__(self,file_name:str,index_border:int,formatted:str) -> None:
        self.file_name = file_name
        self.index_border = index_border
        self.list_coordinates = self.borderCollector(formatted) 

    
    def borderCollector(self,formatted) -> list:
        rd = open(self.file_name).readlines()

        border_raw = rd[self.index_border]
        border_raw = border_raw[1:border_raw[1:].index('"')+1]
        border_raw = border_raw[border_raw.index("((")+2:border_raw.index("))")]

        if formatted == "multi":
            list_coordinates_collector_raw = [list_coordinate.split(",") for list_coordinate in border_raw.split("),(")]
            list_coordinates_collector = []
            for list_coordinate in [list_coordinates_collector_raw[0]]:
                coordinates_raws = [coordinate.split(" ") for coordinate in list_coordinate]
                coordinates = [(float(coordinate[0]),float(coordinate[1])) for coordinate in coordinates_raws]
                list_coordinates_collector += coordinates
            return list_coordinates_collector

        list_coordinates_raw = [coordinate.split(" ") for coordinate in border_raw.split(",")]
        list_coordinates = [(float(coordinate[0]),float(coordinate[1])) for coordinate in list_coordinates_raw]
        
        return list_coordinates
    
    def __len__(self) -> int:
        return len(self.list_coordinates)
    
    def __getitem__(self,i:int) -> tuple:
        return self.list_coordinates[i]
    
    def getCoordinates(self) -> list:
        return self.list_coordinates

def createDict(list_coordinates,base_distance):
    polygon = Polygon(list_coordinates)
    i = 0
    graph = {}
    not_seen = list_coordinates.copy()
    while i < len(list_coordinates):
        point1 = list_coordinates[i]
        k = i + 1
        graph[point1] = []
        
        while k-i < len(list_coordinates)/2 and k < len(list_coordinates):
            # if k-i > len(list_coordinates)/2:
            #     #print(len(graph[point1]))
            #     break
            # if k == i or list_coordinates[k] in graph:
            #     k += 1
            #     continue
            point2 = list_coordinates[k]
            distance = math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
            if distance <= base_distance:
                segment = LineString([point1, point2])
                if segment.within(polygon):
                    graph[point1].append((point2,distance))
                    # if point2 in not_seen:
                    #     not_seen.pop(not_seen.index(point2))
                    #already_seen.append(point2)
            k += 1
        i += 1
        print(len(graph[point1]))
    # print([list_coordinates.index(s) for s in not_seen])
    # print(len(list_coordinates))
    return graph

def remap_keys(mapping):
    return [{'key':k, 'value': mapping[k]} for k in mapping]

def keys_remap(mapping):
    graph = {}
    #print(mapping)
    for i in range(len(mapping)):
        key = mapping[i]["key"]
        value = mapping[i]["value"]
        graph[tuple(key)] = [(tuple(v[0]),v[1]) for v in value]
    return graph

def path_drone_field(list_coordinates,base_distance,json_file):
    if json_file:
        js_file = json_file[:json_file.index(".")]+"_"+str(base_distance)+".json"
        if os.path.exists(js_file):
            with open(js_file, 'r') as json_file:
                raw_graph = json.load(json_file)
            graph = keys_remap(raw_graph)
        else:
            print("Writing")
            graph = createDict(list_coordinates,base_distance)
            with open(js_file,'w') as js_wr:
                json.dump(remap_keys(graph),js_wr,indent=4)
    else:
        graph = createDict(list_coordinates,base_distance)
    open_list = list_coordinates.copy()
    print(graph[open_list[6]])
    paths = algo(graph,open_list[6],open_list[-1])
    return [open_list[6]]+[path[0] for path in paths]

def algo(G:dict,current_node:tuple,final_node:tuple) -> list:
    """
    Dijkstra Algorithm's with A* application.
    From the complete grid `G`, the starting and ending node (coordinates) it'll return the best path between them.
    """
    open_list = {}
    open_list[current_node] = (current_node,[],0)
    closed_list = {}
    while open_list:
        list_action = G[current_node]
        for action in list_action:
            action_cost = action[1]
            next_node = action[0]
            if next_node not in closed_list:
                total_cost = action_cost
                if (next_node in open_list and open_list[next_node][2]>open_list[current_node][2]+total_cost) or (next_node not in open_list):
                    next_node_tuple = (next_node,open_list[current_node][1]+[action],open_list[current_node][2]+total_cost)
                    open_list[next_node] = next_node_tuple
        closed_list[current_node] = open_list[current_node]
        open_list.pop(current_node,None)
        min_next_node = min(open_list.keys(),key=lambda k: open_list[k][2])
        if (open_list[min_next_node][0] == final_node):
            return open_list[min_next_node][1]
        current_node = open_list[min_next_node][0]
    # polygon = Polygon(list_coordinates)
    # path = []
    # not_good = []
    # i = 0
    # while len(open_list) >0:
    #     k = 0
    #     point1 = open_list[i]
    #     open_list.pop(i)
    #     if not point1 in closed_list:
    #         closed_list[point1] = []
    #         while k < len(open_list):
    #             point2 = open_list[k]
    #             distance = math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
    #             if distance <= base_distance and open_list[k] not in not_good:
    #                 closed_list[point1].append((point2,distance,k))
    #             k += 1
    #     if not open_list or len(closed_list[point1]) < 2:
    #         return path
    #     max_distance = max(closed_list[point1],key=lambda x: x[1])
    #     point2 = max_distance[0]
    #     segment = LineString([point1, point2])
    #     #print(path)
    #     #print(len(open_list))
    #     print("PRIMA",len(closed_list[point1]))
    #     while not segment.within(polygon) and closed_list[point1]:
    #         print(len(closed_list[point1]))
    #         max_distance = max(closed_list[point1],key=lambda x: x[1])
    #         point2 = max_distance[0]
    #         segment = LineString([point1, point2])
    #         closed_list[point1].pop(closed_list[point1].index(max_distance))
    #         #print(closed_list[point1])
    #     if not closed_list[point1]:
    #         for point in closed_list[path[-1]]:
    #             open_list.append(point[0])
    #         open_list.pop(max_distance[2])

    #         not_good.append(point1)
    #         open_list.append(path[-1])
    #         i = len(open_list) - 1
    #         continue
    #     i = max_distance[2]
    #     for point in closed_list[point1]:

    #         if point in open_list:
    #             open_list.pop(open_list.index(point))
    #         #open_list.pop(points[2])
    #     path.append(point2)

    return


def path_drone_field1(list_coordinates,base_distance):
    open_list = list_coordinates.copy()
    polygon = Polygon(list_coordinates)
    polygon_ext = LineString(list(polygon.exterior.coords))

    closed_list = [open_list[0]]
    i = 0
    while open_list:
        point1 = (open_list[i][0],open_list[i][1])
        # point_a = Point(point1[0],point1[1])
        # coordinate = open_list[i]
        distances = []
        k = 0
        open_list.pop(i)
        # deleting = []
        while k < len(open_list):
            point2 = (open_list[k][0],open_list[k][1])
            distance = math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
            
            if distance >= base_distance:
                
                distances.append((distance,k))
                k += 1


            else:
                # deleting.append((distance,point2))
                open_list.pop(k)
            
        if len(distances) == 0:
            return closed_list
        min_distance = min(distances, key=lambda x: x[0])
        
        i = min_distance[1]
        # point_b = Point(open_list[i][0],open_list[i][1])
        # segment = LineString([point_a, point_b])
        # while not segment.within(polygon) and len(distances)>1:
        #     distances.pop(distances.index(min_distance))
        #     min_distance = min(distances, key=lambda x: x[0])
        #     i = min_distance[1]
        #     point_b = Point(open_list[i][0],open_list[i][1])
        #     segment = LineString([point_a, point_b])

        # if not segment.within(polygon) and deleting:
        #     good = (-math.inf,(0,0))
        #     for dell in deleting:
        #         point_b = Point(dell[1][0],dell[1][1])
        #         segment = LineString([point_a, point_b])
        #         if segment.within(polygon) and dell[0] > good[0]:
        #             good = dell
        #     open_list.append(dell[1])
        #     i = len(open_list) - 1
            # for dell in deleting:
            #     if i != dell[1]:
            #         open_list.pop(dell[1])

        closed_list.append(open_list[i])

    return closed_list
        

def define_circle_quarter(coordinates):
    d1 = 0
    d2 = 0
    line1 = []
    line2 = []
    quarter = [coordinates[:len(coordinates)//4],coordinates[len(coordinates)//4:len(coordinates)//2],coordinates[len(coordinates)//2:(len(coordinates)//4)*3],coordinates[(len(coordinates)//4)*3:]]
    for i0 in range(len(quarter[0])):
        for i2 in range(len(quarter[2])):
            distance = math.sqrt(((quarter[0][i0][0]-quarter[2][i2][0])**2)+((quarter[0][i0][1]-quarter[2][i2][1])**2))
            if distance > d1:
                line1 = [quarter[0][i0],quarter[2][i2]]
                d1 = distance
    for i1 in range(len(quarter[1])):
        for i3 in range(len(quarter[3])):
            distance = math.sqrt(((quarter[1][i1][0]-quarter[3][i3][0])**2)+((quarter[1][i1][1]-quarter[3][i3][1])**2))
            if distance > d2:
                line2 = [quarter[1][i1],quarter[3][i3]]
                d2 = distance
    
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]

    m1 = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')
    b1 = y1 - m1 * x1 if m1 != float('inf') else x1

    m2 = (y4 - y3) / (x4 - x3) if (x4 - x3) != 0 else float('inf')
    b2 = y3 - m2 * x3 if m2 != float('inf') else x3

    if m1 == m2:
        center = ((line1[0]+line2[0])/2,(line1[1]+line2[1]/2))
        lines = line1+line2
        return center, max(lines,key=lambda x: math.sqrt(((center[0]-x[0])**2)+((center[1]-x[1])**2)))

    X1 = (b2 - b1) / (m1 - m2)
    Y1 = m1 * X1 + b1
    
    max_dist_point = max(coordinates,key=lambda x: math.sqrt(((X1-x[0])**2)+((Y1-x[1])**2)))
    radius = math.sqrt(((X1-max_dist_point[0])**2)+((Y1-max_dist_point[1])**2))
    return (X1,Y1),radius

def define_circle(coordinates):
    d1 = 0
    line = []
    for i in range(len(coordinates)):
        for k in range(i+1,len(coordinates)):
            distance = math.sqrt(((coordinates[i][0]-coordinates[k][0])**2)+((coordinates[i][1]-coordinates[k][1])**2))
            if distance > d1:
                line = [coordinates[i],coordinates[k]]
                d1 = distance
    center_point = ((line[0][0]+line[1][0])/2,(line[0][1]+line[1][1])/2)
    max_distance_point = max(coordinates,key=lambda x: math.sqrt(((center_point[0]-x[0])**2)+((center_point[1]-x[1])**2)))
    max_distance = math.sqrt(((center_point[0]-max_distance_point[0])**2)+((center_point[1]-max_distance_point[1])**2))
    return center_point, max_distance


def display_border_field(list_coordinates,prev_not_view,name_field,extra) -> None:
    fig = plt.figure()
    ax = fig.add_subplot()
    new_coordinates = [[],[]]
    path = [[],[]]
    for view in prev_not_view:
        path[0].append(view[0])
        path[1].append(view[1])
    for coordinate in list_coordinates:
        new_coordinates[0].append(coordinate[0])
        new_coordinates[1].append(coordinate[1])
    
    ax.plot(new_coordinates[0],new_coordinates[1],'r')
    
    ax.plot(path[0],path[1],'b')

    if "triangulate" in extra:

        polygon = Polygon(list_coordinates)
        triangles = triangulate_within(polygon)
        
        for t in triangles:
            triangle = [[],[]]
            coordinates = t.exterior.coords
            for coo in coordinates:
                triangle[0].append(coo[0])
                triangle[1].append(coo[1])
            ax.plot(triangle[0],triangle[1],'g')

    if "circle" in extra:
        center,radius = define_circle(list_coordinates)
        circle = plt.Circle(center, radius, color='g', fill=False,clip_on=False)
        ax.add_patch(circle)
        ax.plot([center[0]],[center[1]],'*')

    ax.grid(False)
    ax.set_title(f'{name_field if name_field != "" else "Field Drone Path"}')
    plt.show()

def triangulate_within(polygon):
    return [triangle for triangle in triangulate(polygon) if triangle.within(polygon)]

def NewBorder(file_name:str,border_index:int,formatted:str):
    return Border(file_name,border_index,formatted)


def DronePathBorder(border:Border,max_distance:int,json_file:str):
    list_coordinates = border.getCoordinates().copy()
    return path_drone_field(list_coordinates,max_distance,json_file)

def DisplayBorderPath(border:Border,path_drone_border:list,name_field:str,center:bool):
    list_coordinates = border.getCoordinates()
    display_border_field(list_coordinates,path_drone_border,name_field,center)