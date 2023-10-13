# UAV-Drone-Path

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

[`federico-rosatelli`](https://github.com/federico-rosatelli)

# Description
UAV-Drone-Path is a package which allows you to create a coordinate grid with objects, called obstacles, and control a virtual drone. Once instructed in the actions to perform, he will perform them avoiding obstacles and completing the various objectives. Once the route is finished you can view the grid and the route used by the drone.

<img src="img/Figure_1.png"  width="500" height="500" alt="test1 output">
<img src="img/Figure_2.png"  width="500" height="500" alt="test2 output">

# Usage
`test1.py` & `test2.py` provide a semi-complete guide on how to use this package.

To get started import the command file from src:
```python
from src import command
```

Now you can create the first Command and Drone object as:
```python
comm = command.NewCommand('grid_file')
drone = command.NewDrone(comm,"Drone_Type","Drone_Name",[100,200,201,300],100)
```

To execute and create an action use:
```python
comm.createAction("Name_of_Action",drone,COMMAND_INT,comm.returnObstacle(OBSTACLE_NUM),HEIGHT_INT)
```

The grid display is made available by the method `display()` of the Command class.

# The Grid
To create you personal grid you have to create a .txt file like this:
```
0,0,0 20,20,20  //first and last coordinate of you grid
2,2,0 4,5,15    //first and last coordinate of your obstacle
7,16,2 10,17,20 //first and last coordinate of your obstacle
```
Remember that each coordinate is `(x,y,z)` formatted

# Why?
Because I was bored and I like UAV and drones :)

# WARINNG
This package is not completed.

## TODO
- [x] Best Path Finder
- [x] Dinamic Obstacle with file
- [x] Grid Display
- [x] Drone Battery Usage
- [x] Rotation Action
- [x] Hawk's View Action
- [ ] Implement More Action
- [ ] Live Drone Test
- [ ] Panorama mapping and Grid Implementation
