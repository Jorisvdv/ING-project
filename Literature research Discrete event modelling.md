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


### Babulak, E., & Wang, M. (2008 ). Discrete Event Simulation _International Journal of Online Engineering (iJOE) _, _4_ (60)

Discrete-event simulation represents modeling, simulating, and analyzing systems utilizing
the computational and mathematical techniques, while creating a model construct of a
conceptual framework that describes a system. The system is father simulates by performing
experiment(s) using computer implementation of the model and analyzed to draw
conclusions from output that assist in decision making process. Discrete event simulation
technologies have been extensively used by industry and academia to deal with various
industrial problems. By late 1990s, the discrete event simulation was in doldrums as global
manufacturing industries went through radical changes. The simulation software industry
also went through consolidation. The changes have created new problems, challenges and
opportunities to the discrete event simulation. This chapter reviews the discrete event
simulation technologies; discusses challenges and opportunities presented by both global
manufacturing and the knowledge economy. The authors believe that discrete event
simulation remains one of the most effective decision support tools but much need to be
done in order to address new challenges. To this end,