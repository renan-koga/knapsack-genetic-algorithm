import csv
import math
from random import seed
from random import randint

population = []
generation = []
inventory = []
knapsack_length = 0
knapsack_volume = 0
best_importance = 0
worst_importance = 999999
size = 50

def gen_population(n=50):
    global population
    for i in range(n):
        population.append(gen_individual())
        #rint(population[i])

def gen_next_generation():
    global generation
    global population
    global best_importance
    global worst_importance
    generation = []
    has_childs = False
    #for i in range(0, len(population), 2):
    #best_importance = get_best_importance()
    if(len(population) > 1):
        aux = get_worst_importance()
        if(aux < worst_importance):
            worst_importance = aux
        aux = get_best_importance()
        if(aux > best_importance):
            best_importance = aux
        print("TAMANHO DA POPULAÇÃO: ", len(population), " MELHOR IMPORTÂNCIA ATÉ AGORA: ", best_importance, " PIOR IMPORTÂNCIA ATÉ AGORA: ", worst_importance)
        mutate(population)
        worst_importance = get_worst_importance()
        population.sort(key=lambda x: x[2], reverse=True)
        for i in range(0, len(population)-2, 2):
            p1 = population[i]
            p2 = population[i+1]
            f1, f2 = crossover(p1, p2)
            if(f1[2] > worst_importance):
                generation.append(f1)
                has_childs = True
            if(f2[2] > worst_importance):
                generation.append(f2)
                has_childs = True
        population = generation

    return has_childs

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

def mutate(population):
    for solution in population:
        items = solution[0]
        for i in range(len(items)):
            value = randint(0, 100)
            if(value < 3):
                if(items[i] == 1):
                    items[i] = 0
                else:
                    items[i] = 1

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
#gen_population(10)
gen_population(size)
#print(population)
n_gen = 0
while(gen_next_generation()):
    print("GERAÇÃO: ", n_gen)
    n_gen = n_gen + 1