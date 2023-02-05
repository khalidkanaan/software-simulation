# SYSC4005 Project - Manufacturing Facility Simulation

This project aims to simulate and analyze the performance of a manufacturing facility which assembles three different products (P1, P2, and P3) that consist of one or more component types (C1, C2, and C3). Two inspectors clean and repair the components and three workstations (W1, W2, and W3) that assemble the products. 

## Input Data

The following data files are required to run the simulation:
- Inspector 1 inspection time: servinsp1.dat
- Inspector 2 inspection time for component 2: servinsp22.dat
- Inspector 2 inspection time for component 3: servinsp23.dat
- Workstation 1 processing time: ws1.dat
- Workstation 2 processing time: ws2.dat
- Workstation 3 processing time: ws3.dat

In addition, we also have the average buffer occupancy based on historical data is listed below:
- C1 Buffer of Workstation 1: 0.28
- C1 Buffer of Workstation 2: 0.41
- C2 Buffer of Workstation 2: 0.60
- C1 Buffer of Workstation 3: 0.32
- C3 Buffer of Workstation 3: 1.75

## Objectives

The simulation will assess the performance of the manufacturing facility and provide the following information:
- Throughput or product output per unit time
- Average buffer occupancy of each buffer
- Probability (or proportion of time) that each workstation is busy
- Probability (or proportion of time) that each inspector remains "blocked" (and therefore idle)
- Possible improvement of the policy that Inspector 1 follows when delivering C1 components to the different workstations to increase throughput and decrease inspector blocked/idle time.
