from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt

def controller():
    # Two product at a time
    m = GEKKO()
    nt = 10
    #m.time = np.linspace(0,nt,2)
    m.time = [i for i in range(0,nt)]

    #variables
    u1 = m.MV(value=0, lb=0, ub=1, integer=True) #input
    u2 = m.MV(value=0, lb=0, ub=1, integer=True) #input
    u3 = m.MV(value=0, lb=0, ub=1, integer=True) #input

    # Variables
    q = m.SV(value=0, lb=0, integer=True) #state variable
    wt = m.SV(value=0, lb=0, ub=480, integer=True)
    r = m.SV(value=0, lb=0, ub=5000, integer=True)

    ## CONSTRAINTS
    # STATUS = 0, optimizer doesn't adjust value;  STATUS = 1, optimizer can adjust
    u1.STATUS = 1
    u2.STATUS = 1
    u3.STATUS = 1

    # DMAX = maximum movement each cycle
    #u1.DMAX = 1.0
    #u2.DMAX = 1.0
    #u3.DMAX = 1.0

    prices = {
        1: 5,
        2: 7,
        3: 10
    }

    quantities = {
        1: 12,
        2: 6,
        3: 1
    }


    # Equations
    m.Equations([q.dt() == 12*u1 + 6*u2 + 1*u3,
                wt.dt() == m.max2(m.max2(28*u1,57*u2),80*u3),
                wt <= 480,
                r.dt() == 12*5*u1 + 6*7*u2 + 1*10*u3,
                u1 + u2 + u3 <= 2
                ])



    m.Maximize(r) # Objective function

    m.options.IMODE = 6 # optimal control mode
    #m.options.IMODE = 9 #dynamic optimization
    m.solve(disp=False) # solve

def plot_results(m, u1, u2, u3, r, wt):
    plt.figure(1) # plot results
    plt.subplot(3,1,1)
    plt.plot(m.time,u1.value,'k.-',label=r'$u_1$')
    plt.plot(m.time,u2.value,'b.-',label=r'$u_2$')
    plt.plot(m.time,u3.value,'r.-',label=r'$u_3$')
    plt.legend(loc='best')

    plt.subplot(3,1,2)
    plt.plot(m.time,r.value,'k.-',label=r'$q$')
    plt.ylabel('Revenue')

    plt.subplot(3,1,3)
    plt.plot(m.time,wt.value,'b--',label=r'$wt$')
    plt.legend(loc='best')

    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.show()