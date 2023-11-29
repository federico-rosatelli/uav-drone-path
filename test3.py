from uav import command

field = command.NewField(name="Italy")
field.CreateField("italy/italy_border.csv",6,formatted="multi")
coordinates = field.GetCoordinates()
drone_path = field.DronePathBorder(max_distance=0.3)
field.DisplayBorderPath()
