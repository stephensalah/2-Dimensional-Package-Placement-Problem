import random
from math import fabs

# Define the problem parameters
num_packages = 10
weights = [[random.randint(1, 10) for _ in range(num_packages)] for _ in range(num_packages)]
locations = [[random.uniform(0, 10), random.uniform(0, 10)] for _ in range(num_packages)]

# Define the genetic algorithm parameters
population_size = 50
num_generations = 100
crossover_prob = 0.5
mutation_prob = 0.2

# Define the fitness function
def evaluate_permutation(individual):
    sum_weights = 0.0
    sum_manhattan_dist = 0.0
    for i in range(num_packages):
        for j in range(i + 1, num_packages):
            sum_weights += weights[individual[i]][individual[j]]
            sum_manhattan_dist += fabs(locations[individual[i]][0] - locations[individual[j]][0]) + fabs(locations[individual[i]][1] - locations[individual[j]][1])
    return (sum_weights, sum_manhattan_dist)

# Define the genetic algorithm functions
def init_population(population_size):
    population = []
    for i in range(population_size):
        individual = list(range(num_packages))
        random.shuffle(individual)
        population.append(individual)
    return population

def select_parents(population):
    parent1 = random.choice(population)
    parent2 = random.choice(population)
    while parent2 == parent1:
        parent2 = random.choice(population)
    return parent1, parent2

def crossover(parent1, parent2):
    child = [None] * num_packages
    start = random.randint(0, num_packages - 1)
    end = random.randint(start + 1, num_packages)
    for i in range(start, end):
        child[i] = parent1[i]
    j = 0
    for i in range(num_packages):
        if child[i] is None:
            while parent2[j] in child:
                j += 1
            child[i] = parent2[j]
            j += 1
    return child

def mutate(individual):
    if random.random() < mutation_prob:
        idx1 = random.randint(0, num_packages - 1)
        idx2 = random.randint(0, num_packages - 1)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

def select_population(population):
    fitnesses = [evaluate_permutation(individual) for individual in population]
    non_dominated_individuals = []
    for i in range(len(population)):
        is_dominated = False
        for j in range(len(population)):
            if i == j:
                continue
            if fitnesses[i][0] > fitnesses[j][0] and fitnesses[i][1] > fitnesses[j][1]:
                is_dominated = True
                break
        if not is_dominated:
            non_dominated_individuals.append(population[i])
    return non_dominated_individuals[:population_size]

# Create the initial population
population = init_population(population_size)

# Run the genetic algorithm
for generation in range(num_generations):
    offspring = []
    for i in range(population_size):
        parent1, parent2 = select_parents(population)
        child = crossover(parent1, parent2)
        mutate(child)
        offspring.append(child)
    population = select_population(population + offspring)

# Print the final solutions
fitnesses = [evaluate_permutation(individual) for individual in population]
for individual, fitness in zip(population, fitnesses):
    print("Individual:", individual, "Fitness:", fitness)
