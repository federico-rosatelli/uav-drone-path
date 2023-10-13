from src import command

comm = command.NewCommand("example/grid1.txt")
drone = command.NewDrone(comm,"Thermal","BHackFox",[command.INSPECT_CAMERA,command.INSPECT_THERMAL,command.ROTATE],800)

print(comm.returnObstacles())

comm.createAction("Rotation Obstacle 0",drone,command.ROTATE,comm.returnObstacle(0),6)
comm.createAction("Rotation Obstacle 2",drone,command.ROTATE,comm.returnObstacle(2),4)
comm.createAction("Rotation Obstacle 0",drone,command.ROTATE,comm.returnObstacle(0),18)
comm.createAction("Rotation Obstacle 1",drone,command.ROTATE,comm.returnObstacle(1),14)
print(f"The battery of drone {drone.getName()} is: {drone.getBattery()}")
comm.createAction("Inspection Obstacle 6",drone,command.INSPECT_CAMERA,comm.returnObstacle(6))
comm.createAction("Rotation Obstacle 7",drone,command.ROTATE,comm.returnObstacle(6),3)
comm.createAction("Inspection Obstacle 7",drone,command.INSPECT_CAMERA,comm.returnObstacle(7))
comm.createAction("Inspection Obstacle 1",drone,command.INSPECT_CAMERA,comm.returnObstacle(1))
print(f"The battery of drone {drone.getName()} is: {drone.getBattery()}")
comm.returnToBase("Return to Base",drone)

comm.display()
