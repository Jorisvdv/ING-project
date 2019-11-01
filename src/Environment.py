"""
Class for creating an environment where a simulation can run in.
This is a small extension of the simpy.Environment which allows
us to add some additional middleware functionality.

@file   src/Environment.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  public
"""

# dependencies
import simpy

class Environment(simpy.Environment):

    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        super().__init__(*args, **kwargs)

        # install a collection of middlewares
        self._middleware = []

    def use(self, middleware):
        """
        Method to install middleware on this environment.

        Parameters
        ----------
        middleware: Middleware
            The middelware to install.

        Returns
        -------
        self
        """

        # install the middleware
        self._middleware.append(middleware)

        # allow chaining
        return self

    def step(self, *args, **kwargs):
        """
        Method that wraps around simpy.Environment.step.
        """

        # we need the current process, which we can pipe
        # to our middleware
        current = self.active_process

        # we need to iterate over the middleware, so we
        # can pipe the active process to that
        for m in self._middleware:
            m.pipe(current)

        # call the original method
        return super().step(*args, **kwargs)

