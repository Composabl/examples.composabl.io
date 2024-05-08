from composabl import Sensor

x = Sensor("x", "this is the x position of the starship", lambda obs: obs[0])
x_speed = Sensor("x_speed", "this is the speed in the x direction that the starship is headed", lambda obs: obs[1])
y = Sensor("y", "this is the y position of the starship", lambda obs: obs[2])
y_speed = Sensor("y_speed", "this is the speed in the y direction that the starship is headed", lambda obs: obs[3])
angle = Sensor("angle", "this is the angle of the starship", lambda obs: obs[4])
ang_speed = Sensor("ang_speed", "this is rate that the angle is changing", lambda obs: obs[5])

sensors = [x, x_speed, y, y_speed, angle, ang_speed]
