# Poisson distribution
This document explains why a poisson distribution is suitable for simulating
user activity on a server.

## Assumptions
The Poisson distribution is an appropriate model if the following assumptions are true:

- k is the number of times an event occurs in an interval and k can take values 0, 1, 2, ....
- The occurrence of one event does not affect the probability that a second event will occur. That is, events occur independently.
- The average rate at which events occur is constant.
- Two events cannot occur at exactly the same instant; instead, at each very small sub-interval exactly one event either occurs or does not occur.

Or
- The actual probability distribution is given by a binomial distribution and the number of trials is sufficiently bigger than the number of successes one is asking about - (see Related distributions).
- If these conditions are true, then k is a Poisson random variable, and the distribution of k is a Poisson distribution.

Within an hour, transactions probably happen in a constant rate.