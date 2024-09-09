# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from composabl_core.agent.sensor import Sensor

counter_value = Sensor("counter", "The value of the counter", lambda sensors: sensors["counter"])
text_value = Sensor("text", "The value of the text", lambda sensors: sensors["text"])

sensors_text = [text_value, counter_value]
