import uav
from uav import command

comm = command.NewCommand("example/grid2.txt")
drone = command.NewDrone(comm,"Thermal","LittleF0x",[command.INSPECT_CAMERA,command.INSPECT_THERMAL,command.ROTATE],100)

comm.setBase((9,0,0))

comm.createAction("Rotation Obstacle 0",drone,uav.ROTATE,comm.returnObstacle(0),6)
comm.createAction("Rotation Obstacle 1",drone,uav.ROTATE,comm.returnObstacle(1),1)
comm.createAction("Inspection Obstacle 1",drone,uav.INSPECT_CAMERA,comm.returnObstacle(1))
comm.createAction("Rotation Obstacle 2",drone,uav.ROTATE,comm.returnObstacle(2),5)
print(f"The battery of drone {drone.getName()} is: {drone.getBattery()}")
comm.returnToBase("Return to Base",drone)

comm.display()