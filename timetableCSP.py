from src.CSPclass import CSP

class TimetableCSP(CSP):
    def __init__(self, lectures: list[tuple[str, int]], labs: list[tuple[str, int]], classes_per_day: int, days: None | list[str] = None):
        # build list of variables
        variables = []
        for lecture, count in lectures:
            for i in range(count):
                variables.append(lecture + " " + str(i))
        for lab, count in labs:
            for i in range(count):
                variables.append(lab + " " + str(i))
        days = days or ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        time_slots = [f"{day} slot {i+1}" for day in days for i in range(classes_per_day)]
        self.classes_per_day = classes_per_day

        # build dictionary of domains
        domains = {}
        for var in variables:
            domains[var] = time_slots.copy()

        # build dictionary of neighbors
        neighbors = {}
        for var in variables:
            # all other variables are neighbors
            neighbors[var] = [v for v in variables if v != var]

        def is_lab(class_name: str) -> bool:
            return class_name.endswith(" Lab")

        def get_day(slot: str) -> str:
            return slot.split()[0]

        def get_course_name(class_name: str) -> str:
            return class_name.rsplit(" ", 1)[0]

        def constraints(var1, val1, var2, val2):
            # There can't be 2 lectures on the same course on the same day, but there can be a lecture and a lab on the same course on the same day.
            if get_course_name(var1) == get_course_name(var2):
                if not is_lab(var1) and not is_lab(var2):
                    if get_day(val1) == get_day(val2):
                        return False
            # There can't be 2 lectures on the same course on an adjacent day, but there can be a lecture and a lab on the same course on an adjacent day.
            if get_course_name(var1) == get_course_name(var2):
                if not is_lab(var1) and not is_lab(var2):
                    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
                    day1 = get_day(val1)
                    day2 = get_day(val2)
                    if abs(days.index(day1) - days.index(day2)) == 1:
                        return False
            # There can't be 2 labs on the same course on an adjacent day.
            if get_course_name(val1) == get_course_name(val2):
                if is_lab(var1) and is_lab(var2):
                    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
                    day1 = get_day(val1)
                    day2 = get_day(val2)
                    if abs(days.index(day1) - days.index(day2)) == 1:
                        return False

            # No 2 things can be scheduled in the same time slot.
            if val1 == val2:
                return False

            return True

        super().__init__(variables, domains, neighbors, constraints)
    
    def display(self, assignment):
        for class_name in self.variables:
            # parse off the index (last part)
            name = class_name.rsplit(" ", 1)[0]
            print(f"{name}: {assignment[class_name]}")

    def display_table(self, assignment):
        classes = []
        for class_name in self.variables:
            # parse off the index (last part)
            classes.append(class_name.rsplit(" ", 1)[0])

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        time_slots = [str(i+1) for i in range(self.classes_per_day)]

        table = {}
        for day in days:
            table[day] = {}
            for time in time_slots:
                table[day][time] = "Free"


        for class_name in self.variables:
            slot = assignment[class_name]
            day = slot.split()[0]
            time = slot.split()[2]
            name = class_name.rsplit(" ", 1)[0]
            table[day][time] = name

        for day in table:
            print(f"{day}:")
            for time in table[day]:
                print(f"  {time}: {table[day][time]}")
            print()


