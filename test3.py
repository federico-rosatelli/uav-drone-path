from uav import command

field = command.NewField(name="Italy",verbose=True)
field.CreateField("italy/italy_border.csv",6,formatted="multi")
coordinates = field.GetCoordinates()
drone_path = field.DronePathBorder(max_distance=0.05,json_file="italy")
field.DisplayBorderPath(drone_path)
