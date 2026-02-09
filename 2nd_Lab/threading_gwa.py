import threading
import time

# Move the functions here instead of importing them
def calculate_grade(name, score):
    print(f"  > Processing {name}...")
    time.sleep(0.5)
    return score

def display_header(mode):
    print(f"\n{'='*10} {mode.upper()} GWA SYSTEM {'='*10}")

results = []
lock = threading.Lock()

def thread_task(name, score):
    res = calculate_grade(name, score)
    with lock:
        results.append(res)

def main():
    display_header("Multithreading")
    # Take user input creatively
    num_subjects = int(input("Enter number of subjects: "))
    data = {}
    for _ in range(num_subjects):
        name = input("Subject Name: ")
        grade = float(input(f"Grade for {name}: "))
        data[name] = grade
    
    threads = []
    start_time = time.perf_counter()

    for sub, grade in data.items():
        t = threading.Thread(target=thread_task, args=(sub, grade))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    gwa = sum(results) / len(results) if results else 0
    end_time = time.perf_counter()
    
    print(f"\nFinal GWA: {gwa:.2f}")
    print(f"Total Time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()