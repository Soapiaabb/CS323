def add(a, b):
    return a + b

def subtraction(a, b):
    return a - b

def multiplication (a, b):
    return a * b

def division(dividend, divisor):
    if divisor == 0:
        return "Error: Cannot divide by zero"
    return dividend / divisor


def show_menu():
    print("\n=== Calculator Menu ===")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")


def get_numbers():
    try:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        return a, b
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return None, None


if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ")

        if choice == "5":
            print("Exiting calculator. Goodbye!")
            break

        if choice not in {"1", "2", "3", "4"}:
            print("Invalid choice. Please select a valid option.")
            continue

        a, b = get_numbers()
        if a is None:
            continue

        if choice == "1":
            print("Result:", add(a, b))
        elif choice == "2":
            print("Result:", subtraction(a, b))
        elif choice == "3":
            print("Result:", multiplication(a, b))
        elif choice == "4":
            print("Result:", division(a, b))
