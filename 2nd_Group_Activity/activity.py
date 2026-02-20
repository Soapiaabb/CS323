import threading
import random
import time

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
