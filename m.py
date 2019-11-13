import argparse
import sys
from multiprocessing import Queue
import redis
import time
import os

import parsl
from parsl import python_app, bash_app
from parsl.executors import ThreadPoolExecutor
from parsl.executors import HighThroughputExecutor
from parsl.providers import LocalProvider
from parsl.config import Config
from parsl.data_provider.files import File
from concurrent.futures import Future

from redis_q import RedisQueue

import value_server

config_mac = Config(
    executors=[
        ThreadPoolExecutor(label="theta_mpi_launcher"),
        ThreadPoolExecutor(label="local_threads")
    ],
    strategy=None,
)

config = Config(
    executors=[
        HighThroughputExecutor(
            label="theta_mpi_launcher",
            # Max workers limits the concurrency exposed via mom node
            max_workers=2,
            provider=LocalProvider(
                init_blocks=1,
                max_blocks=1,
            ),
        ),
        ThreadPoolExecutor(label="local_threads")
    ],
    strategy=None,
)

def trace(frame, event, arg):
    print("%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno))
    return trace


if __name__ == "__main__":
    #sys.settrace(trace)

    parser = argparse.ArgumentParser()
    parser.add_argument("--redishost", default="127.0.0.1",
                        help="Address at which the redis server can be reached")
    parser.add_argument("--redisport", default="6379",
                        help="Port on which redis is available")
    args = parser.parse_args()

    parsl.load(config_mac)

    value_server = value_server.ValueServer(args.redishost, port=int(args.redisport), database=1)
#    value_server.connect()

    for i in range(4):
        print(f"a{i}", i)
        value_server.set(f"a{i}", i)
    print('Size is really', value_server.size())

    keys = value_server.all_keys()
    print('All keys', keys)

    value_server.flush()
    print('That is it')
