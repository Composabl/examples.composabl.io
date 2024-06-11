from composabl import Sensor

y1 = Sensor("y1", "Temperature Sensor - Control Y1", lambda obs: obs[0])
y1ref = Sensor("y1ref", "Temperature Setpoint - Y1 Reference ", lambda obs: obs[1])
u1 = Sensor("u1", "Manipulated Variables", lambda obs: obs[2])
rms = Sensor("rms", "Root Mean Squared Error", lambda obs: obs[3])

sensors = [y1, y1ref, u1, rms]
