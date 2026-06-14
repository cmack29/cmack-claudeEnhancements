items = []

print("List Builder — type items to add, or 'done' to finish.\n")

while True:
    entry = input("Add item: ").strip()
    if entry.lower() == "done":
        break
    elif entry:
        entry = entry[0].upper() + entry[1:]
        items.append(entry)
        print(f"  ✓ '{entry}' added")
    else:
        print("  (empty input skipped)")

print("\nYour list:")
for item in items:
    print(f"  - {item}")