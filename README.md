# Heuristic Approaches for Heterogeneous Vehicle Routing Problem with 2D Vector Demands

## Project Motivation

This project serves as the culmination of the Heuristic Optimization Methods course of Ozyegin University during the Master in Data Science study, showcasing the competencies acquired throughout the term. It delves into a rather unconventional problem domain, incorporating two distinct aspects of vehicle routing problems: fleet heterogeneity and the consideration of 2D vector demands, representing both weight and volume in practical scenarios. The primary objective of this project is to devise efficient and robust heuristics, aiming to deliver swift solutions while also benchmarking the achieved results.

## Install

Python3 has been used for this project. Additional to default libraries that exist in Python3 setup, these packages are also required to run some or at least one of the project files:
* NumPy
* Pandas
* itertools

## File Descriptions
The project has been developed in object-oriented way. Thus each file contains a class.

* **Problem Construction:** These files are created to build to problem. Each of them are required to build to problem. *Fleet.py*, *Vehicle.py*, *CustomerManagement.py*.
* **Heuristic solutions:** Each of these files provide a solution for the specified data. Some of them make use of others, for instance to create an initial solution. These files are *ConstructiveHeuristic.py*, *ClosestNeighborInitializer.py*, *ImprovementHeuristic.py*, *SimulatedAnnealing.py*, *AntColony.py*, *AntColony_v2.py*, *DecomposedGenetic.py*.
* **Exact solution:** A mathematical model is developed and implemented by using Cplex Concert Technology. *CplexSolver.py* provides exact solution for the problem and we utilized it as a benchmark.
* **Data Files:** Data files contain two types of files which are fleet information and customer information (demand and location). These files are available in implementation/data folder.

## Project Summary

This study considers a routing problem with a heterogeneous fleet. The fleet size is not limited, and demands are 2D vectors. Thus, this study cares additional contraints for demands unlike the classical vehicle routing problems. The problem is modeled mathematically, and a feasible solution is obtained with Cplex solver. In this study, heuristics are built to get close feasible solutions to Cplex in more reasonable time. Various approaches are developed to investigate their behaviour and parameter tuning routines. Two different constructive heuristics are created, and their effect to improvement heuristics as an initial solutions are analyzed. There are also three different improvement heuristics, to improve an initial solution. Well-known first improvement and best improvement strategies are analyzed in the study. The stochastic approaches while accepting non-improving solutions to prevent stuck are also investigated with simulated annealing algorithm. Finally population based heuristics are also evaluated. Two different graph representation is built to solve the problem. A genetic algorithm is also introduced for future studies but not completed. These study contributes to see heuristic approaches to deal with unusual constraints in an optimization problem. Experiments also show that why heuristic approaches should be used to deal with such complex problems that considerably close, even better, objective values are obtained in significantly less time compared to an exact solver. Moreover, results also show that tuning parameters has great importance and this study provides some pre-knowledge about parameters' effects on performance.

Keywords: heuristic algorithms, NP-hard, VRP, heterogeneous fleet

Full report is avaiable here: 

## Licences and Acknowledgements

All rights are reserved by Taha Huzeyfe Aktas.

Thanks to Burcu Balcık for teaching Heuristic Optimization Methods course and providing support during the project. 

Please warn me about my mistakes or do not hesitate to give inspiring ideas.
