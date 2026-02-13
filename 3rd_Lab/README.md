Provide concise but well-structured explanations.

1. Differentiate Task and Data Parallelism. Identify which part of the lab demonstrates each and justify the workload division.

    - In our project, data_parallelism.py demonstrates Data Parallelism by having different processes perform the same payroll calculation on a list of several employees at once. In contrast, task_parallelism.py shows Task Parallelism by taking a single employee and splitting their specific deductions like SSS and Tax into different jobs handled by separate threads.

2. Explain how concurrent.futures managed execution, including submit(), map(), and Future objects. Discuss the purpose of with when creating an Executor.

    - We used map() in our data script to automatically deal out the employee list to functions, while submit() in our task script acted like a work order that gave us a Future object (a receipt) to claim our results later. The with statement served as our manager, ensuring that all threads and processes were cleaned up and closed properly once the work was finished.

3. Analyze ThreadPoolExecutor execution in relation to the GIL and CPU cores. Did true parallelism occur?

    - In our ThreadPoolExecutor test, true parallelism did not occur because of Python’s Global Interpreter Lock (GIL), which only allows one thread to use the CPU at a time. This means our threads were actually taking very fast turns to calculate deductions rather than working at the exact same millisecond.

4. Explain why ProcessPoolExecutor enables true parallelism, including memory space separation and GIL behavior.

    - Our ProcessPoolExecutor achieved true parallelism because each process runs in its own memory space and has its own copy of Python, allowing them to bypass the GIL. This let our computer use multiple CPU cores to perform different payroll calculations at the exact same moment.

5. Evaluate scalability if the system increases from 5 to 10,000 employees. Which approach scales better and why?

    - If we scaled to 10,000 employees, Data Parallelism would be much more efficient because it spreads the heavy workload across all available CPU cores. Using threads for 10,000 people would be slower because the system would spend too much time managing the "paperwork" of the threads instead of doing the actual math.


6. Provide a real-world payroll system example. Indicate where Task Parallelism and Data Parallelism would be applied, and which executor you would use.

    - In a real-world system with thousands of workers, we would use Data Parallelism to process large groups of employees across different CPU cores simultaneously to save time. We could then use Task Parallelism within those groups if we needed to pull data from different sources, like a tax database and a bank API, at the same time.