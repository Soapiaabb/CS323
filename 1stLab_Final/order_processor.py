from mpi4py import MPI
from multiprocessing import Manager, Lock
import time
import random

manager = Manager()
shared_orders = manager.list()
lock = Lock()

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 2:
        if rank == 0:
            print("Please run with at least 2 processes (e.g., mpirun -np 4 python order_processor.py)")
        return

    if rank == 0:
        orders = [
            {'id': 1, 'item': 'Laptop'},
            {'id': 2, 'item': 'Mouse'},
            {'id': 3, 'item': 'Keyboard'},
            {'id': 4, 'item': 'Monitor'},
            {'id': 5, 'item': 'Headphones'},
            {'id': 6, 'item': 'Desk'},
            {'id': 7, 'item': 'Chair'}
        ]
        
        print(f"Master (Process {rank}) generating {len(orders)} orders...")
        
        num_workers = size - 1
        for i, order in enumerate(orders):
            worker_rank = (i % num_workers) + 1
            comm.send(order, dest=worker_rank, tag=1)
            
        for i in range(1, size):
            comm.send(None, dest=i, tag=1)
            
        comm.Barrier()
        
        # We gather lists here since Manager() is isolated per MPI process
        all_completed = comm.gather(list(shared_orders), root=0)
        final_list = []
        for lst in all_completed[1:]:
            final_list.extend(lst)
            
        print("\n--- Final Completed Orders ---")
        for order in final_list:
            print(f"Order ID: {order['id']} - Item: {order['item']}")
            
    else:
        while True:
            order = comm.recv(source=0, tag=1)
            if order is None:
                break
                
            print(f"Process {rank} received Order {order['id']}: {order['item']}")
            time.sleep(random.uniform(0.5, 1.5))
            
            with lock:
                shared_orders.append(order)
                
            print(f"Process {rank} finished Order {order['id']}")
            
        comm.Barrier()
        comm.gather(list(shared_orders), root=0)

if __name__ == '__main__':
    main()
