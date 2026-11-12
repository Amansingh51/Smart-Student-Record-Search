# Smart Student Record Search
# DAA Mini Project

import json
import os
from difflib import get_close_matches

FILE = "students.json"


# Save and Load Functions
def load():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []


def save(students):
    with open(FILE, "w") as f:
        json.dump(students, f, indent=4)


# Display Student Records
def show(results):
    if not results:
        print("No record found.")
        return

    print("\nRoll   Name                 Course   Sem   CGPA")
    print("-" * 55)

    for s in results:
        print(
            f"{s['roll']:<6} "
            f"{s['name']:<20} "
            f"{s['course']:<8} "
            f"{s['sem']:<5} "
            f"{s['cgpa']}"
        )

    print(f"\nTotal: {len(results)} record(s)")


# Add Student
def add(students):
    roll = input("Roll no: ").strip()

    if roll == "":
        print("Roll no cannot be empty!")
        return

    for s in students:
        if s["roll"] == roll:
            print("This roll no already exists!")
            return

    name = input("Name: ").strip().title()
    course = input("Course: ").strip().upper()
    sem = input("Semester: ").strip()

    try:
        cgpa = float(input("CGPA (0-10): "))
    except ValueError:
        print("Invalid CGPA! Record not added.")
        return

    students.append({
        "roll": roll,
        "name": name,
        "course": course,
        "sem": sem,
        "cgpa": cgpa
    })

    save(students)
    print("Student added!")


# Smart Search
def search(students):
    query = input(
        "Search (name / roll / course / sem): "
    ).strip().lower()

    if query == "":
        print("Type something to search.")
        return

    found = []

    # Linear Search
    for s in students:
        text = (
            f"{s['roll']} {s['name']} "
            f"{s['course']} {s['sem']}"
        ).lower()

        if query in text:
            found.append(s)

    # Fuzzy Search
    if not found:
        names = [s["name"].lower() for s in students]

        close = get_close_matches(
            query, names, n=3, cutoff=0.5
        )

        found = [
            s for s in students
            if s["name"].lower() in close
        ]

        if found:
            print(
                "No exact match. Showing similar names..."
            )

    show(found)


# Filter Students by CGPA
def filter_by_cgpa(students):
    try:
        limit = float(
            input("Show students with CGPA above: ")
        )
    except ValueError:
        print("Enter a valid number!")
        return

    result = [
        s for s in students
        if s["cgpa"] > limit
    ]

    result.sort(
        key=lambda s: s["cgpa"],
        reverse=True
    )

    show(result)


# Delete Student
def delete(students):
    roll = input("Enter roll no to delete: ").strip()

    for s in students:
        if s["roll"] == roll:

            confirm = input(
                f"Delete {s['name']}? (y/n): "
            ).lower()

            if confirm == "y":
                students.remove(s)
                save(students)
                print("Deleted!")

            return

    print("Student not found.")


# Main Program
def main():
    students = load()

    while True:
        print("\n===== SMART STUDENT RECORD SEARCH =====")
        print("1. Add Student")
        print("2. View All")
        print("3. Smart Search")
        print("4. Filter by CGPA")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            add(students)

        elif choice == "2":
            show(students)

        elif choice == "3":
            search(students)

        elif choice == "4":
            filter_by_cgpa(students)

        elif choice == "5":
            delete(students)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Wrong choice!")


if __name__ == "__main__":
    main()