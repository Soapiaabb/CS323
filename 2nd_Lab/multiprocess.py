from multiprocessing import Process, Manager, Lock
import time

def compute_gwa_process(subject, grade, shared_list, order_counter, lock):
    time.sleep(0.1)  # simulate heavy computation
    shared_list.append(grade)

    with lock:
        order_counter.value += 1
        exec_order = order_counter.value

    gwa = sum(shared_list) / len(shared_list)
    print(f"[Process] Order {exec_order} | {subject} processed | Current GWA: {gwa:.2f}")

if __name__ == "__main__":
    num_subjects = int(input("Enter number of subjects: "))
    grades = []

    for i in range(num_subjects):
        grade = float(input(f"Enter grade for subject {i + 1}: "))
        grades.append(grade)

    manager = Manager()
    shared_results = manager.list()
    order_counter = manager.Value('i', 0)  # shared execution counter
    lock = Lock()

    start_time = time.time()

    processes = []
    for i, grade in enumerate(grades):
        p = Process(
            target=compute_gwa_process,
            args=(f"Subject {i + 1}", grade, shared_results, order_counter, lock)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end_time = time.time()

    final_gwa = sum(grades) / len(grades)
    print(f"\n[Process] Final GWA: {final_gwa:.2f}")
    print(f"[Process] Execution Time: {end_time - start_time:.4f} seconds")
