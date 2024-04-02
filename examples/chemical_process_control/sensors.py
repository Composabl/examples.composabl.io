from composabl import Sensor

T = Sensor("T", "", lambda obs: obs[0])
Tc = Sensor("Tc", "", lambda obs: obs[1])
Ca = Sensor("Ca", "", lambda obs: obs[2])
Cref = Sensor("Cref", "", lambda obs: obs[3])
Tref = Sensor("Tref", "", lambda obs: obs[4])

sensors = [T, Tc, Ca, Cref, Tref]
