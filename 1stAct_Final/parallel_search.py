import random
import time
from multiprocessing import Process, Queue

def merge_sort(arr):
    """Standard merge sort used within each parallel chunk."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    return merge(left_half, right_half)


def merge(left, right):
    result = []
    i = 0
    j = 0
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

def sort_worker(chunk, chunk_id, result_queue):
    sorted_chunk = merge_sort(chunk)
    result_queue.put((chunk_id, sorted_chunk))

def k_way_merge(sorted_chunks):
    while len(sorted_chunks) > 1:
        next_level = []
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                merged = merge(sorted_chunks[i], sorted_chunks[i + 1])
            else:
                # Odd one out — carry it forward without merging
                merged = sorted_chunks[i]
            next_level.append(merged)
        sorted_chunks = next_level
    return sorted_chunks[0]


def parallel_sort(data, num_processes=4):
    n = len(data)
    chunk_size = n // num_processes
    result_queue = Queue()
    processes = []


    for i in range(num_processes):
        start = i * chunk_size

        end = start + chunk_size if i < num_processes - 1 else n
        chunk = data[start:end]

        p = Process(target=sort_worker, args=(chunk, i, result_queue))
        processes.append(p)
        p.start()

    raw_results = []
    for _ in range(num_processes):
        raw_results.append(result_queue.get())

    for p in processes:
        p.join()

    raw_results.sort(key=lambda x: x[0])
    sorted_chunks = [chunk for _, chunk in raw_results]

    final_sorted = k_way_merge(sorted_chunks)
    return final_sorted


def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def run_benchmark(label, data):
    print(f"\n  [{label}]  {len(data):>9,} elements")
    start = time.time()
    sorted_data = parallel_sort(data)
    end = time.time()
    elapsed = end - start
    valid = is_sorted(sorted_data)
    print(f"    Time   : {elapsed:.4f} seconds")
    print(f"    Valid  : {valid}")
    print(f"    Sample : {sorted_data[:5]} ... {sorted_data[-5:]}")
    return elapsed


if __name__ == "__main__":
    print("  Parallel Sorting — 4-Process Merge Sort")
    results = {}
    print("Random Datasets")

    small_data = [random.randint(1, 1_000_000) for _ in range(1_000)]
    results["small (random)"] = run_benchmark("SMALL ", small_data)

    medium_data = [random.randint(1, 1_000_000) for _ in range(100_000)]
    results["medium (random)"] = run_benchmark("MEDIUM", medium_data)

    large_data = [random.randint(1, 1_000_000) for _ in range(1_000_000)]
    results["large (random)"] = run_benchmark("LARGE ", large_data)


    print("Special Cases (n = 100,000)")

    already_sorted = list(range(1, 100_001))
    results["medium (already sorted)"] = run_benchmark(
        "ALREADY SORTED", already_sorted
    )

    reverse_sorted = list(range(100_000, 0, -1))
    results["medium (reverse sorted)"] = run_benchmark(
        "REVERSE SORTED", reverse_sorted
    )

    print("  Summary — Parallel Merge Sort")
    for label, t in results.items():
        print(f"  {label:<30s} : {t:.4f}s")