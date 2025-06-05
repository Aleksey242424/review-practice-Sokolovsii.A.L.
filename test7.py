# binary_search (предварительно отсортировать массив!)
from memory_profiler import profile
@profile
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
import time
start = time.time()
arr = list(range(1, 10000000))
target = 2222222
binary_search(arr, target)
print(time.time() - start)
