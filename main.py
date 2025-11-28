from timetableCSP import TimetableCSP
from src.algorithms import min_conflicts1

def main():

    lectures = [
        ("Practical Programming Methodology", 2),
        ("Algorithms I", 2),
        ("Operating Systems", 2),
        ("Introduction to File and Database Management", 2),
    ]

    labs = [
        ("Practical Programming Methodology Lab", 2),
        ("Algorithms I Lab", 1),
        ("Operating Systems Lab", 1),
        ("Introduction to File and Database Management Lab", 1),
    ]

    csp = TimetableCSP(lectures, labs, classes_per_day=3)

    solution = min_conflicts1(csp, max_steps=10000)
    if solution:
        print("Solution found:")
        csp.display_table(solution)
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()