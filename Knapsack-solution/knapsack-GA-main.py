from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import sys

import random
# import tools
import numpy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import Knapsack

import sys, getopt

# Genetic Algorithm constants:
POPULATION_SIZE = 100
P_CROSSOVER = 0.9  # probability for crossover
P_MUTATION = 0.3   # probability for mutating an individual
MAX_GENERATIONS = 1000000000000
HALL_OF_FAME_SIZE = 1

# set the random seed:
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
    
def varAnd(population, toolbox, cxpb, mutpb):
    offspring = [toolbox.clone(ind) for ind in population]

    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1], offspring[i])
            del offspring[i - 1].fitness.values, offspring[i].fitness.values


    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

    return offspring

#Evolution algorithm
def eaSimple(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}

    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    # elapsed is calculated as seconds
    gen, elapsed = 1, 0
    start = time.time()
    curr_max = -999
    cnt = 0

    #set the timer for 3 minutes = 180 seconds
    #if the previous max is larger or equal than current max 300 times -> break the algorithm
    #which means the max is almost optimal or already optimal
    while gen <= ngen and elapsed < 180 and cnt < 300:
        
        gen += 1

        if curr_max >= record["max"]:
            cnt += 1
        else:
            curr_max = record["max"]
            cnt = 0
        # print(cnt)

        #Time 
        elapsed = time.time() - start 
        
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

    return population, logbook, elapsed, gen 


# Genetic Algorithm flow:
def main():
        
    #Input
    check_point = 0
    # print("Test = ", end = '')
    # FILE_NUM = int(input())

    for i in range(check_point, 1):
        print("Test =", i)
        FILE_NUM = i
        # create the knapsack problem instance to be used:
        knapsack = Knapsack.Knapsack01Problem(FILE_NUM)

        toolbox = base.Toolbox()

        # create an operator that randomly returns 0 or 1:
        toolbox.register("zeroOrOne", random.randint, 0, 1)

        # define a single objective, maximizing fitness strategy:
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))

        # create the Individual class based on list:
        creator.create("Individual", list, fitness=creator.FitnessMax)

        # create the individual operator to fill up an Individual instance:
        toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, len(knapsack))

        # create the population operator to generate a list of individuals:
        toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

        # fitness calculation
        def knapsackValue(individual):
            return knapsack.getValue(individual),  # return a tuple

        toolbox.register("evaluate", knapsackValue)

        # genetic operators:mutFlipBit

        # Tournament selection with tournament size of 3:
        toolbox.register("select", tools.selTournament, tournsize=3)

        # Single-point crossover:
        toolbox.register("mate", tools.cxTwoPoint)

        
        # Flip-bit mutation:
        # indpb: Independent probability for each attribute to be flipped
        toolbox.register("mutate", tools.mutFlipBit, indpb=1.0/len(knapsack))


        # create initial population (generation 0):
        population = toolbox.populationCreator(n=POPULATION_SIZE)

        # prepare the statistics object:
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("max", numpy.max)
        stats.register("avg", numpy.mean)


        # define the hall-of-fame object:
        hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

        # perform the Genetic Algorithm flow with hof feature added:
        population, logbook, minutes, gen = eaSimple(population, 
                                                    toolbox, 
                                                    cxpb=P_CROSSOVER, 
                                                    mutpb=P_MUTATION,
                                                    ngen=MAX_GENERATIONS, 
                                                    stats=stats, 
                                                    halloffame=hof, 
                                                    verbose=True)




        # print best solution found:
        best = hof.items[0]
        print(end = '\n')
        totalWeight, totalValue, maxCapacity, weights, values = knapsack.printItems(best)


        real_sum = 0
        for i in range(len(best)):
            if best[i] == 1:
                print(best[i], values[i])
                real_sum += weights[i]  
            else:
                print(best[i])
        print('Real sum =', real_sum)


        with open("output/Genetic-Algorithm/test " + str(FILE_NUM) + ".txt", 'w+') as solver_file:
            solver_file.write('File name: {}\n'.format(knapsack.file_name))
            solver_file.write('Generation: {} \n'.format(gen))
            solver_file.write('Executed time = {} sec \n'.format(minutes))
            solver_file.write('Best genes = {} \n'.format(best))
            solver_file.write('Best solution = {} \n'.format(best.fitness.values[0]))
            solver_file.write('Max capacity = {}\n'.format(maxCapacity))
            solver_file.write('Total weight = {} \n'.format(totalWeight))
            solver_file.write('Total value = {} \n'.format(totalValue))

        print('File name: {}\n'.format(knapsack.file_name))
        print("-- Executed time = " + str(minutes) + " sec", end = '\n')
        # print("-- Best Ever Individual = ", best)
        # print("-- Best Ever Fitness = ", best.fitness.values[0])

        # print("-- Knapsack Items = ")


        # extract statistics:
        maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")

        # plot statistics:x
        # sns.set_style("whitegrid")
        # plt.plot(maxFitnessValues, color='red')
        # plt.plot(meanFitnessValues, color='green')
        # plt.xlabel('Generation')
        # plt.ylabel('Max / Average Fitness')
        # plt.title('Max and Average fitness over Generations')
        # plt.show()

if __name__ == "__main__":
    # main(sys.argv[1:])
    main()