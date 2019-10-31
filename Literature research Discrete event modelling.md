# Literature research: Discrete event modelling

**Author**: Milos Dragojevic
**Date**: October 31st 2019

## About

This document contains a series of summaries of papers. The subject of these papers is related to discrete event modelling. The summaries should present new insights into discrete event modelling, improving its understanding.

## Papers

### Sanford, A. D. & Moosa, I. A. (2012). A Bayesian network structure for operational risk modelling in structured finance operations. _The Journal of the Operational Research Society_, _63_ (4), pp.431-444

**This paper seems very useful for the study that we are trying to perform.**

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

The Bayesian network construction process is made in steps and cycles.

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