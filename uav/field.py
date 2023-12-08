"""
Field Module
"""
import copy
import json
import math
import os
import matplotlib.pyplot as plt
import numpy as np
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
    while i < len(list_coordinates):
        point1 = list_coordinates[i]
        k = i + 1
        graph[point1] = []
        
        while k-i < len(list_coordinates)/2 and k < len(list_coordinates):
            point2 = list_coordinates[k]
            distance = math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
            if distance <= base_distance:
                segment = LineString([point1, point2])
                if segment.within(polygon):
                    graph[point1].append((point2,distance))
            k += 1
        i += 1
        print("{:.2f}".format(i/len(list_coordinates)*100),"%",end="\r")
    return graph

def remap_keys(mapping):
    return [{'key':k, 'value': mapping[k]} for k in mapping]

def keys_remap(mapping):
    graph = {}
    for i in range(len(mapping)):
        key = mapping[i]["key"]
        value = mapping[i]["value"]
        graph[tuple(key)] = [(tuple(v[0]),v[1]) for v in value]
    return graph

def path_drone_field(list_coordinates,base_distance,json_file):
    if json_file:
        js_file = json_file+"_"+str(base_distance)+".json"
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
    #print(graph[open_list[1]])
    paths = []
    path,max_len_point = algo(graph,open_list[1],open_list[-1])
    paths += path
    while max_len_point != open_list[-1]:
        print("{:.2f}".format((open_list.index(max_len_point)/len(open_list))*100),"%",end="\r")
        path,max_len_point = algo(graph,open_list[open_list.index(max_len_point)+1],open_list[-1])
        paths += path
    return paths


def algo(G:dict,current_node:tuple,final_node:tuple) -> list:
    first_node = current_node
    if current_node == final_node:
        return [final_node],final_node
    
    open_list = G.copy()
    closed_list = [current_node]
    max_len = 0
    max_len_point = ()
    
    history = []
    while open_list:
        if not current_node in history:
            history.append(current_node)
            open_list[current_node] = G[current_node].copy()
        if len(closed_list) > max_len:
            max_len = len(closed_list)
            max_len_point = current_node
        if final_node in [x[0] for x in open_list[current_node]]:
            closed_list.append(final_node)
            return closed_list,max_len_point
        if not open_list[current_node]:
            closed_list = closed_list[:-1]
            if not closed_list:
                return algo(G,first_node,max_len_point)[0],max_len_point
            current_node = closed_list[-1]
            continue
        max_distance = max(open_list[current_node], key=lambda x:x[1])
        open_list[current_node].pop(open_list[current_node].index(max_distance))
        current_node = max_distance[0]
        closed_list.append(current_node)
    return [final_node],final_node
        

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


def display_border_field(list_coordinates,paths,name_field,info,labels) -> None:
    fig = plt.figure()
    ax = fig.add_subplot()
    new_coordinates = [[],[]]
    all_paths = []
    for i in range(len(paths)):
        path = [[],[]]
        for view in paths[i]:
            path[0].append(view[0])
            path[1].append(view[1])
        all_paths.append(path)
    for coordinate in list_coordinates:
        new_coordinates[0].append(coordinate[0])
        new_coordinates[1].append(coordinate[1])
    ax.plot(new_coordinates[0],new_coordinates[1],'r')
    for i in range(len(all_paths)):
        path = all_paths[i]
        ax.plot(path[0],path[1],label=labels[i] if i < len(labels) else name_field+str(i+1))
    plt.legend(loc='upper right', fontsize='small', frameon=True, title='Legend Title')


    if  "triangulate" in info:

        polygon = Polygon(list_coordinates)
        triangles = triangulate_within(polygon)
        
        for t in triangles:
            triangle = [[],[]]
            coordinates = t.exterior.coords
            for coo in coordinates:
                triangle[0].append(coo[0])
                triangle[1].append(coo[1])
            ax.plot(triangle[0],triangle[1],'g')

    if "circle" in info:
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

def DisplayBorderPath(border:Border,path_drone_border:tuple[list[tuple], ...],name_field:str,info:list[str],labels:list[str]):
    list_coordinates = border.getCoordinates()
    display_border_field(list_coordinates,path_drone_border,name_field,info,labels)