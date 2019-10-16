"""
Class for generating a sample distribution of transactions according to a some
seasonality. All distributions are generated through a Poisson distribution
function.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   src/TransactionGenerator.py
"""

# dependencies
from __future__ import division
from scipy.stats import poisson

class TransactionGenerator(object):

    # class defaults
    MINUTE = 60 # seconds
    HOUR = 60 # minutes
    DAY = 24 # hours
    WEEK = 7 # days

    def __init__(self, rpm=1000, seed=42):
        """
        Constructor.

        Parameters
        ----------
        rpm: int
            Expected rate/transactions per minute.
            Default: 1000
        seed: int
            Random state seed to encourage reproducability.
            Default: 42
        """
        self._rpm = rpm
        self._seed = seed

    def minutely(self):
        """
        Method to expose a sample per minute.

        Returns
        -------
        list
        """
        return list(poisson.rvs(mu=self._rpm, size=self.MINUTE, random_state=self._seed))

    def hourly(self):
        """
        Method to expose a sample per hour.

        Returns
        -------
        list
        """
        return list(poisson.rvs(mu=self._rpm * self.MINUTE, size=self.HOUR, random_state=self._seed))

    def daily(self):
        """
        Method to expose a sample per day.

        Returns
        -------
        list
        """
        return list(poisson.rvs(mu=self._rpm * self.MINUTE * self.HOUR, size=self.DAY, random_state=self._seed))

    def weekly(self):
        """
        Method to expose a sample per week.

        Returns
        -------
        list
        """
        return list(poisson.rvs(mu=self._rpm * self.MINUTE * self.HOUR * self.DAY, size=self.WEEK, random_state=self._seed))

# plot when running as main
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    gen = TransactionGenerator()

    # start all subplots
    plt.subplot(321)
    plt.plot(range(gen.MINUTE), gen.minutely())
    plt.xlabel('per minute')
    plt.ylabel('number of transactions')

    plt.subplot(322)
    plt.plot(range(gen.HOUR), gen.hourly())
    plt.xlabel('per hour')
    plt.ylabel('number of transactions')

    plt.subplot(323)
    plt.plot(range(gen.DAY), gen.daily())
    plt.xlabel('per day')
    plt.ylabel('number of transactions')

    plt.subplot(324)
    plt.plot(range(gen.WEEK), gen.weekly())
    plt.xlabel('per week')
    plt.ylabel('number of transactions')

    # plot all seasonalities
    plt.tight_layout()
    plt.show()