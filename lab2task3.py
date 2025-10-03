
from src.locations import *

from src.CompanyEnvironmentClass import CompanyEnvironment

ce = CompanyEnvironment()

from src.Task3YourClasses import Student, ITStaff, OfficeManager

itStaff = ITStaff()
student = Student()
manager = OfficeManager()

ce.add_thing(itStaff)
print("IT is located at {}.".format(itStaff.location))

ce.add_thing(student)
print("Student is located at {}.".format(student.location))

ce.add_thing(manager)
print("Manager is located at {}.".format(manager.location))

from src.agents import ReflexAgentA2pro

raTask3pro1 = ReflexAgentA2pro()

ce.add_thing(raTask3pro1)

print("State of the office enviroment: {}.".format(ce.locations))
print("Agent is located at {}.".format(raTask3pro1.location))

ce.run()