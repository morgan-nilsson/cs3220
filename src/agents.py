from src.agentPrograms import *
from src.agentClass import Agent

from src.rules import vacuumRules
from src.rules import actionList
from src.rules import table
from src.rules import a2proRules




'''Randomly choose one of the actions from the vacuum environment'''
def RandomVacuumAgent():
    return Agent(RandomAgentProgram(actionList))


def TableDrivenVacuumAgent():
     return Agent(TableDrivenAgentProgram(table))
 
 
def ReflexAgent() :
  return Agent(ReflexAgentProgram(vacuumRules,interpret_input,rule_match))


def ReflexAgentA2pro():
    return Agent(ReflexAgentA2proProgram(a2proRules))
  

