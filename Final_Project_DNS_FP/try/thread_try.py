# import threading
# import time
#
#
# def worker():
#     for i in range(5):
#         yield
#         print(f"Worker: Step {i}")
#
# # Create a thread and start it
# thread = threading.Thread(target=worker)
# thread.start()
#
# # Main thread continues execution
# for _ in range(5):
#     print("Main Thread: Working")
#     print(thread.join())  # Yield control to the worker thread


import concurrent.futures

def calculate_sum():
    for i in range(5):
        yield i
        print('time:', i)


# Create a ThreadPoolExecutor
executor = concurrent.futures.ThreadPoolExecutor()

# Submit the task to the executor
future = executor.submit(calculate_sum)

# Retrieve the result when it's done
result = future.result()

for _ in range(5):
    print(next(result))

# Shutdown the executor when you're done with it
executor.shutdown()

print(f"Sum of numbers: {result}")

import time
import sys
import threading
from alive_progress import alive_bar

value = 10
def up():
    sys.stdout.write('\x1b[1A')
    sys.stdout.flush()


def down():
    sys.stdout.write('\n')
    sys.stdout.flush()


def task_1():
    global value
    items = range(1000)
    with alive_bar(len(items)) as bar:
        for item in items:
            while True:
                if value == 0:
                    down()
                    bar()
                    time.sleep(0.5)
                    value = 1


def task_2():
    global value
    items = range(2000)
    with alive_bar(len(items)) as bar:
        for item in items:
            while True:
                if value == 1:
                    up()
                    bar()
                    time.sleep(0.5)
                    value = 0


t1 = threading.Thread(target=task_1)
t2 = threading.Thread(target=task_2)

t1.start()
t2.start()