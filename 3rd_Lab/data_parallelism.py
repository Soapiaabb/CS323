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

