# linear_search
from memory_profiler import profile
@profile
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
import time
start = time.time()
linear_search([i for i in range(10000000)],2222222)
print(time.time() - start)
