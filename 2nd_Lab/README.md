# Lab 2 Report: Exploring Multithreading and Multiprocessing

## 3. Performance Analysis & Execution

### Execution Results Table

| Method | Execution Order | GWA Output | Execution Time (seconds) |
| :--- | :--- | :--- | :--- |
| **Multithreading** | *Non-deterministic* | *89.33* | *0.5022 seconds* |
| **Multiprocessing** | *Non-deterministic* | *89.33* | *0.5713 seconds* |

### Discussion of Execution Order
The outputs appear in different, often non-sequential orders for both threads and processes because of **non-deterministic scheduling**.
* **Multithreading:** The operating system and Python's Global Interpreter Lock (GIL) manage thread switching. The exact moment a thread pauses and another begins is unpredictable, leading to varied output orders.
* **Multiprocessing:** Each process runs independently in its own memory space. The Operating System schedules these processes on available CPU cores. Depending on system load and core availability, some processes may finish and print faster than others, regardless of the start order.

### Code Optimization & Creativity
To optimize for faster execution and better readability:
* **`concurrent.futures` Module:** Instead of manually managing lists of threads/processes and calling `.join()`, we can use `ThreadPoolExecutor` and `ProcessPoolExecutor`. This handles context management automatically and creates a cleaner pool of workers.
* **Input Validation:** We improved the algorithm by adding `try-except` blocks to handle non-numeric inputs gracefully, ensuring the system doesn't crash during parallel execution.
* **Map Function:** Using the `map()` method within the executors allows for cleaner iteration over the grades list compared to standard `for` loops.

---

## 4. Discussion Questions

### 1. Which approach demonstrates true parallelism in Python? Explain. 
**Multiprocessing** demonstrates true parallelism. In Python, the `multiprocessing` module creates separate memory spaces and instances of the Python interpreter for each process. This allows each process to run on a different CPU core simultaneously, effectively bypassing the Global Interpreter Lock (GIL).

### 2. Compare execution times between multithreading and multiprocessing. 
* **Small Data (Current Lab):** For small inputs (like the 4 grades in the example), **Multithreading** is often faster. This is because creating new processes (`multiprocessing`) has significant system overhead (memory allocation, starting new interpreters), which can take longer than the actual calculation itself.
* **Heavy Computation:** If the GWA calculation were more complex or the dataset much larger, **Multiprocessing** would eventually outperform threading because it utilizes multiple CPU cores.

### 3. Can Python handle true parallelism using threads? Why or why not? 
**No**, standard Python (CPython) cannot handle true parallelism using threads for CPU-bound tasks. This is due to the **Global Interpreter Lock (GIL)**, a mutex that prevents multiple native threads from executing Python bytecodes at once. Even on a multi-core processor, the GIL forces threads to run one at a time (concurrently, but not in parallel).

### 4. What happens if you input a large number of grades (e.g., 1000)? Which method is faster and why? 
If processing a large number of grades (e.g., 1000) where the calculation is intensive:
* **Faster Method:** **Multiprocessing**.
* **Why:** With 1000 tasks, the benefit of running calculations simultaneously on multiple CPU cores outweighs the initial overhead of creating the processes. Multithreading would be slower because the GIL would force the 1000 calculations to queue up and run essentially in serial (one after another), plus the overhead of context switching.

### 5. Which method is better for CPU-bound tasks and which for I/O-bound tasks? 
* **CPU-bound tasks (Math, Image Processing):** **Multiprocessing** is better because it avoids the GIL and utilizes multi-core CPUs to perform heavy calculations simultaneously.
* **I/O-bound tasks (Network Requests, File Reading/Writing, User Input):** **Multithreading** is better. While one thread waits for I/O (like waiting for a user to type a grade), the GIL is released, allowing other threads to continue working.

### 6. How did your group apply creative coding or algorithmic solutions in this lab? 
* **Dynamic Input:** We replaced the hardcoded lists with a loop that accepts dynamic user input for grades, allowing the user to specify exactly how many subjects to calculate.

