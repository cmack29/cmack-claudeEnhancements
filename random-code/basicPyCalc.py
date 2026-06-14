def calculate(a, op, b):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0:
            return "Error: division by zero"
        return a / b

print("Terminal Calculator — type 'quit' to exit.\n")

while True:
    entry = input("Enter calculation (e.g. 3 + 5): ").strip()
    if entry.lower() == "quit":
        break

    try:
        parts = entry.split()
        a, op, b = float(parts[0]), parts[1], float(parts[2])

        if op not in ("+", "-", "*", "/"):
            print("  Unsupported operator. Use +, -, *, /\n")
            continue

        result = calculate(a, op, b)

        # Print as int if result is a whole number
        if isinstance(result, float) and result.is_integer():
            print(f"  = {int(result)}\n")
        else:
            print(f"  = {result}\n")

    except (ValueError, IndexError):
        print("  Invalid input. Try something like: 10 / 2\n")