"""
tas_sections.py
"""
import random as rnd
import pandas as pd
import numpy as np
import evo
import os
import csv

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__),'.')) # Project Root

# reading in tas and sections data
arr_tas = np.loadtxt(os.path.join(ROOT_DIR, 'data', 'tas.csv'),delimiter=",", dtype = 'object')
arr_sections = np.loadtxt(os.path.join(ROOT_DIR, 'data', 'sections.csv'), delimiter=",", dtype = 'object')

def overallocation(solution):
    """Calculate no. of times TAs are allocated"""
    sums_actual = np.sum(solution, axis=1)
    sums_wanted = list(map(lambda x: int(x), arr_tas[1:,2]))
    result = list(map(lambda x, y: int(x - y), sums_actual, sums_wanted))
    result = list(filter(lambda number: number > 0, result))
    penalties = np.sum(result)

    return int(penalties)

def conflicts(solution):
    """Calculate no. of time conflicts across all TA-Section assignments"""
    result = list(np.where(solution == 1))
    times = [arr_sections[i+1][2] for i in result[1]]
    zipped = list(zip(result[0], times))
    penalties = len(np.unique([x[0] for x in zipped if zipped.count(x) > 1]))

    return int(penalties)

def undersupport(solution):
    """Calculate the score for the amount by which sections are under-supported"""
    sums_actual = np.sum(solution, axis=0)
    sums_wanted = list(map(lambda x: int(x), arr_sections[1:,6]))
    result = list(map(lambda x, y: y-x, sums_actual, sums_wanted))
    result = list(filter(lambda number: number > 0, result))
    penalties = np.sum(result)

    return int(penalties)

def unwilling(solution):
    """Calculate total no. of assignments that TAs are unwilling to support"""
    result = list(np.where(solution == 1))
    zipped = list(zip(result[0], result[1]))
    ta_preference = list(zip(result[0], [arr_tas[i+1][k+3] for i, k in zipped]))
    penalties = len([item[0] for item in ta_preference if item[1] == 'U'])

    return int(penalties)

def unpreferred(solution):
    """Calculate total no. of assignments that TAs don't prefer to support"""
    result = list(np.where(solution == 1))
    zipped = list(zip(result[0], result[1]))
    ta_preference = list(zip(result[0], [arr_tas[i+1][k+3] for i, k in zipped]))
    penalties = len([item[0] for item in ta_preference if item[1] == 'W'])

    return int(penalties)

def swapper(solutions):
    """ randomly swapping each array"""
    solution = solutions[0]
    [np.random.shuffle(c) for c in solution]
    return solution

def minimize_unwilling(solutions):
    """ """
    solution = solutions[0]
    result = list(np.where(solution == 1))
    zipped = list(zip(result[0], result[1]))
    ta_preference = list([arr_tas[i+1][k+3] for i, k in zipped])
    random_choice = rnd.randint(0, len(zipped)-1)
    if ta_preference[random_choice] == 'U':
        solution[zipped[random_choice][0]][zipped[random_choice][1]] = 0
        solution[zipped[random_choice][0]][rnd.randint(0, 16)] = 1
    return solution



def main():
    # read in the test data
    test1 = np.loadtxt("test1.csv", delimiter=",")
    test2 = np.loadtxt("test2.csv", delimiter=",")
    test3 = np.loadtxt("test3.csv", delimiter=",")

    # creating an initial solution w/ no overallocation whatsoever
    sums_wanted = list(map(lambda x: int(x), arr_tas[1:,2]))
    lst = []
    # looping through the desired numbers
    for i in sums_wanted:
        # making an array with zeros and an array with ones based on the desired number
        zeros = list(np.zeros(len(test1[0]) - i, dtype=int))
        ones = list(np.ones(i, dtype=int))
        # combining the two arrays together
        zeros.extend(ones)
        lst.append(zeros)
    initial_sol = np.array(lst)

    # list of all solutions
    solution = [initial_sol]

    # create population
    E = evo.Environment()

    # register the fitness criteria (objects)
    E.add_fitness_criteria("overallocation", overallocation)
    E.add_fitness_criteria("conflicts", conflicts)
    E.add_fitness_criteria("undersupport", undersupport)
    E.add_fitness_criteria("unwilling", unwilling)
    E.add_fitness_criteria("unpreferred", unpreferred)

    # register all agents
    E.add_agent("swapper", swapper, 1)
    E.add_agent("minimize_unwilling", minimize_unwilling, 1)

    # seed the population with an initial solution
    E.add_solution(solution[0])

    # run the evolver
    E.evolve(time_limit = 300)

    # print result
    print(E)


if __name__ == '__main__':
    main()
