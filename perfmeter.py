import time

all_elapsed = {}
all_call_count = {}

def clock(func):
    def clocked(*args):
        global all_elapsed
        global all_call_count
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        all_elapsed[name] = all_elapsed.get(name,0) + elapsed
        all_call_count[name] = all_call_count.get(name,0) + 1
        return result
    return clocked

def reset_clocks():
    global all_elapsed
    global all_call_count
    all_elapsed = {}
    all_call_count = {}

def dump_clocks():
    print(all_elapsed)
    print(all_call_count)

