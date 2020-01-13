"""
Toy example on how introduce error using PreemptiveResource
"""

from random import randint
import simpy

timeout_time = 30
error_duration = 100
latency = (25, 32)


def message(env, server, i):
    # Enter all message processes here, for now random timeout
    try:
        process_time = randint(latency[0], latency[1])
        with server.request(priority=1) as req:  # Generate a request event
            yield req                    # Wait for access
            yield env.timeout(process_time)
        print(f"INFO: message {i} processed at time {env.now}, duration {process_time}")
    except simpy.Interrupt as interrupt:
        print(f"ERROR: message {i} {interrupt.cause} at time {env.now}")


def message_generator(env, server):
    for i in range(1000):

        message_process = env.process(message(env, server, i))
        yield message_process | env.timeout(timeout_time)

        # If message not triggered then timeout is past
        if (not message_process.triggered):
            message_process.interrupt("timeout")


def error_generator(env, server):
    while True:
        yield env.timeout(randint(100, 250))
        print(f"LOG_ERROR_Start error at time {env.now}")
        with server.request(priority=0) as req:  # Generate a request event
            yield req                               # Wait for access
            yield env.timeout(error_duration)
            print(f"LOG_ERROR_End error at time {env.now}")


if __name__ == "__main__":
    env = simpy.Environment()
    print(env)
    serv = simpy.PreemptiveResource(env, capacity=1)
    env.process(error_generator(env, serv))
    env.process(message_generator(env, serv))
    env.run(until=1000)
