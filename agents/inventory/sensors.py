from composabl import Sensor

inventory_sensor = Sensor("inventory", "")
balance_sensor = Sensor("balance", "")
num_ordered_sensor = Sensor("num_ordered", "")
holding_cost = Sensor("holding_cost", "")
cost_price = Sensor("cost_price", "")
delay_days_until_delivery = Sensor("delay_days_until_delivery", "")
customer_demand_min = Sensor("customer_demand_min", "")
customer_demand_max = Sensor("customer_demand_max", "")
selling_price = Sensor("selling_price", "")

sensors = [inventory_sensor, balance_sensor, num_ordered_sensor, holding_cost, cost_price, delay_days_until_delivery, customer_demand_min, customer_demand_max, selling_price]
