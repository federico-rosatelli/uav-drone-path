from uav import command

field = command.NewField(name="Vatican City",verbose=True)
field.CreateField("italy/italy_border.csv",6,formatted="multi")
coordinates = field.GetCoordinates()
drone_path = field.DronePathBorder(max_distance=0.0037,json_file="italy.json")
field.DisplayBorderPath()
