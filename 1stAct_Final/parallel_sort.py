import random
import time
from multiprocessing import Process, Queue


def merge(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


def merge_sort(arr):
    if len(arr) < 2:
        return arr
    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))


def worker(data, idx, q):
    q.put((idx, merge_sort(data)))


def combine(chunks):
    while len(chunks) > 1:
        nxt = []
        for i in range(0, len(chunks), 2):
            if i + 1 < len(chunks):
                nxt.append(merge(chunks[i], chunks[i + 1]))
            else:
                nxt.append(chunks[i])
        chunks = nxt
    return chunks[0]


def parallel_sort(data, k=4):
    n = len(data)
    size = n // k
    q = Queue()
    procs = []

    for i in range(k):
        s = i * size
        e = n if i == k - 1 else s + size
        p = Process(target=worker, args=(data[s:e], i, q))
        p.start()
        procs.append(p)

    parts = [q.get() for _ in range(k)]

    for p in procs:
        p.join()

    parts.sort(key=lambda x: x[0])
    return combine([p[1] for p in parts])


def check(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def bench(tag, arr):
    t0 = time.time()
    res = parallel_sort(arr)
    t1 = time.time()
    elapsed = t1 - t0
    print(f"{tag:<18} | {len(arr):>9,} | {elapsed:.4f}s | ok={check(res)}")
    return elapsed


if __name__ == "__main__":
    print("Parallel Merge Sort (4 processes)\n")

    stats = {}

    datasets = {
        "small random": [random.randint(1, 10**6) for _ in range(1_000)],
        "medium random": [random.randint(1, 10**6) for _ in range(100_000)],
        "large random": [random.randint(1, 10**6) for _ in range(1_000_000)],
        "sorted": list(range(100_000)),
        "reversed": list(range(100_000, 0, -1)),
    }

    for name, data in datasets.items():
        stats[name] = bench(name, data)

    print("\n" + "-" * 55)

    print("\nSummary")
    for name, t in stats.items():
        print(f"{name:<18} : {t:.4f}s")
