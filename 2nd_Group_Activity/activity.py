import threading
import random

# Simulated shared resources
customer_db = {}
db_lock = threading.Lock()
cooking_lock = threading.Lock()

def generate_requests(n=20):
    types = ["time", "payment", "food", "support"]
    return [(i, random.choice(types)) for i in range(n)]
