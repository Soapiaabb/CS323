from concurrent.futures import ProcessPoolExecutor
import multiprocessing

employees = [
    ("Alice",   25000),
    ("Bob",     32000),
    ("Charlie", 28000),
    ("Diana",   40000),
    ("Edward",  35000),
]


SSS_RATE        = 0.045   
PHILHEALTH_RATE = 0.025   
PAGIBIG_RATE    = 0.02   
TAX_RATE        = 0.10    


def compute_payroll(employee):
    """
    Computes the complete payroll breakdown for a single employee.

    This function is designed to be called in parallel by
    ProcessPoolExecutor. Each process runs this function on a
    different employee — that is Data Parallelism.

    Parameters:
        employee (tuple): A tuple of (name, gross_salary)

    Returns:
        dict: Payroll breakdown including all deductions and net salary
    """
    name, gross_salary = employee
    process_name = multiprocessing.current_process().name


    sss        = gross_salary * SSS_RATE
    philhealth = gross_salary * PHILHEALTH_RATE
    pagibig    = gross_salary * PAGIBIG_RATE
    tax        = gross_salary * TAX_RATE


    total_deduction = sss + philhealth + pagibig + tax
    net_salary      = gross_salary - total_deduction

    return {
        "name":            name,
        "gross_salary":    gross_salary,
        "sss":             sss,
        "philhealth":      philhealth,
        "pagibig":         pagibig,
        "tax":             tax,
        "total_deduction": total_deduction,
        "net_salary":      net_salary,
        "process":         process_name,
    }


def run_parallel_payroll(emp_list=None):
    """
    Applies compute_payroll to all employees in parallel
    using ProcessPoolExecutor (Data Parallelism).

    Parameters:
        emp_list (list): Optional list of (name, salary) tuples.
                         Defaults to the module-level employees list.

    Returns:
        list[dict]: Payroll results for each employee
    """
    if emp_list is None:
        emp_list = employees

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(compute_payroll, emp_list))

    return results

def display_results(results):
    print(f"\n{'Employee':<12} {'Gross Salary':>14} {'SSS':>10} {'PhilHealth':>12} "
          f"{'Pag-IBIG':>10} {'W/Tax':>10} {'Total Deduction':>16} {'Net Salary':>12}")
    print("-" * 100)

    for r in results:
        print(
            f"{r['name']:<12} "
            f"₱{r['gross_salary']:>13,.2f} "
            f"₱{r['sss']:>9,.2f} "
            f"₱{r['philhealth']:>11,.2f} "
            f"₱{r['pagibig']:>9,.2f} "
            f"₱{r['tax']:>9,.2f} "
            f"₱{r['total_deduction']:>15,.2f} "
            f"₱{r['net_salary']:>11,.2f}"
        )

    print("-" * 100)

    total_gross      = sum(r["gross_salary"]    for r in results)
    total_deductions = sum(r["total_deduction"] for r in results)
    total_net        = sum(r["net_salary"]       for r in results)

    print(
        f"{'TOTAL':<12} "
        f"₱{total_gross:>13,.2f} "
        f"{'':>10} {'':>12} {'':>10} {'':>10} "
        f"₱{total_deductions:>15,.2f} "
        f"₱{total_net:>11,.2f}"
    )
    print("=" * 100)

    print("\n[Process Assignment (optional trace)]")
    for r in results:
        print(f"  {r['name']:<10} → handled by: {r['process']}")

    print("\n[Done] All payroll computations completed in parallel.\n")

# Main Entry Point

def main():
    print("=" * 60)
    print("  PART B: DATA PARALLELISM — ProcessPoolExecutor")
    print("=" * 60)
    print(f"  Employees to process : {len(employees)}")
    print(f"  CPU cores available  : {multiprocessing.cpu_count()}")
    print("=" * 60)

    results = run_parallel_payroll()
    display_results(results)

if __name__ == "__main__":
    main()