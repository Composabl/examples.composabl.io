from composabl import Sensor

inventory_sensor = Sensor("inventory", "Inventory sensor", lambda obs: obs[0])
balance_sensor = Sensor("balance", "Balance sensor", lambda obs: obs[1])
num_ordered_sensor = Sensor("num_ordered", "Number of ordered items sensor", lambda obs: obs[2])
holding_cost_sensor = Sensor("holding_cost", "Holding cost sensor", lambda obs: obs[3])
cost_price_sensor = Sensor("cost_price", "Cost price sensor", lambda obs: obs[4])
delay_days_until_delivery_sensor = Sensor("delay_days_until_delivery", "Delay days until delivery sensor", lambda obs: obs[5])
customer_demand_min_sensor = Sensor("customer_demand_min", "Customer demand min sensor", lambda obs: obs[6])
customer_demand_max_sensor = Sensor("customer_demand_max", "Customer demand max sensor", lambda obs: obs[7])
selling_price_sensor = Sensor("selling_price", "Selling price sensor", lambda obs: obs[8])


sensors = [inventory_sensor, balance_sensor, num_ordered_sensor, holding_cost_sensor, cost_price_sensor, delay_days_until_delivery_sensor, customer_demand_min_sensor, customer_demand_max_sensor, selling_price_sensor]
