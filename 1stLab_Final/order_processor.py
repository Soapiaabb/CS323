from mpi4py import MPI
import time

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
            {'id': 5, 'item': 'Headphones'}
        ]
        
        num_workers = size - 1
        for i, order in enumerate(orders):
            worker = (i % num_workers) + 1
            comm.send(order, dest=worker, tag=1)
            
        for i in range(1, size):
            comm.send(None, dest=i, tag=1)
            
    else:
        while True:
            order = comm.recv(source=0, tag=1)
            if order is None:
                break
            print(f"Worker {rank} handled Order {order['id']}")

if __name__ == '__main__':
    main()
