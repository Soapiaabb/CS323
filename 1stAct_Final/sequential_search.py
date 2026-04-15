import random
import time

def linear_search(data, target):
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1


def run_benchmark(label, data, target, expected_label=""):
    print(f"\n  [{label}]  {len(data):>9,} elements | target={target} {expected_label}")
    start = time.time()
    index = linear_search(data, target)
    end = time.time()
    elapsed = end - start

    if index != -1:
        print(f"    Found  : index {index}  (data[{index}] = {data[index]})")
    else:
        print(f"    Found  : NOT FOUND")
    print(f"    Time   : {elapsed:.6f} seconds")
    return elapsed


if __name__ == "__main__":
    print("=" * 55)
    print("  Sequential Searching — Linear Search")
    print("=" * 55)

    results = {}

    print("\n--- Random Datasets ---")

    small_data = [random.randint(1, 1_000_000) for _ in range(1_000)]
    target_small = random.choice(small_data)
    results["small (found)"] = run_benchmark(
        "SMALL ", small_data, target_small, "(guaranteed found)"
    )

    medium_data = [random.randint(1, 1_000_000) for _ in range(100_000)]
    target_medium = random.choice(medium_data)
    results["medium (found)"] = run_benchmark(
        "MEDIUM", medium_data, target_medium, "(guaranteed found)"
    )

    large_data = [random.randint(1, 1_000_000) for _ in range(1_000_000)]
    target_large = random.choice(large_data)
    results["large (found)"] = run_benchmark(
        "LARGE ", large_data, target_large, "(guaranteed found)"
    )

    print("\n--- Not-Found Case (n = 100,000) ---")
    results["medium (not found)"] = run_benchmark(
        "NOT FOUND", medium_data, 0, "(target=0, out of range 1–1,000,000)"
    )

    print("\n--- Special Cases (n = 100,000) ---")

    already_sorted = list(range(1, 100_001))
    # Worst case: target at the very end
    results["already sorted (worst case)"] = run_benchmark(
        "ALREADY SORTED", already_sorted, 100_000, "(last element)"
    )

    reverse_sorted = list(range(100_000, 0, -1))
    results["reverse sorted (worst case)"] = run_benchmark(
        "REVERSE SORTED", reverse_sorted, 1, "(last element)"
    )

    # --- Summary ---
    print("\n" + "=" * 55)
    print("  Summary — Sequential Linear Search")
    print("=" * 55)
    for label, t in results.items():
        print(f"  {label:<40s} : {t:.6f}s")