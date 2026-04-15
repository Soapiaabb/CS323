import random
import time
from multiprocessing import Process, Queue

def merge(left, right):
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))

def sequential_sort(data):
    return merge_sort(data)

def _sort_worker(chunk, chunk_id, q):
    q.put((chunk_id, merge_sort(chunk)))


def _k_way_merge(chunks):
    while len(chunks) > 1:
        next_level = []
        for i in range(0, len(chunks), 2):
            if i + 1 < len(chunks):
                next_level.append(merge(chunks[i], chunks[i + 1]))
            else:
                next_level.append(chunks[i])
        chunks = next_level
    return chunks[0]


def parallel_sort(data, num_processes=4):
    n = len(data)
    chunk_size = n // num_processes
    q = Queue()
    processes = []
    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else n
        p = Process(target=_sort_worker, args=(data[start:end], i, q))
        processes.append(p)
        p.start()
    raw = [q.get() for _ in range(num_processes)]
    for p in processes:
        p.join()
    raw.sort(key=lambda x: x[0])
    return _k_way_merge([c for _, c in raw])


def sequential_search(data, target):
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1

def _search_worker(sub_data, target, q, offset):
    for i in range(len(sub_data)):
        if sub_data[i] == target:
            q.put(offset + i)
            return
    q.put(-1)


def parallel_search(data, target, num_processes=4):
    n = len(data)
    chunk_size = n // num_processes
    q = Queue()
    processes = []
    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else n
        p = Process(target=_search_worker, args=(data[start:end], target, q, start))
        processes.append(p)
        p.start()
    raw = [q.get() for _ in range(num_processes)]
    for p in processes:
        p.join()
    found = [r for r in raw if r != -1]
    return min(found) if found else -1

def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def time_it(fn, *args):
    """Returns (result, elapsed_seconds)."""
    start = time.time()
    result = fn(*args)
    return result, time.time() - start

def benchmark_sorting(label, data):
    print(f"\n  Sorting  |  {label}  |  {len(data):>9,} elements")
    print(f"  {'-'*48}")

    sorted_seq, t_seq = time_it(sequential_sort, data[:])
    valid_seq = is_sorted(sorted_seq)
    print(f"  Sequential : {t_seq:.4f}s   valid={valid_seq}")

    sorted_par, t_par = time_it(parallel_sort, data[:])
    valid_par = is_sorted(sorted_par)
    print(f"  Parallel   : {t_par:.4f}s   valid={valid_par}")

    if t_seq > 0:
        ratio = t_seq / t_par
        faster = "parallel" if ratio > 1 else "sequential"
        print(f"  Ratio seq/par : {ratio:.2f}x  →  {faster} was faster")

    return t_seq, t_par


def benchmark_searching(label, data, target, note=""):
    print(f"\n  Searching |  {label}  |  {len(data):>9,} elements  |  target={target} {note}")
    print(f"  {'-'*48}")

    idx_seq, t_seq = time_it(sequential_search, data, target)
    print(f"  Sequential : {t_seq:.6f}s   index={idx_seq}")

    idx_par, t_par = time_it(parallel_search, data, target)
    print(f"  Parallel   : {t_par:.6f}s   index={idx_par}")

    match = "MATCH" if idx_seq == idx_par else "MISMATCH — CHECK IMPLEMENTATION"
    print(f"  Index agreement : {match}")

    if t_seq > 0:
        ratio = t_seq / t_par
        faster = "parallel" if ratio > 1 else "sequential"
        print(f"  Ratio seq/par : {ratio:.2f}x  →  {faster} was faster")

    return t_seq, t_par


if __name__ == "__main__":
    print("=" * 55)
    print("  Full Benchmark — Sequential vs Parallel")
    print("=" * 55)

    sort_results = {}
    search_results = {}

    #Dataset
    SIZES = {
        "Small  (1K)  ": 1_000,
        "Medium (100K)": 100_000,
        "Large  (1M)  ": 1_000_000,
    }

    print("\n" + "━" * 55)
    print("  SORTING BENCHMARKS")
    print("━" * 55)

    for label, n in SIZES.items():
        data = [random.randint(1, 1_000_000) for _ in range(n)]
        t_seq, t_par = benchmark_sorting(label, data)
        sort_results[label] = (t_seq, t_par)

    print("\n  --- Special Cases (n=100,000) ---")

    already = list(range(1, 100_001))
    t_seq, t_par = benchmark_sorting("Already sorted", already)
    sort_results["Already sorted (100K)"] = (t_seq, t_par)

    reverse = list(range(100_000, 0, -1))
    t_seq, t_par = benchmark_sorting("Reverse sorted", reverse)
    sort_results["Reverse sorted (100K)"] = (t_seq, t_par)

    print("\n" + "━" * 55)
    print("  SEARCHING BENCHMARKS")
    print("━" * 55)

    for label, n in SIZES.items():
        data = [random.randint(1, 1_000_000) for _ in range(n)]
        target = random.choice(data)
        t_seq, t_par = benchmark_searching(label, data, target, "(in list)")
        search_results[label + " found"] = (t_seq, t_par)

    medium_data = [random.randint(1, 1_000_000) for _ in range(100_000)]
    t_seq, t_par = benchmark_searching(
        "Medium (100K)", medium_data, 0, "(not in list)"
    )
    search_results["Medium (100K) not found"] = (t_seq, t_par)

    print("\n  --- Special Cases (n=100,000) ---")

    already = list(range(1, 100_001))
    t_seq, t_par = benchmark_searching(
        "Already sorted", already, 100_000, "(last element — worst case)"
    )
    search_results["Already sorted (100K) worst"] = (t_seq, t_par)

    reverse = list(range(100_000, 0, -1))
    t_seq, t_par = benchmark_searching(
        "Reverse sorted", reverse, 1, "(last element — worst case)"
    )
    search_results["Reverse sorted (100K) worst"] = (t_seq, t_par)

    print("\n" + "=" * 65)
    print("  FINAL SUMMARY TABLE")
    print("=" * 65)
    print(f"  {'Dataset':<35s} {'Seq (s)':>10} {'Par (s)':>10} {'Faster':>10}")
    print(f"  {'-'*35} {'-'*10} {'-'*10} {'-'*10}")

    print("  [SORTING]")
    for label, (ts, tp) in sort_results.items():
        faster = "parallel" if ts > tp else "sequential"
        print(f"    {label:<33s} {ts:>10.4f} {tp:>10.4f} {faster:>10}")

    print("  [SEARCHING]")
    for label, (ts, tp) in search_results.items():
        faster = "parallel" if ts > tp else "sequential"
        print(f"    {label:<33s} {ts:>10.6f} {tp:>10.6f} {faster:>10}")

    print("=" * 65)
    print("  Benchmark complete.")