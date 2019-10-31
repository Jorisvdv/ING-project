# Literature research: Discrete event modelling

**Author**: Milos Dragojevic
**Date**: October 31st 2019

## About

This document contains a series of summaries of papers. The subject of these papers is related to discrete event modelling. The summaries should present new insights into discrete event modelling, improving its understanding.

## Papers

### Sanford, A. D. & Moosa, I. A. (2012). A Bayesian network structure for operational risk modelling in structured finance operations. _The Journal of the Operational Research Society_, _63_ (4), pp.431-444

#### This paper seems very useful for the study that we are trying to perform.

This paper is concerned with the design of a Bayesian network structure that is suitable for operational risk modelling.  

Bayesian networks are ideal for analysing an event that occurred and predicting the likelihood that any one of several possible known causes was the contributing factor.

The model's structure is designed specifically from the perspective of a business unit operational risk manager whose role is to measure, record, predict, communicate, analyse and control operational risk within their unit.

The problem domain modelled is a functioning structured finance operations unit within a major Australian bank.
The network model design incorporates a number of existing human factor frameworks to account for human error and operational risk events within the domain. The design also supports a modular structure, allowing for the inclusion of many operational loss event types, making it adaptable to different operational risk environments.

This last paragraph is intriguing since we want to model a banking system where many potential events could occur and need to be taken into consideration. The problems that they encountered are:

- Payments made to incorrect beneficiaries, and/or for an incorrect amount, and/or for an incorrect value date. 
- Regulatory breach such as regulatory reporting or account segregation.
- Failure to enforce its rights or meet its obligations to counterparties over the life of a deal. 
- Exposure capture. This is the risk that the terms of a transaction or details of a counterparty /security are not recorded accurately in the Bank's systems, resulting in a misunderstanding of the risk profile.

#### The Bayesian network construction process is made in steps and cycles.

- Step 1, Structural development and evaluation:

    -  identify all of the relevant risk driver events, their causal relations, and the query, hypothesis or operational loss event variables.

- Step 2, Probability elicitation and parameter estimation:

    -  involves defining the probability distributions of the nodes and setting their parameter values.

- Step 3, Model validation:

    - **most problematic step**
    -  How does one validate a model constructed largely through the subjective opinion of experts?
        - Elication review
        - sensitivity analysis
        - case evaluation


#### Structural development

- What operational risk queries should the model be able to answer?
- What operational risk categories and events should be included in the model?
- What are the main risk drivers in SFO for operational risk events?
- What are the causal relations between risk drivers and risk events? 
- What are the key performance indicators (KPIs) for the SFO domain?

The paper developed a network structure for the modelling of operational risk based on a functioning SFO unit within a major Australian bank.
The dominant perspective used in developing this model structure is that of human error and its role in contributing to operational losses. Within the unit under investigation, human action plays a dominant role in the transaction processes, which makes it logical to emphasize human error.

The model is designed to generate probabilities of operational loss events by consideration of interaction between the working environment, transaction processes and their effect on the generation of human errors. A valuable feature of the model is its modularity, which provides the opportunity to add other types of operational loss events as necessary.


### Babulak, E., & Wang, M. (2008 ). Discrete Event Simulation _International Journal of Online Engineering (iJOE)_. _4_ (60)

Managers have started to use discrete event simulation for the service industries. In particular for banking and finance services. Some examples are:

- call center modeling & simulation
- bank branch modeling & simulation
- simulation of vehicle routing (cash carriage services) and number of cash carriage services per routing
- simulation study of cash management of ATM such as minimum re-order point, optimum budget and so on.

#### Modeling of service operations

*1)* Process flow: A manufacturing process is always associated with physical flows of
materials/components and therefore can be easily identified. It may not be the case for
many service applications where business activities are information-based and triggered by
an external or internal event such as a written or oral request. The current solution is to use
a business process mapping tool to capture the business process and then convert the
process model to the discrete event simulation model [KBSI, Lanner].
*2)* Process related data such as processing time: In a manufacturing company, industrial
engineers are responsible for time study, setting processing time and balancing flow. Most
of service companies do not hire industrial engineers or have equivalent position within
organizations. As a result, much of the process related data are not readily available.
*3)* Knowledge workers: In many service companies, employees work primarily with
information or develop and use knowledge. They are knowledge workers, a term coined by
Peter Drucker. A knowledge worker tends to be self-motivated, work interactively and
make decisions constantly. How to represent knowledge workers and human-decision
making process in discrete event simulation remains a subject under study [10].
In the postindustrial economy, the service sector makes up more than half of the American
economy. Since mid 1990s, the sector has generated almost all of the US economy increases
in employment. Knowledge workers are now estimated to outnumber all other workers in
North America by at least a four to one margin [11]. Thus, there is a great potential for
discrete event simulation technologies in service sector. However, new approach and
techniques are required to model and simulate knowledge workers and their decisionmaking
processes.
