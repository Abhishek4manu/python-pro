# employee_manager.py
import json
import os
from typing import List, Dict, Optional

DATA_FILE = "employees.json"

def load_data(filename: str = DATA_FILE) -> List[Dict]:
    """Load employee list from JSON file. Return empty list if file missing or invalid."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError):
        return []

def save_data(employees: List[Dict], filename: str = DATA_FILE) -> None:
    """Save employees list to JSON file (pretty printed)."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(employees, f, indent=2, ensure_ascii=False)

def validate_name(name: str) -> bool:
    name = name.strip()
    return len(name) >= 1

def validate_age(age_str: str) -> Optional[int]:
    """Return int age if valid (18-100), else None."""
    try:
        age = int(age_str)
        if 15 <= age <= 100:
            return age
    except ValueError:
        pass
    return None

def add_employee(employees: List[Dict]) -> None:
    name = input("Enter name: ").strip()
    if not validate_name(name):
        print("Invalid name. Try again.")
        return
    age_str = input("Enter age (15-100): ").strip()
    age = validate_age(age_str)
    if age is None:
        print("Invalid age. Must be number between 15 and 100.")
        return
    dept = input("Enter department: ").strip()
    if not dept:
        dept = "General"
    # create an id: next integer
    next_id = 1 + max((e.get("id", 0) for e in employees), default=0)
    emp = {"id": next_id, "name": name, "age": age, "department": dept}
    employees.append(emp)
    save_data(employees)
    print(f"Added employee {name} (id={next_id}).")

def view_all(employees: List[Dict]) -> None:
    if not employees:
        print("No employees.")
        return
    print("-" * 50)
    print(f"{'ID':<4} {'Name':<20} {'Age':<4} {'Department':<15}")
    print("-" * 50)
    for e in employees:
        print(f"{e.get('id', ''):<4} {e.get('name',''):<20} {e.get('age',''):<4} {e.get('department',''):<15}")
    print("-" * 50)

def find_by_name(employees: List[Dict], name_query: str) -> List[Dict]:
    name_query = name_query.strip().lower()
    return [e for e in employees if name_query in e.get("name", "").lower()]

def delete_by_id(employees: List[Dict], id_to_delete: int) -> bool:
    for i, e in enumerate(employees):
        if e.get("id") == id_to_delete:
            del employees[i]
            save_data(employees)
            return True
    return False

def prompt_search(employees: List[Dict]) -> None:
    q = input("Enter name to search (partial allowed): ").strip()
    results = find_by_name(employees, q)
    if not results:
        print("No matches.")
        return
    print(f"Found {len(results)}:")
    for e in results:
        print(f"  id={e['id']} name={e['name']} age={e['age']} dept={e['department']}")

def prompt_delete(employees: List[Dict]) -> None:
    sid = input("Enter id to delete: ").strip()
    try:
        sid_int = int(sid)
    except ValueError:
        print("Invalid id.")
        return
    ok = delete_by_id(employees, sid_int)
    if ok:
        print(f"Deleted employee id={sid_int}.")
    else:
        print("No employee with that id.")

def main():
    employees = load_data()
    while True:
        print("\nEmployee Manager — Choose an option:")
        print("1. Add employee")
        print("2. View all")
        print("3. Search by name")
        print("4. Delete by id")
        print("5. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            add_employee(employees)
        elif choice == "2":
            view_all(employees)
        elif choice == "3":
            prompt_search(employees)
        elif choice == "4":
            prompt_delete(employees)
        elif choice == "5":
            print("Exiting. Goodbye.")
            break
        else:
            print("Invalid choice. Enter 1-5.")

if __name__ == "__main__":
    main()
