import math

def Dijkstra(G:dict,current_node:tuple,final_node:tuple) -> list:
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
                total_cost = action_cost + math.sqrt((final_node[0]-next_node[0])**2+(final_node[1]-next_node[1])**2+(final_node[2]-next_node[2])**2)
                if (next_node in open_list and open_list[next_node][2]>open_list[current_node][2]+total_cost) or (next_node not in open_list):
                    next_node_tuple = (next_node,open_list[current_node][1]+[action],open_list[current_node][2]+total_cost)
                    open_list[next_node] = next_node_tuple
        closed_list[current_node] = open_list[current_node]
        open_list.pop(current_node,None)
        min_next_node = min(open_list.keys(),key=lambda k: open_list[k][2])
        if (open_list[min_next_node][0] == final_node):
            return open_list[min_next_node][1]
        current_node = open_list[min_next_node][0]