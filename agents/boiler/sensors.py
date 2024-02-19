"""
This module contains the definition of the sensors used
in the boiler system.
"""

from composabl import Sensor


y1 = Sensor("y1", "drum level")
y2 = Sensor("y2", "drum pressure")
y3 = Sensor("y3", "drum temperature")
y1ref = Sensor("y1ref", "")
y2ref = Sensor("y2ref", "")
y3ref = Sensor("y3ref", "")
u1 = Sensor("u1", "feed water flow rate")
u2 = Sensor("u2", "fuel flow rate")
u3 = Sensor("u3", "spray flow rate")


sensors = [y1, y2, y3, y1ref, y2ref, y3ref, u1, u2, u3]
