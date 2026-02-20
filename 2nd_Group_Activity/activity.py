import threading

# Simulated shared resources
customer_db = {}
db_lock = threading.Lock()
cooking_lock = threading.Lock()
