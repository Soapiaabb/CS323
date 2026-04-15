import random
import time

def merge_sort(arr):
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

def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

def run_benchmark(label, data):
    print(f"\n  [{label}]  {len(data):>9,} elements")
    start = time.time()
    sorted_data = merge_sort(data)
    end = time.time()
    elapsed = end - start
    valid = is_sorted(sorted_data)
    print(f"    Time   : {elapsed:.4f} seconds")
    print(f"    Valid  : {valid}")
    print(f"    Sample : {sorted_data[:5]} ... {sorted_data[-5:]}")
    return elapsed

if __name__ == "__main__":
    print("\n Sequential Sorting")


    results = {}

    print("\n Random Datasets ")

    small_data = [random.randint(1, 1_000_000) for _ in range(1_000)]
    results["small (random)"] = run_benchmark("Small", small_data)

    medium_data = [random.randint(1, 1_000_000) for _ in range(100_000)]
    results["medium (random)"] = run_benchmark("Medium", medium_data)

    large_data = [random.randint(1, 1_000_000) for _ in range(1_000_000)]
    results["large (random)"] = run_benchmark("Large", large_data)

    print("\n Special Cases (n = 100,000) ")

    already_sorted = list(range(1, 100_001))
    results["medium (already sorted)"] = run_benchmark(
        "Already Sorted", already_sorted
    )

    reverse_sorted = list(range(100_000, 0, -1))
    results["medium (reverse sorted)"] = run_benchmark(
        "Reverse Sorted", reverse_sorted
    )

    print("\n Summary \n")
    for label, t in results.items():
        print(f"  {label:<30s} : {t:.4f}s")