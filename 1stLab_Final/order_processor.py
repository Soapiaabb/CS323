from mpi4py import MPI
from multiprocessing import Manager
import time
import random

manager = Manager()
shared_orders = manager.list()

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 2:
        if rank == 0:
            print("Need at least 2 processes")
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
        
        num_workers = size - 1
        for i, order in enumerate(orders):
            worker = (i % num_workers) + 1
            comm.send(order, dest=worker, tag=1)
            
        for i in range(1, size):
            comm.send(None, dest=i, tag=1)
            
        comm.Barrier()
        
        # gather hack because of mpirun isolation
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
            
            # writing without a lock!
            shared_orders.append(order)
            print(f"Process {rank} finished Order {order['id']}")
            
        comm.Barrier()
        comm.gather(list(shared_orders), root=0)

if __name__ == '__main__':
    main()
