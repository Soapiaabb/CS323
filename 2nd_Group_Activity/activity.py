import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor

# Simulated shared resources
customer_db = {}
db_lock = threading.Lock()
cooking_lock = threading.Lock()

def generate_requests(n=20):
    types = ["time", "payment", "food", "support"]
    return [(i, random.choice(types)) for i in range(n)]

def process_request(request):
    customer_id, req_type = request

    if req_type in ["time", "payment"]:
        time.sleep(0.1)
        with db_lock:
            customer_db[customer_id] = "updated"

    elif req_type == "food":
        with cooking_lock:
            time.sleep(0.3)

    elif req_type == "support":
        time.sleep(0.2)

# Sequential nga part
def run_sequential(requests):
    start = time.time()
    for req in requests:
        process_request(req)
    return time.time() - start

# Parallel version
def run_parallel(requests, workers=3):
    start = time.time()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(process_request, requests)
    return time.time() - start

if __name__ == "__main__":
    requests = generate_requests(30)

    seq_time = run_sequential(requests)
    par_time = run_parallel(requests)

    speedup = seq_time / par_time 

    print(f"Sequential Time: {seq_time:.4f} seconds")
    print(f"Parallel Time:   {par_time:.4f} seconds")
    print(f"Speedup:         {speedup:.2f}x")
