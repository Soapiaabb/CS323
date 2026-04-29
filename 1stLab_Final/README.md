# First Laboratory - Distributed Order Processing System

We built a distributed order processing system using MPI and Python's multiprocessing tools for our final CS323 lab. This was definitely a fun challenge. I think getting the processes to talk to each other correctly took some trial and error, but we got it working smoothly.

## Reflection Questions

**1. How did you distribute orders among worker processes?**
We used a round-robin approach. The master process (rank 0) loops through the orders and uses `comm.send` to fire them off to the workers one by one. The workers just sit in a loop using `comm.recv` to wait for their next task. It keeps things pretty balanced.

**2. What happens if there are more orders than workers?**
The workers just end up taking on multiple tasks. Since we distribute them in a circle, if we have 3 workers and 7 orders, worker 1 gets order 1, 4, and 7. The extra orders just wait in the MPI message queue until the worker is done with its current delay and ready to receive the next one. 

**3. How did processing delays affect the order completion?**
It completely jumbled the completion order, which makes sense. Because we added a random `time.sleep()`, a worker that gets an order later might finish before a worker that got an earlier one. Maybe this is why real-world distributed systems need strict IDs to track things. You definitely can't rely on the order they finish in.

**4. How did you implement shared memory, and where was it initialized?**
We initialized `Manager().list()` and `Lock()` right at the top of our script, just like the snippets suggested. Though, I think it's worth noting that `mpirun` spawns entirely isolated processes. A standard multiprocessing manager doesn't natively cross MPI bounds without a dedicated sync server. To actually make the master print the final list, we added a quick `comm.gather()` at the very end to pull the local lists together. 

**5. What issues occurred when multiple workers wrote to shared memory simultaneously?**
Before adding the lock, things got a bit messy. If two workers finish their `sleep()` at the exact same time and try to `append()` to the list, one of the updates can get lost. It's a classic race condition. The list just isn't thread-safe or process-safe on its own.

**6. How did you ensure consistent results when using multiple processes?**
We wrapped the append operation in a `with lock:` block. This acts like a bouncer. Only one process can hold the lock at a time, so it guarantees that workers line up to write their results sequentially. No more data loss!

## Execution Demonstration
![Execution GIF](execution.gif)
