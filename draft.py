import csv
from random import seed
from random import randint
import random

knapsack_size = 0
# print(f'Processed {POPULATION_SIZE} lines.')
# print(items)


def gen_population(n=50):
    population = []
    for i in range(n):
        population.append(gen_individual())
        # print("pi")
    return population

def gen_individual():
    individual = []
    for i in range(knapsack_size):
        value = randint(0, 1)
        individual.append(value)
        # print(i)
    return individual

# def mutate(population):


def read_csv(name):
    global knapsack_size
    items = []
    with open(name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for rows in csv_reader:
            if line_count > 1:
                items.append(rows)
                # print(rows)
                # item = [itemId, volume, importance]
                # print(item)
                # items.append(item)
            line_count += 1
        knapsack_size = line_count - 2
    return items


if __name__ == "__main__":
    # print(knapsack_size)
    random.seed(0)
    value = randint(0, 1)
    print(value)
    # items = read_csv('tests/item_50.csv')
    # population = gen_population()
    # print(population)
    # print(knapsack_size)
