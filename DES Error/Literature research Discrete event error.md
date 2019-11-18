# Literature research: Discrete event modelling

**Author**: Milos Dragojevic
**Date**: November 14 2019

## About

This document contains a series of summaries of papers. The subject of these papers is related to error introduction in discrete event simulation.

## Papers

### Davoli G., Nielsen P., Pattarozzi G., Melloni R. (2013) Practical Considerations about Error Analysis for Discrete Event Simulations Model.

#### https://www.mendeley.com/viewer/?fileId=30051a54-4770-bce3-1456-1504409a87ab&documentId=c7e181d3-64ce-34ec-8ee0-0e4148d1d8b4

#### This paper seems very useful for the study that we are trying to perform.

#### 

### Intro

Stochastic, discrete events, simulation models are widely used to study production and logistic system. Apart from the development, one of the main problem of this approach is to perform the error analysis on the outputs of the simulation model

If we limit our interests on non-terminating simulation, the error analysis can be split into two different parts. The first part consists of individuating the initial transient period and the confidence interval of the outputs. The second part consists of estimating how the transient period and the outputs confidence interval varies when the initial model scenario is changed.

The first part of the problem is widely studied.
Between the proposed techniques Mean Squared Pure Error method, Mosca et al. (1985-1992), should be reminded as a practical method useful to determinate both transient period  and confidence interval.

On the other hand the second part of error analysis problem is not commonly addressed. In fact in some recent simulation handbook (Chung 2004) the advice to quantify the confidence interval for all different simulated scenario is given.

### Method

The aim of this paper is to give some practical guidelines in order to drive the error analysis for discrete event stochastic simulation models. The paper is focused on the study of confidence interval variance related to the variance of simulated scenario. Nowadays, in many practical applications, the calculation potential is large enough to perform “long” simulation run in order to assure to exceed the initial transient period. Much more important is to determinate the confidence interval for the outputs in  different simulated scenario, because overestimate or underestimate these confidence intervals can drive analysts towards a wrong interpretation of the results. 

To address the aim of the paper a quite simple discrete event simulation model is considered and the MSPE (1) is used to es timate outputs confidence interval. Then the simulation are performed according to different scenario and the variance of confidence interval is studied for different outputs.

#### 3.1 Simulation Model 

The simulation model was developed according with the standard EOQ model for single item. A set of stochastic functions, developed in SciLab environment, are used to generate the demand that activates the model. The simulation model was tested performing standard EOQ model with normal distributed demand (where σd  is demand standard deviation) and normal distributed lead time (where σt  is lead time standard deviation).

To evaluate model performances, in terms of achieved service level, a set of  4 Key Performance Indicators (KPI) is defined.

#### 3.2 Design of the Experiments  

To investigate the influence of different parameters on confidence intervals four factors are considered. These four factors are: 
    • Demand distribution; 
    • Lead time distribution; 
    • Ratio Co/Cs ; 
    • SS, safety stocks. 

### Findings

In practice, the effort to check the confidence interval related to discrete event simulation should be done when the modified parameters are not simply numeric. This kind of analysis, thanks to the actual computational resource, is not prohibitive in terms of time when we manage a rather simple model.