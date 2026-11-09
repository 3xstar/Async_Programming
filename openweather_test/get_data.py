# threading vs ThreadPoolExecutor

import threading
from concurrent.futures import ThreadPoolExecutor

result = {}
arrays = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

# threading
def worker(i, arr):
    result[i] = sum(arr)

threads: list = [
    threading.Thread(target=worker, args=(i, a))
    for i, a in enumerate(arrays)
]

# Другой способ (C++)
# threads: list = []
# for i, a in enumerate(arrays):
#     t = threading.Thread(target=worker, args=(i, a))
#     threads.append(t)

for t in threads:
    t.start()
for t in threads:
    t.join()
print(result)


# ThreadPoolExecutor
def worker(arr):
    return sum(arr)

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(worker, a) for a in arrays]
    result = [f.result() for f in futures] # Исключения всплывут здесь
    print(result)