import csv
import math
from random import seed
from random import randint

population = []
generation = []
inventory = []
knapsack_length = 0
knapsack_volume = 0


def gen_population(n=50):
    global population
    for i in range(n):
        population.append(gen_individual())
        #rint(population[i])

def gen_next_generation():
    for i in range(0, len(population), 2):
        p1 = population[i]

def gen_individual():
    individual = fill_zeros(knapsack_length)
    limit = 0
    importance = 0

    while (limit < knapsack_volume):
        value = randint(0, knapsack_length-1)
        item =inventory[value]
        if (item[0] <= knapsack_volume - limit):
            limit += item[0]
            importance += item[1]
            individual[value] = 1
        else:
            break
    
    return (individual, limit, importance)

# def mutate(population):

def crossover(bag1, bag2):
    bag1_items = bag1[0]
    bag2_items = bag2[0]

    ceil = math.ceil(len(bag1_items)/2)

    #print(bag1_items[:ceil])
    #print(bag2_items[ceil:])

    s1 = bag1_items[:ceil] + bag2_items[ceil:]
    s2 = bag2_items[:ceil] + bag1_items[ceil:]

    print("CASAMENTO")
    print(bag1)
    print(bag2)
    print(bag_info(s1))
    print(bag_info(s2))
    print()

    


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

def read_csv(name):
    global knapsack_length
    global knapsack_volume
    with open(name) as csv_file:
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

read_csv('tests/item_50.csv')
#print(knapsack_volume)
gen_population(10)



# print(knapsack_length)
