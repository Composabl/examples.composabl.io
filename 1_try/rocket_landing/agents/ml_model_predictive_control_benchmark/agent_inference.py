import casadi
from casadi import *
import numpy as np

from matplotlib import pyplot as plt, rc
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter

from ipywidgets import IntProgress
from IPython.display import display


##DYNAMICS

g = 9.8
m = 100000 # kg
min_thrust = 880 * 1000 # N
max_thrust = 1 * 2210 * 1000 #kN

length = 50 # m
width = 10

# Inertia for a uniform density rod
I = (1/12) * m * length**2

deg_to_rad = 0.01745329

max_gimble = 20  * deg_to_rad
min_gimble = -max_gimble

# x[0] = x position (m)
# x[1] = x velocity (m/)
# x[2] = y position (m)
# x[3] = y velocity (m/s)
# x[4] = angle (rad)
# x[5] = angular velocity (rad/s)

# u[0] = thrust (percent)
# u[1] = thrust angle (rad)

def x_dot(x, u):
    theta = x[4]

    thrust = u[0]
    thrust_angle = u[1]

    # Horizontal force
    F_x = max_thrust * thrust * sin(thrust_angle + theta)
    x_dot = x[1]
    x_dotdot = (F_x) / m

    # Vertical force
    F_y = max_thrust * thrust * cos(thrust_angle + theta)
    y_dot = x[3]
    y_dotdot = (F_y) / m - g

    # Torque
    T = -length/2 * max_thrust * thrust * sin(thrust_angle)
    theta_dot = x[5]
    theta_dotdot = T / I

    return [x_dot, x_dotdot, y_dot, y_dotdot, theta_dot, theta_dotdot]




## OPTM PROBLEM

# Make an optimization problem
opti = casadi.Opti()

# Set the number of steps and the timestep (dt)
steps = 400
t_step = 0.04

# Generate the array of state and control vectors
x = opti.variable(steps, 6)
u = opti.variable(steps, 2)
# t_step = opti.variable(1, 1)

# opti.subject_to( opti.bounded(0.01, t_step, 0.2))

x[0, :] = [0, 0, 1000, -80, -np.pi/2, 0]
x[steps-1, :] = [0, 0, 0, 0, 0, 0]

# u[steps-1, 1] = 0

# Cost function
opti.minimize(sumsqr(u[:, 0]) +  sumsqr(u[:, 1]) + 2 * sumsqr(x[:, 5]))

# Set dynamics constraints
for i in range(0, steps-1):
    opti.subject_to( x[i+1, 0] - x[i, 0] == x_dot(x[i, :], u[i, :])[0] * t_step )
    opti.subject_to( x[i+1, 1] - x[i, 1] == x_dot(x[i, :], u[i, :])[1] * t_step )

    opti.subject_to( x[i+1, 2] - x[i, 2] == x_dot(x[i, :], u[i, :])[2] * t_step )
    opti.subject_to( x[i+1, 3] - x[i, 3] == x_dot(x[i, :], u[i, :])[3] * t_step )

    opti.subject_to( x[i+1, 4] - x[i, 4] == x_dot(x[i, :], u[i, :])[4] * t_step )
    opti.subject_to( x[i+1, 5] - x[i, 5] == x_dot(x[i, :], u[i, :])[5] * t_step )

# Set bounds constraints
for i in range(0, steps):
    opti.subject_to( opti.bounded(0.4, u[i, 0], 1))
    opti.subject_to( opti.bounded(min_gimble, u[i, 1], max_gimble))

# Select solver
opti.solver('ipopt')

# Solve! Might take ~ 20 seconds
sol = opti.solve()


##PLOT

# Plot state
plt.subplot(511)
plt.plot(sol.value(x)[:, 0], label = "x")
plt.plot(sol.value(x)[:, 1], label = "x_dot")
plt.plot(sol.value(x)[:, 2], label = "y")
plt.plot(sol.value(x)[:, 3], label = "y_dot")
plt.plot(sol.value(x)[:, 4], label = "theta")
plt.plot(sol.value(x)[:, 5], label = "theta_dot")
plt.legend()

# Plot control input
plt.subplot(512)
plt.plot(sol.value(u)[:, 0], label = "thrust %")
plt.plot(sol.value(u)[:, 1], label = "angle")
plt.legend()

plt.subplot(513)
plt.plot(sol.value(x)[:, 1], label = "x_dot")
plt.plot(sol.value(x)[:, 3], label = "y_dot")
plt.legend()

plt.subplot(514)
plt.plot(sol.value(x)[:, 2],sol.value(x)[:, 4], label = "theta vs y")
plt.legend()

plt.subplot(515)
plt.plot(sol.value(x)[:, 2],sol.value(x)[:, 3], label = "y_dot vs y")
plt.legend()

plt.show()

final_time_step = sol.value(t_step);
duration = sol.value(t_step) * steps

print(sol.value(t_step))
print(sol.value(t_step * steps))



## PLOT 2

print("Generating Animation")
f = IntProgress(min = 0, max = steps)
display(f)

x_t = sol.value(x)
u_t = sol.value(u)

fig = plt.figure(figsize = (5, 5), constrained_layout=False)

ax1 = fig.add_subplot(111)

ln6, = ax1.plot([], [], '--', linewidth = 2, color = 'orange')

ln2, = ax1.plot([], [], linewidth = 2, color = 'tomato')
ln1, = ax1.plot([], [], linewidth = 5, color = 'lightblue')

#plt.axis('off')
plt.tight_layout()

ax1.set_xlim(-400, 400)
ax1.set_ylim(-50, 1000)
ax1.set_aspect(1)

def update(i):
  rocket_theta = x_t[i, 4]

  rocket_x = x_t[i, 0]
  rocket_x_points = [rocket_x + length/2 * sin(rocket_theta), rocket_x - length/2 * sin(rocket_theta)]

  rocket_y = x_t[i, 2]
  rocket_y_points = [rocket_y + length/2 * cos(rocket_theta), rocket_y - length/2 * cos(rocket_theta)]

  ln1.set_data(rocket_x_points, rocket_y_points)


  thrust_mag = u_t[i, 0]
  thrust_angle = -u_t[i, 1]

  flame_length = (thrust_mag) * 50


  flame_x_points = [rocket_x_points[1], rocket_x_points[1] + flame_length * sin(thrust_angle - rocket_theta)]
  flame_y_points = [rocket_y_points[1], rocket_y_points[1] - flame_length * cos(thrust_angle - rocket_theta)]

  ln2.set_data(flame_x_points, flame_y_points)

  ln6.set_data(x_t[:i, 0], x_t[:i, 2])

  f.value += 1

anim = FuncAnimation(fig, update, np.arange(0, steps-1, 1), interval= final_time_step * 1000)

anim
