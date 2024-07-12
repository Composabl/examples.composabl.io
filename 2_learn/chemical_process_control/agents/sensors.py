from composabl import Sensor

T = Sensor("T", "Temperature inside of the Reactor", lambda obs: obs[0])
Tc = Sensor("Tc", "Temperature of the cooling jacket fluid", lambda obs: obs[1])
Ca = Sensor("Ca", "Concentration of the residual raw material (A) in the out of the reactor", lambda obs: obs[2])
Cref = Sensor("Cref", "Setpoint reference for the concentration of the residual raw material (A) in the out of the reactor", lambda obs: obs[3])
Tref = Sensor("Tref", "Setpoint reference for the temperature inside of the reactor", lambda obs: obs[4])

sensors = [T, Tc, Ca, Cref, Tref]
