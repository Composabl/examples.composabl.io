from composabl import Sensor

T = Sensor("T", "Temperature inside of the Reactor")
Tc = Sensor("Tc", "Temperature of the cooling jacket fluid")
Ca = Sensor("Ca", "Concentration of the residual raw material (A) in the out of the reactor")
Cref = Sensor("Cref", "Setpoint reference for the concentration of the residual raw material (A) in the out of the reactor")
Tref = Sensor("Tref", "Setpoint reference for the temperature inside of the reactor")

sensors = [T, Tc, Ca, Cref, Tref]
