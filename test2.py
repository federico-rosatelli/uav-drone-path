from uav import command

comm = command.NewCommand("example/grid2.txt")
drone = command.NewDrone(comm,"Thermal","LittleF0x",[command.INSPECT_CAMERA,command.INSPECT_THERMAL,command.ROTATE],100)
comm.setBase((0,3,5))
comm.createAction("Rotation Obstacle 0",drone,command.ROTATE,comm.returnObstacle(0),6)
comm.createAction("Rotation Obstacle 1",drone,command.ROTATE,comm.returnObstacle(1),1)
comm.createAction("Inspection Obstacle 1",drone,command.INSPECT_CAMERA,comm.returnObstacle(1))
comm.createAction("Rotation Obstacle 2",drone,command.ROTATE,comm.returnObstacle(2),5)
print(f"The battery of drone {drone.getName()} is: {drone.getBattery()}")
comm.returnToBase("Return to Base",drone)

comm.display()