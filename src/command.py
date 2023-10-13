from src import grid, algorithm, visual
import math
import time

BASE_COORDINATE = (0,0,0)

BASE = 100
INSPECT_CAMERA = 200
INSPECT_THERMAL = 201
INSPECT_OTHER = 202
ROTATE = 300
ROTATE_DIFFERENT_AXES = 301


class Drone:
    def __init__(self,grid_complete,drone_type:str,drone_name:str,allowed_actions:list,battery:int) -> None:
        self.grid = grid_complete
        self.drone_type = drone_type
        self.drone_name = drone_name
        self.allowed_actions = allowed_actions
        self.battery = battery
    
    def isActionAllowed(self,action):
        return action in self.allowed_actions
    
    def isBatteryUp(self,path):
        cost_action = 0
        for p in path:
            cost_action += sum(x[1] for x in p)
        if self.battery - cost_action < 0:
            return False
        if not path[-1][-1][0] == BASE_COORDINATE:
            cost_last_coordinate = sum(x[1] for x in algorithm.Dijkstra(self.grid,path[-1][-1][0],BASE_COORDINATE))
            if self.battery - (cost_action + cost_last_coordinate) < 0:
                return False
        self.battery = self.battery - cost_action
        return True
    
    def getName(self) -> str:
        return self.drone_name

    def getBattery(self) -> int:
        return self.battery




