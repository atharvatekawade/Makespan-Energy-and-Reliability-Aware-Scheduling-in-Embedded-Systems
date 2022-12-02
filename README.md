# Makespan-Energy-and-Reliability-Aware-Scheduling-in-Embedded-Systems

This problem is of scheduling applications modeled as a directed acyclic graph to minimize total execution time and energy consumption subject to reliability constraints in a multiprocessor embedded system without fault-tolerance (each task is assigned a single processor). In particular, our algorithm (WANMS) performs better than others as reliability constraint gets tighter Our proposed methodology is compared with the following state-of-art algorithms:

1) (ODS, MR, LEC) Dynamic DAG Scheduling on Multiprocessor
Systems: Reliability, Energy, and Makespan - Jing Huang
College of Computer Science and Electronic Engineering, Hunan University, Changsha, China,Key Laboratory for Embedded and Network Computing of Hunan Province, Hunan University, Changsha, China
; Renfa Li; Xun Jiao; Yu Jiang; Wanli Chang: https://ieeexplore.ieee.org/document/9211460
2) (HEFT) Performance-effective and low-complexity task scheduling for heterogeneous computing - H. Topcuoglu
Computer Engineering Department, Marmara University, Istanbul, Turkey
; S. Hariri; Min-You Wu: https://ieeexplore.ieee.org/document/993206
3) (ESRG) Energy-Efficient Fault-Tolerant Scheduling of Reliable Parallel Applications on Heterogeneous Distributed Embedded Systems - Guoqi Xie
College of Computer Science and Electronic Engineering, Hunan University, Hunan, China
; Yuekun Chen; Xiongren Xiao; Cheng Xu; Renfa Li; Keqin Li: https://ieeexplore.ieee.org/document/7938375

## Usage
Clone the repositary and run the command: python main.py -rho -itr -pr -R -smin -smax -ods_start -ods_end -ods_step -wanms_start -wanms_end -wanms_step, the arguments are explained below:

1) rho: Represents the number of parameter for number of nodes of FFT Task graph: n = (2+rho)*2**rho - 1.
2) itr: Represents the number of iterations to run the algorithms, with average results reported at the end.
3) pr: Represents the number of processors in our embedded system.
4) R: Represents the reliability constraint as a factor w.r.t maximum reliability < 1.
5) smin: Represents the lower bound for task computation requirement and edge data.
6) smax: Represents the upper bound for task computation requirement and edge data.
7) ods_start: Represents the starting value of Θ in ODS.
8) ods_end: Represents the ending value of Θ in ODS.
9) ods_step: Represents the value of step from ods_start to ods_end.
10) wanms_start: Represents the starting value of α in WANMS.
11) wanms_end: Represents the ending value of α in WANMS.
12) wanms_step: Represents the value of step from wanms_start to wanms_end.

Upon running the command and successful execution, we get plots for the makespan and energy of different algorithms. 
The reliability plot also includes the reliability constraint for reference. Leave all flags blank for running parameters with default values.
 Sample plots are shown below.

## Results

![Figure_1](https://user-images.githubusercontent.com/64606981/204050563-8500ed54-be62-449a-80d9-204407b059b6.png)
