from uav import command

field = command.NewField(name="BHackFox")
field.CreateField("italy/italy_border.csv",1)
coordinates = field.GetCoordinates()
drone_path = field.DronePathBorder(max_distance=0.002)
field.DisplayBorderPath()
