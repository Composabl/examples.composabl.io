# Machine Teaching Tutorial
Build an Intelligent Autonomous Agent to Control an Industrial Mixer

## About This Tutorial
You can use Composabl to build powerful [intelligent agents](## "definition") that solve real problems and beat industrial benchmarks and other AI solutions. This tutorial will teach you how to design and build these agents using the [Machine Teaching](## "definition") methodology and the Composabl platform.

### Before You Start
To be ready for this tutorial, you should have already completed the [Try Tutorial](/1_try/), including:

- Setting up your GitHub codespace environment for Composabl
- Receiving and entering your Composabl license key
- Building your first agent with a step by step tutorial

If you have completed those steps, you are ready to learn how to design and build agents for yourself.

### In This Tutorial
This tutorial is built around a case study of an industrial mixer. Through this case study, you will learn how to design agents using modular building blocks, compare the performance of agents built with different design patterns, and then practice building, training, and operating agents in the Composabl platform.

At the end of this tutorial, you will be able to:

1. Describe why different agent designs perform differently for this problem
2.	Visually identify strategy pattern and plan-execute pattern
3.	Explain what kind of tasks strategy versus plan-execute are good for  (importance of different scenarios)
4.	Articulate differences between strategy and plan-execute pattern
5.	Write Python SDK code that defines the agent structure of a strategy pattern or a plan-execute pattern respectively
6.	Operate a trained agent
7.	Continue training a partially trained agent

### Modules

This two-hour training is divided into modules.

1. Machine Teaching Foundations (10 minutes)

    In this module, you will learn fundamentals of the machine teaching methodology. At the end of this module, you will be able to:
    - Define machine teaching
    - Explain when machine teaching is useful
    - List the three steps for designing agents with machine teaching

2. Industrial Mixer Case Study Agents and Benchmarks (20 minutes)

    In this module, you will learn about the industrial mixer use case and review the design and performance of 5 different agents. At the end of this module, you will be able to:
    - Explain the parts of an intelligent agent
    - Explain why different agent designs result in different performance


3. Build the Strategy Pattern Agent (60 minutes)

    In this module, you will build an agent using the stragegy design pattern. At the end of this module, you will be able to:
    - Write Python SDK code that defines the agent structure of a strategy pattern
    - Train an agent and analyze performance based on training data

4. Design Patterns (30 minutes)

    In this module, you will build two different multi-skill agents using the Composabl platform. In this module, you will practice building skills that learn with deep reinforcement learning, matching skills to scenarios, and coding selectors. At the end of this module, you will be able to:

    - Recognize two fundamental design patterns
    - Apply design patterns to problems they can solve
     or a plan-execute pattern respectively
	- Operate a trained agent
    - Continue training a partially trained agent

## Module 1: Machine Teaching Fundamentals
add content here

#### Check Your Understanding

1. Question

    <details>
    <summary>Need a hint? </summary>
    This is a use case for machine teaching because there is a need to balance two competing goals.
    </details>
</br>

## Module 2: Agent Design and Performance

### The Industrial Mixer Case Study

![chemical tanks](./img/tanks.jpg)

#### The Use Case
An industrial mixer manufactures chemical products by stirring raw materials together inside a tank. As the reagents are mixed together, a chemical reaction occurs that creates the end product.

The chemical reaction also produces heat. The hotter the tank is allowed to get, the more efficiently it produces the product, leaving less wasted reagent behind.

But if the liquid in the tank gets too hot, it can cross a thershold known as "thermal runaway" and create conditions where the tank will catch fire or explode.

![tanks on fire](./img/runaway.jpg)

#### Two Competing Goals

As in all Machine Teaching use cases, the "fuzziness" or nuance in this process can be summarized in the form of two separate goals that must be balanced against each other:

1. Produce as much product as possible
2. Eliminate the risk of thermal runaway

The key to balancing these goals is maintaining the right temperature in the tank throughout the reaction, so that it's hot enough to be efficient but cool enough that the thermal runaway threshold is never crossed.

#### Controlling the Temperature in the Tank

This use case has only one control variable. Your agent controls the termperature in the tank by adjusting the temperature of the mixture using a “jacket” filled with coolant.

![diagram of tank](./img/mechanism.png)

If the chemicals get too hot and approach thermal runaway, the coolant temperature can be decreased to bring down the temperature in the tank – but the conversion rate will also decrease.

#### Three Different Phases with Different Control Needs

One of the reasons this use case is complex is that it occurs in three different phases.

1. It starts in a steady state with low temperature and low productivity
2. It goes through a transition period when the temperature can change quickly and unpredictably
3. It ends in a steady state of high but consistent temperature and high productivity

The transition phase is the most unpredictable and challenging to control, with the highest risk of thermal runaway.

[More details of the use case](a)


#### Check Your Understanding

1. Why is this problem a good use case for machine teaching?

    <details>
    <summary>Check answer </summary>
    This is a good use case for machine teaching because there is a need to balance two competing goals.
    </details>
</br>

2. What part of the process does the intelligent agent control?

    <details>
    <summary>Check answer </summary>
    Cooling jacket.
    </details>

</br>

3. Why are the phases of the reaction important to agent design?

    <details>
    <summary>Check answer </summary>
    This is a good use case for machine teaching because there is a need to balance two competing goals.
    </details>


### Agent Designs

The design of an agent determines its performance. In this section, we will look at five different agent designs and compare how well they control the reaction to balance the competing goals of maximizing throughput while keeping the temperature at a safe level.

#### Agent 1: Single Skill - Linear Model Predictive Control

The first agent design is the current automation solution, a linear MPC controller. As the current solution, this agent performance is the benchmark for the other designs.

The image below shows an MPC controller represented in the visual system of agent designs. The agent takes in [sensor](## "definition") information about the temperature in the tank and the concentrations of the chemicals. It passs that information to the [skills layer](## "definition") of the agent. The skills layer contains a single programmed skill: control reactor. This skill uses a mathematical model to determine the desired temperature set point for the tank. It also determines the control actions to take to achieve that temperature using the cooling jacket, and outputs those actions as decisions.

![MPC agent structure](./img/MPC-agent.png)

In simulation, this agent's conversion rate was 82%. That means that 82% of the reagents were turned into product, with 18% waste. As you will see when you build this agent later in the tutorial, Composabl provides visualizations of agent performance. The image below shows how the single-skill MPC agent's temperature control performed in simulation.

><br>
>
>**How to read this graph**: This graph shows the performance of the agent through the phases of the process. The x axis represents time, and the y axis shows temperature. The red line is the temperature at which thermal runaway occurs – so we want the agent to keep the temperature well below that point.
>
>The black line is the benchmark – the goal temperature if the reaction is being controlled as well as possible. And the blue area shows the actual temperature as controlled by the agent, over the course of 100 different runs through the simulation. Not every run is the same, so at each point along the x axis, the blue area represents all of the different temperatures from the 100 runs.
>
>
>![MPC agent performance](./img/MPC-graph.png)

You can see from this graph that the MPC agent doesn’t perform very well. It does a good job at the start, in the first steady state. But then once it hits the challenging transition, it hits thermal runaway almost immediately.

When an MPC controller is used to control this process in the real world, a human operator needs to step in and take over control before the automated system lets the temperature cross the thermal runaway threshold.

#### Analyzing Agent Performance: Agent 1

Why did this agent perform the way it did? Like all technologies, model predictive control has a “personality,” a unique set of strengths and weaknesses. Like most math-based control systsems, MPC is a rule follower. It works well in situations governed by mathematical relationships that are straightforward and linear.

As you can see from the graph, MPC works well in the straightforward and linear first phase of the reaction, when the problem is predictable. The agent performance is very close to the benchmark.

However, as the transition phase begins, the agent’s performance starts to fail. Its performance becomes dangerously inconsistent, potentially allowing the temperature to exceed the thermal runaway checkpoint at nearly every point in the reaction.

#### Check Your Understanding

1. What is the "skill" in the single-skill MPC agent?

    <details>
    <summary>Check answer </summary>
   The skill is an MPC controller that uses a mathematical model to d
    </details>
</br>

2. What happens between 5 and 10 minutes on the agent performance graph?

    <details>
    <summary>Check answer </summary>
   The reaction enters into the transition phase, when the relationships between the chemical concentrations and temperature fluctuate in non-linear ways. In some of the training runs, the agent reaches thermal runaway at this point in the reaction.
    </details>

#### Explore Agent 1

Want to go more in depth into Agent 1?  [Explore the agent files](/2_learn/chemical_process_control/agents/deep_reinforcement_learning/) to:

- View the agent design in the SDK
- See what [a programmed skill for an MPC controller](/2_learn/chemical_process_control/agents/model_predictive_control_benchmark/controller.py) looks like
- Try training the agent in your Composabl codespace
- Copy the code to practice building the agent youself.

### Agent 2: Single Skill - Deep Reinforcement Learning

The second agent is also a single-skill agent, but instead of an MPC controller, the single skill that is being used to control the entire reaction is a learned skill trained with deep reinforcement learning.

As with the MPC agent, the sensors take information into the agent, and then that information is passed to a single skill whose job is to control the reaction. But this time, the skill is not making decisions based on math. Instead, it's using AI's unique capability to learn through practice. The DRL skill has been given parameters that reward for how well its results balance the competing goals, and then used simulation to discover and remember the best way to consisently achieve the reward.

![DRL agent](./img/DRL-agent.png)

#### Analyzing Agent Performance - Agent 2

In simulation, the DRL agent had a 90% conversion rate. Here we can see its performance.

![DRL agent performance](./img/DRL-result.png)

Compared to the MPC agent, this result is much better. It stays within the safety threshold every time, and it also controls the steady states very well, staying right on the benchmark line.

But during the transition, the DRL agent goes off the benchmark line quite a bit. It doesn't notice right away when the transition phase begins, staying too long in the lower region of the graph, and then overcorrecting.

Deep reinforcement learning’s “personality” is almost the opposite of MPC’s. Where MPC is a rule follower, DRL works by experimentation, teaching itself how to get results by exploring every possible way to tackle a problem. It has no prior knowledge or understanding of a situation and relies entirely on trial and error. That means that it is potentially well suited to complex processes – like the transition phase - that can’t easily be represented mathematically. On the graph, you can see DRL’s characteristic pattern of wild experimentation, as the agent tries many different approaches to the transition on different runs.

The DRL agent’s skills do better than MPC but still leaves some room for improvement.

#### Check Your Understanding

1. What is the difference between Agent 1 and Agent 2?

    <details>
    <summary>Check answer </summary>
   The skill is an MPC controller that uses a mathematical model to d
    </details>
</br>

2. The designs you just looked at are autonomous intelligent agents, but they don't reflect the complete Machine Teaching methodology, because they don't use all three steps for designing agents with Machine Teaching.

    What are the three steps?
    <details>
    <summary>Check answer </summary>
    1. Divide the process into skills
    2. Orchestrate skills together
    3. Choose the right technology for each skill
    </details>
    </br>

    Which step is missing?

    <details>
    <summary>Check answer </summary>
    Orchestrate skills together is missing, since you can't orchestrate skills in a single-skill agent. But without orchestration, you miss out on a lot of the power of machine teaching to use modularity to drive results.
    </details>


#### Explore Agent 2

Want to go more in depth into Agent 2? [Explore the agent files](/2_learn/chemical_process_control/agents/deep_reinforcement_learning/) to:

- View the code in the SDK
- See [what a teacher looks like](/2_learn/chemical_process_control/agents/deep_reinforcement_learning/teacher.py) for a learned skill for this problem
- Try training the agent in your Composabl codespace
- Copy the code to practice building the agent youself

### Agent 3: Multi-Skill Agent - Strategy Pattern

Multi-skill agents are where you can truly leverage the power of machine teaching. Orchestrating separate, modular skills  together is what allows Machine Teachign to improve performance, compute efficiency, and explanability.

Agent 3 uses a [design pattern](## "Common agent structure known to successfully addresses one or more challenging phenomena") called the [strategy pattern](## "definition"). The strategy pattern is a design in which the agent has several skills to choose from to make the decision, depending on the circumstances. The agent uses a special skill called a [selector](## "definition") that is programmed or trained to distinguish between different [scenarios](## "Scenarios are situations where your agent needs to behave differently to succeed"), conditions with specific characteristics in which different decision-making skills or strategies should be used. Depending on the conditions, the agent will pass control to one of the skills, and it will output the action. The strategy pattern is useful for problems that are challenging because they have variable conditions.

The image below shows a strategy pattern agent with the skills missing. Thinking about the problem, how would you break it into three separate skills to handle different scenarios?

![blank strategy pattern diagram](./img/strategy-blank.png)
    <details>
    <summary>**Need a hint?** </summary>
    There is not one right answer to how to assign skills within an agent design. But a logical way to think about different scenarios for the industrial mixer would be to separate the skills based on the phase of the process.
    </details>


In the strategy pattern design for the industrial mixer, the sensor layer takes in the same information about the condition in the tank as in the other two examples. Then it passes this information to a selector based on the phase of the process. The selector executes the appropriate strategy by assigning control to the appropriate skill. This is the [orchestration](## "definition") of the skills.

What about assigning the right technology to the skills? In this agent, all of the skills, including the selector, are learned with deep reinforcement learning. But unlike the single skill DRL agent, the skills practice separately, each with simulation data specific to its own phase of the process.

![strategy pattern agent](./img/strategy-agent.png)

#### Analyzing Agent Performance - Agent 3

The strategy-pattern agent had 93% conversion and 0% risk of thermal runaway. As you can see from the results, it has better performance in terms of productivity and temperature control that the single-skill DRL agent.

![strategy pattern results](./img/strategy-result.png)


#### Check Your Understanding

1. Agents 2 and 3 use the same technology, deep reinforcement learning. Why do they perform differently?

    <details>
    <summary>Check answer </summary>
   Answer
    </details>

#### Build Agent 3
Later in this tutorial, you will build this agent.

- Skip ahead to build the agent
- [View pre-built agent files](/2_learn/chemical_process_control/agents/strategy_pattern/)



### Agent 4: Multi-Skill Agent - Plan-Execute Pattern

There are many ways to combine technologies to create an intelligent agent, and sometimes two technologies that don’t perform well individually can be very successful when paired together.

This is a design for an agent that strategically leverages the unique capabilities of DRL and MPC to achieve better control than either technology can create alone. The agent does this by putting the two technologies together in skill group, a structure that directs the agent to use the skills in sequence in a two-part decision-making process.

In this example, the DRL skill first determines the set point – that is, it uses its powers of learning and experimentation to ascertain the desired temperature at a given moment in the reaction. It then passes this information on to the MPC skill, which uses its powers of control and execution to direct the agent on what action to take to achieve the desired temperature.

These two skills working together achieve results that are arguably as good or better as the multiple learned skills in a hierarchy. In a head-to-head comparison in the same simulation conditions, the agent with DRL and MPC in a skill group converted a lower percentage of the reagents, but also came less close to thermal runaway.

The decision about which of the two high performing agents to use could be a business decision about whether it is more important to maximize conversion, in which case the multiple learned skills agent would be a better choice, or to prioritize safety, in which case the DRL and MPC agent might be preferable.

While there may not be a clear winner between the two multi-skill agents, they both significantly outperform the single-skill agents. Multiple skills and technologies working together make the difference in creating a successful intelligent agent that can effectively control the process.

## Module 3: Build the Strategy Pattern Agent

### The Strategy Pattern Agent Starter Kit
In this module, you will build the strategy pattern agent from a  starter kit of agent files.


Navigate to the strategy_pattern folder. Inside the folder you'll find the following files:

- ```agent.py``` |
The [agent](## "definition") file organizes all the code for your agent, and is where you will add all the components you develop.

- ```scenarios.py``` | The [scenarios](## "different situations where the agent needs to perform differently to succeed") file identifies the sensor values that define each scenario.

- ```teacher. py``` | The [teacher](## "definition") file contains parameters for how each skill will practice in simulation to get better at the task.

- ```config.py``` | The [config](## "definition") file contains the information that tells the agent how to run, including the Composabl license key and the compute enviornment.

- ```sensors.py``` | The [sensors](## "definition") file organizes the data provided by the simulator or the real system.

This tutorial focuses on building the capabilities of the agent that are unique to the Machine Teaching methodology.
- **Breaking the process into separate modular skills**: Your starter kit agent only has one skill. You will add two additional action skills to complete the strategy pattern.
- **Orchestrating the skills together**: You will add a selector to enable the agent to use the right skill for the right phase of the process. You will also create scenarios for the selector to use.
- **Selecting the right technology for each skill**: You will add the additional skills to the teacher so that they can learn with deep reinforcement learning.

The files that are not directly related to these Machine Teaching capabilites are pre-populated and complete. The other files are partially complete, and require you to add additional code to create agent components. As you put the agent together, you will learn about the function and syntax for these agent components.

This tutorial focuses on the basics. You can also refer to the [full SDK documentation]("link") for additional explanations and resources.

### Steps to Build the Agent

These are the steps you will take the complete the agent:

- Create the scenarios for the additional skills
- Add the additional skills in the teacher
- Create the skills in the agent file
- Add scenarios to the skills in the agent file
- Add skills to the agent file
- Add the selector with the skills in the selector to the agent file

#### Step 1: Create Scenarios

