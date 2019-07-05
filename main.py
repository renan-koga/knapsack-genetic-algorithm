import sys
import csv
import math
import time
from random import seed
from random import randint

FILE = sys.argv[1]

population = []
generation = []
inventory = []
knapsack_length = 0
knapsack_volume = 0
n_gen = 0
max_generation = 1000

def gen_population(n=50):
    global population
    for i in range(n):
        population.append(gen_individual())

def gen_next_generation():
    global generation
    global population
    global n_gen
    generation = []
    
    population.sort(key=lambda x: x[2], reverse=True)
    print("[", n_gen, "] - MELHOR IMPORTÂNCIA: ", population[0][2], " - PESO: ", population[0][1])
    for i in range(0, len(population)-1, 2):
        p1 = population[i]
        p2 = population[i+1]
        f1, f2 = crossover(p1, p2)

        if f1[1] > knapsack_volume:
            bag_info_aux = f1[0]
            bag_volume_aux = f1[1]
            bag_importance_aux = f1[2] * -1

            f1 = (bag_info_aux, bag_volume_aux, bag_importance_aux)

        if f2[1] > knapsack_volume:
            bag_info_aux = f2[0]
            bag_volume_aux = f2[1]
            bag_importance_aux = f2[2] * -1

            f2 = (bag_info_aux, bag_volume_aux, bag_importance_aux)

        generation.append(f1)
        generation.append(f2)

    aux = population[:] + generation[:]
    aux.sort(key=lambda x: x[2], reverse=True)

    population = aux[:size]
    mutate()

def gen_individual():
    individual = fill_zeros(knapsack_length)
    limit = 0
    importance = 0

    while (limit < knapsack_volume):
        value = randint(0, knapsack_length-1)
        item = inventory[value]
        if (item[0] <= knapsack_volume - limit):
            limit += item[0]
            importance += item[1]
            individual[value] = 1
        else:
            break
    
    return (individual, limit, importance)

def mutate():
    global population

    for solution in population:
        value = randint(0, 100)
        
        if(value < 3):
            i = randint(0, knapsack_length-1)

            if (solution[0][i] == 0):
                solution[0][i] = 1
            else: solution[0][i] = 0

def get_best_importance():
    global population
    best = 0
    for solution in population:
        if solution[2] > best:
            best = solution[2]
    
    return best
    
def get_worst_importance():
    global population
    worst = 99999
    for solution in population:
        if solution[2] < worst:
            worst = solution[2]
    
    return worst

def crossover(bag1, bag2):
    bag1_items = bag1[0]
    bag2_items = bag2[0]

    ceil = math.ceil(knapsack_volume/2)
    s1 = bag1_items[:ceil] + bag2_items[ceil:]
    s2 = bag2_items[:ceil] + bag1_items[ceil:]

    return bag_info(s1), bag_info(s2)

def fitness(arr):
    pass

def bag_info(bag_items):
    limit = 0
    importance = 0
    for i in range(len(bag_items)):
        if bag_items[i] == 1:
            item = inventory[i]
            limit += item[0]
            importance += item[1]

    return (bag_items, limit, importance)

def read_csv():
    global knapsack_length
    global knapsack_volume
    with open(FILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for rows in csv_reader:
            if line_count == 1:
                knapsack_volume = int(rows[1])
            elif line_count > 1:
                aux = rows[1:]
                for i in range(len(aux)):
                    aux[i] = int(aux[i])

                inventory.append(tuple(aux))
            line_count += 1
        knapsack_length = line_count - 2

def fill_zeros(n):
    arr = []
    for i in range(n):
        arr.append(0)

    return arr

def print_population():
    for solution in population:
        print(solution)

def write_solution():
    aux = str(FILE)
    filename = aux[:len(aux)-4] + '-solution.csv'

    with open(filename, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for item in population[0][0]:
            writer.writerow([item])

    return filename

def finishing():
    print("\n\n##############################################################################################################")
    print("################################################### MELHOR ###################################################")
    print("##############################################################################################################\n\n")
    
    print("Items:", population[0][0])
    print("Volume:", population[0][1])
    print("Importance:", population[0][2])
    filename = write_solution()

    print("\n\n##############################################################################################################")
    print("##############################################################################################################")
    print("##############################################################################################################\n\n")

    print("\nSaved file:", filename)


##
# Main starts here
##

start = time.time()

read_csv()
size = knapsack_length * 3
gen_population(size)

end = time.time()

try:
    # while(n_gen < max_generation):
    while(end-start < 5 * 60):
        gen_next_generation()
        n_gen += 1
        end = time.time()
except (KeyboardInterrupt):
    finishing()
    print("\nTIME:", end-start)
    sys.exit(0)

finishing()

print("\nTIME:", end-start)