class Block:
    def __init__(self,coordinates:list,name:str) -> None:
        self.min = coordinates[0]
        self.max = coordinates[1]
        self.trajectory = [(self.min[0],self.min[1]),(self.max[0],self.min[1]),(self.min[0],self.max[1]),(self.max[0],self.max[1])]
        self.block_name = name
    
    
    def getNearestCoordinate(self,coordinates):
        nearest_distance = math.inf 
        nearest_point = (0,0)
        for p in self.trajectory:
            distance = math.sqrt(abs(((p[0]-coordinates[0])**2)+((p[1]-coordinates[1])**2)))
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_point = (p[0],p[1])
        return nearest_point

    def calculatePath(self,point):
        if point == (self.min[0],self.min[1]):
            return [(self.min[0]-1,self.min[1]-1),(self.max[0]+1,self.min[1]-1),(self.max[0]+1,self.max[1]+1),(self.min[0]-1,self.max[1]+1)]
        elif point == (self.min[0],self.max[1]):
            return [(self.min[0]-1,self.max[1]+1),(self.min[0]-1,self.min[1]-1),(self.max[0]+1,self.min[1]-1),(self.max[0]+1,self.max[1]-1)]
        elif point == (self.max[0],self.min[1]):
            return [(self.max[0]+1,self.min[1]-1),(self.max[0]+1,self.max[1]+1),(self.min[0]-1,self.max[1]+1),(self.min[0]-1,self.min[1]-1)]
        elif point == (self.max[0],self.max[1]):
            return [(self.max[0]+1,self.max[1]+1),(self.min[0]-1,self.max[1]+1),(self.min[0]-1,self.min[1]-1),(self.max[0]+1,self.min[1]-1)]

    def spot(self):
        return ((self.max[0]+self.min[0])//2,(self.max[1]+self.min[1])//2,self.max[2]+1)
    
    def getName(self):
        return self.block_name


class Action:
    def __init__(self,auth:str,drone:Drone,action_type:int,block:Block,initial_coordinates:tuple=(0,0,0),coordinateZ:int=0) -> None:
        self.type = action_type
        self.time = int(time.time())
        self.author = auth
        self.drone = drone
        self.block = block
        self.initial_coordinates = initial_coordinates
        self.coordinateZ = coordinateZ
    
    def isActionAllowed(self):
        return self.drone.isActionAllowed(self.type)

    def action(self) -> int:
        return self.type
    
    def execute(self,grid_complete):
        if self.type == ROTATE:
            nearest_coordinate = self.block.getNearestCoordinate(self.initial_coordinates)
            routes = self.block.calculatePath(nearest_coordinate)
            paths = []
            for r in range(len(routes)):
                routes[r] = (routes[r][0],routes[r][1],self.coordinateZ)
            paths = [algorithm.Dijkstra(grid_complete,self.initial_coordinates,routes[0])]
            for i in range(1,len(routes)):
                route = routes[i]
                paths.append(algorithm.Dijkstra(grid_complete,routes[i-1],route))
            
            paths.append(algorithm.Dijkstra(grid_complete,routes[len(routes)-1],routes[0]))
            
            return paths
        if self.type == BASE:
            return [algorithm.Dijkstra(grid_complete,self.initial_coordinates,(0,0,0))]
    
        if self.type == INSPECT_CAMERA:
            coordinate = self.block.spot()
            return [algorithm.Dijkstra(grid_complete,self.initial_coordinates,coordinate)]
    
    def isBatteryUp(self,path):
        return self.drone.isBatteryUp(path)



    




class Command:
    """
    Class for interact with a drone and the grid.
    """
    def __init__(self,grid_complete:dict,obstacles_coordinates:list,obstacles:list) -> None:
        self.grid_complete = grid_complete
        self.obstacles_coordinates = obstacles_coordinates
        self.obstacles = obstacles
        self.actions:list[Action] = []
        self.baseBlock = self.createBaseBlock()
        self.path = [((0,0,0),0)]
        self.blocks = self.createBlocks()
    def createAction(self,name:str,drone:Drone,action_type:int,block:Block,coordinateZ:int=0):
        action = Action(name,drone,action_type,block,self.path[-1][0],coordinateZ)
        self.addAction(action)
        return action
    def addAction(self,action:Action):
        path = action.execute(self.grid_complete)
        if not action.isBatteryUp(path):
            return
        for points in path:
            for p in points:
                self.path.append(p)
        self.actions.append(action)
    def __len__(self):
        return len(self.actions)
    def returnPath(self):
        return self.path
    def createBaseBlock(self):
        return Block([[0,0,0],[0,0,0]],"BaseBlock")
    def returnToBase(self,name,drone):
        action = Action(name,drone,BASE,self.baseBlock,self.path[-1][0],0)
        self.addAction(action)

    def display(self):
        visual.display(self.obstacles_coordinates,self.path)
    
    def createBlocks(self) -> list:
        return [Block(self.obstacles_coordinates[i],f"Block_{i}") for i in range(len(self.obstacles_coordinates))]
    
    def returnObstacle(self,i) -> Block:
        return self.blocks[i]
    
    def returnObstacles(self) -> list:
        return [(self.blocks[i].getName(),i) for i in range(len(self.blocks))]
    
    def getGrid(self) -> dict:
        return self.grid_complete


def NewCommand(filename:str):
    dimensions, obstacles_coordinates = grid.importGrid(filename)
    grid_complete, obstacles = grid.createGrid(dimensions,obstacles_coordinates)
    command = Command(grid_complete,obstacles_coordinates,obstacles)
    return command

def NewDrone(command:Command,drone_type:str,drone_name:str,drone_actions:list,battery:int):
    return Drone(command.getGrid(),drone_type,drone_name,drone_actions,battery)



# drone = Drone(grid_complete,"Thermal","ProvaDrone",[INSPECT_CAMERA,INSPECT_THERMAL,ROTATE])
# block1 = Block(obstacles_coordinates[0],"Blocco1")
# block2 = Block(obstacles_coordinates[1],"Blocco2")
# block3 = Block(obstacles_coordinates[2],"Blocco3")
# block6 = Block(obstacles_coordinates[6],"Blocco6")
# block7 = Block(obstacles_coordinates[7],"Blocco7")

# command = Command(grid_complete)
# command.createAction("fede",drone,ROTATE,block1,6)
# command.createAction("Controllo2 blocco3",drone,ROTATE,block3,4)
# command.createAction("Controllo2 blocco1",drone,ROTATE,block1,18)
# command.createAction("Controllo2 blocco2",drone,ROTATE,block2,14)
# command.createAction("Controllo2 blocco6",drone,INSPECT_CAMERA,block6)
# command.createAction("Controllo2 blocco7",drone,ROTATE,block7,3)
# # command.createAction("Controllo2 blocco7",drone,INSPECT_CAMERA,block7)
# command.createAction("Controllo2 blocco2",drone,INSPECT_CAMERA,block2)
# command.returnToBase("fede",drone)
# # print(command.returnPath())
# command.display(obstacles_coordinates)