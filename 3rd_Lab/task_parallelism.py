from concurrent.futures import ThreadPoolExecutor
import threading

def compute_sss(salary):
    thread = threading.current_thread().name
    amount = salary * 0.045
    print(f"[{thread}] SSS computed")
    return amount


def compute_philhealth(salary):
    thread = threading.current_thread().name
    amount = salary * 0.025
    print(f"[{thread}] PhilHealth computed")
    return amount


def compute_pagibig(salary):
    thread = threading.current_thread().name
    amount = salary * 0.02
    print(f"[{thread}] Pag-IBIG computed")
    return amount


def compute_tax(salary):
    thread = threading.current_thread().name
    amount = salary * 0.10
    print(f"[{thread}] Withholding Tax computed")
    return amount
