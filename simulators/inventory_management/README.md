# Inventory Management Discrete Event Simulation

Inventory Management Sim is a Python simulator made from discrete functions using simpy library that manages an inventory system.
Simulated Flow:
* Every step is one day in the factory and we simulate a customer inter_arrival period and a customer demand  when we have customers arriving in the simulated day.
* Factory sell "demand" products to "customer"
* System updates the balance and inventory level
* Decision: Agent will send actions to decide the order cutoff and how many parts will ordered at each day
* Apply delay in order, calculate cost of order, and update inventory level

<br>


Specification:
* Sell products for selling_price : we can only sell products in stock and followed by demand
* Customer inter-arrival period = d~exponential(5)
* Each customer demands D~uniform("customer_demand_min", "customer_demand_max") products
* Order Policy ("order_cutoff", "order_target"): if inventory is x < "order_cutoff", order y = "order_target" - x
* Costs c(y) = "cost_price" * y to order y units
* Delay of L = "delay_days_until_delivery" days until delivery
* Holding cost of h = "holding_cost" items per day

MIMO system:
* 9 sensors (Temperature and Concentration)
* 2 control actions (order_cutoff, order_target)

### Assumptions

## State, Actions, Config and Constraints
Episode = "run_time" steps

### State Variables
* "inventory" " inventory level
* "balance" : balance -= cost_price * num_ordered
* "num_ordered": quantity of items ordered
* "holding_cost": cost to hold item in inventory
* "cost_price": price to order the item
* "delay_days_until_delivery": delay in days until delivery order
* "customer_demand_min": customer min demand
* "customer_demand_max": customer max demand
* "selling_price": item selling price


### Action Variables
* "order_cutoff": threshold value to order (cut), applied in the inventory level
* "order_target": quantity of parts to order

### Config Values
* run_time: time in days that the simulation will run

### Graph
* Inventory level
* Balance History ($)
* Order History

## Building

```bash
docker build -t composabl/sim-inventory-management .
docker run --rm -it -p 1337:1337 composabl/sim-inventory-management
```

## Running from Remote

```bash
docker pull composabl/sim-inventory-management
docker run --rm -it -p 1337:1337 composabl/sim-inventory-management
```

## Rquirements to run Train and Inference
Install this packages in your python env
* composabl-dev==0.5.0.dev23
* matplotlib
* simpy==4.0.2

## References

