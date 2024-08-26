# Industrial Boiler

Industrial Boiler Sim is a Python simulator made from Transfer functions that control the Level, Temperature and Pressure of an Industrial Boiler.<br>
This model simulates an Industrial Boiler with the objective to control their main process variables (Level, Temperature, Pressure) and environmental variables (NOx emissions). One of the main optimizations that can be done with this simulator is reducing NOx emissions.

![industrial boiler](https://www.process-heating.com/ext/resources/Issues/2016/January/3-PH0116-Arizona-Boiler-cut-away-view.jpg?t=1450881722&width=1080)

An industrial boiler is a closed vessel used to produce steam or hot water for industrial and manufacturing processes. Boilers can burn a variety of fuels, including coal, oil, natural gas, and biomass,this Boiler simulator works with Natural Gas as fuel. As with any complex machinery, efficient operation requires managing several critical variables to ensure safety, efficiency, and longevity. For this simulation we are manipulating these variables:

1. Temperature: Maintaining the appropriate temperature is crucial for achieving optimal combustion and efficiency. Too high or too low temperatures can affect the combustion process and energy transfer.

2. Tank Level: The water level inside the boiler drum is essential for safety and efficiency. If the level is too low, it can expose the boiler tubes, causing them to overheat and possibly rupture. Conversely, too high a level can lead to inefficient steam generation and may carry water into the steam pipeline (water carryover).

3. Pressure: Boilers operate under pressure, which is vital for producing steam at the desired temperature and ensuring the steam is delivered efficiently to where it's required. Maintaining proper pressure is also crucial for safety as overpressure can lead to boiler explosions.

4. NOx Emissions: Nitrogen oxides (NOx) are harmful pollutants resulting from combustion processes. Industrial boilers, being significant contributors, must control and reduce their NOx emissions to meet environmental regulations and reduce air pollution.

A simplified Linear Time Invariant (LTI) system of a boiler system is used as the starting point of the simulation. This work is based on the Multivariable Robust Controller Design for a Boiler System[1], a published paper written in the Department of Electrical and Computer Engineering at University of Alberta. This paper outlines the process of designing a robust controller. In this process, the LTI system was derived using the MATLAB Systems Identification Toolbox, focusing on the relationship between the following inputs (States) and outputs (Actions).

![industrial boiler sim](img/boiler_diagram.jpg)

## Transfer Function Equations

MIMO system:

- 5 sensors (Temperature, Level, Flowrate, Pressure, NOx emissions)
- 3 control action (Setpoints)

### Assumptions

## State, Actions, Config and Constraints

Episode = 120 steps
dt = 12 min

### State Variables

| Description                | State             | Continuous Value | Units    |
| -------------------------- | ----------------- | ---------------- | -------- |
| Drum Level                 | y1                | [0.1, 12]        | [m]      |
| Drum Pressure              | y2                | [10, 800]        | [MPa]    |
| Steam Temperature          | y3                | [10, 800]        | [C°]     |
| Drum Level Setpoint        | y1ref             | [0.1, 12]        | [m]      |
| Drum Pressure Setpoint     | y2ref             | [10, 800]        | [MPa]    |
| Steam Temperature Setpoint | y3ref             | [10, 800]        | [C°]     |
| Nox Emision Yearly Rate    | nox_emissions_yr  | [0, 20]          | [kg/yr]  |
| Nox Emision Hourly Rate    | nox_emissions_hr  | [0, 0.2]         | [kg/hr]  |
| Nox Emision Minute Rate    | nox_emissions_min | [0, 0.1]         | [kg/min] |
| Total Emissions            | total_emissions   | [0, 5]           | [kg]     |
| Feedwater Flowrate         | u1                | [0, 120]         | [kg/s]   |
| Fuel Flowrate              | u2                | [0, 7]           | [kg/s]   |
| Attemperator Flowrate      | u3                | [0, 10]          | [kg/s]   |

Additional Details on addes states:

- Emissions model that is dependent to the fuel flowrate was added to this model so estimate emission production.
- Calculation of current input based on rate change from agent.

#### List:

- y1 - Drum Level
- y2 - Drum Pressure
- y3 - Drum Temperature
- y1ref, y2ref, y3ref - Setpoints
- u1 - Feed water flowrate
- u2 - Fuel flowrate
- u3 - Spray Flowrate
- rms - root mean square error between y1 and y1ref
- eff_nox_red - Efficiency of NOx reduction system
- nox_emissions - instant NOx emission
- total_nox_emission - total NOx emission

### Action Variables

| Description                     | Action | Range         | Units    |
| ------------------------------- | ------ | ------------- | -------- |
| Change in Feedwater Flowrate    | dU1    | [-50, 50]     | $kg/s^2$ |
| Change in Fuel Flowrate         | dU2    | [-1.02, 1.02] | $kg/s^2$ |
| Change in Attemperator Flowrate | dU3    | [-0.5, 0.5]   | $kg/s^2$ |

### Config Variables

- signal - choose with setpoint variable to control
  - "y1" - Control Level
  - "y2" - Control Pressure
  - "y3" - Control Temperature
- eff_nox_red - Efficiency of NOx reduction system

### Constraints:

**State Constraints:** One importnat constraint to consider in this simulation is that the state space representation of the boiler system is defined based on specific operating points. Training outside of these operation points will not reflect real behavior. Setpoints are as follows:

$u_0 =\begin{Bmatrix}
    40.68 \\
    2.102 \\
    0\end{Bmatrix}$

$y_0 =\begin{Bmatrix}
    1.0 \\
    6.45 \\
    466.7\end{Bmatrix}$

**Input Constraints:** There are physical contraints on the actuators defined in the original research paper. Each pump has a physical input limit, and the fuel pump has a rate limit.

$0 \leq u_1 \leq 120$

$0 \leq u_2 \leq 7$

$0 \leq u_3 \leq 10$

$-0.017 \leq du_2 \leq 0.017 $

#### List:

- -20 < du1 < 20
- -0.017 < du2 < 0.017
- -2 < du3 < 2
- 0 < u1 < 120
- 0 < u2 < 7
- 0 < u3 < 10

## **Results**

### **Python Simulation Results**

| Description                                                  | States Results                              | Actions |
| ------------------------------------------------------------ | ------------------------------------------- | ------- |
| Python Simulation - Control of a drum pressure step response | ![](img/Python-Benchmark-States.jpg)        |         |
| Python - Control boiler and reduce emissions                 | ![](img/Python-ReducedEmissions-States.jpg) |         |

## **References**

[1] Tan, W., Chen, T. Multivariable robust controller design for a boiler system. 2002 - Articles in Control Systems Technology, IEEE Transactions - October 2022
