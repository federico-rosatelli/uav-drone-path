from uav import command

field = command.NewField(name="Vatican City",verbose=False)
field.CreateField("italy/italy_border.csv",-1)
coordinates = field.GetCoordinates()
drone_path = field.DronePathBorder(max_distance=0.001,json_file="vatican")
drone_path1 = field.DronePathBorder(max_distance=0.003,json_file="vatican")
field.DisplayBorderPath(drone_path,drone_path1,labels=["Vatican 0.001"])
