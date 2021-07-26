#!/usr/bin/python3
# ga.py
# William O'Brien 07/08/2021

import numpy as np

def generate_population(size, x_boundaries, y_boundaries):
    lower_x_boundary, upper_x_boundary = x_boundaries
    lower_y_boundary, upper_y_boundary = y_boundaries

    population = []
    for i in range(size):
        individual = {
            "LaserPowerHatch": np.random.uniform(lower_x_boundary, upper_x_boundary),
            "LaserSpeedHatch": np.random.uniform(lower_y_boundary, upper_y_boundary),
        }
        population.append(individual)

    return population

def choice_by_roulette(sorted_population, fitness_sum):
    offset = 0
    normalized_fitness_sum = fitness_sum

    lowest_fitness = apply_function(sorted_population[0])
    if lowest_fitness < 0:
        offset = -lowest_fitness
        normalized_fitness_sum += offset * len(sorted_population)

    draw = np.random.uniform(0, 1)

    accumulated = 0
    for individual in sorted_population:
        fitness = model_predict(individual) + offset
        probability = fitness / normalized_fitness_sum
        accumulated += probability

        if draw <= accumulated:
            return individual

def sort_population_by_fitness(population):
    return sorted(population, key=model_predict)


def crossover(individual_a, individual_b):
    xa = individual_a["LaserPowerHatch"]
    ya = individual_a["LaserSpeedHatch"]

    xb = individual_b["LaserPowerHatch"]
    yb = individual_b["LaserSpeedHatch"]

    return {"LaserPowerHatch": (xa + xb) / 2, "LaserSpeedHatch": (ya + yb) / 2}


def mutate(individual):
    next_x = individual["LaserPowerHatch"] + np.random.uniform(-0.05, 0.05)
    next_y = individual["LaserSpeedHatch"] + np.random.uniform(-0.05, 0.05)

    lower_boundary, upper_boundary = (-4, 4)

    # Guarantee we keep inside boundaries
    next_x = min(max(next_x, lower_boundary), upper_boundary)
    next_y = min(max(next_y, lower_boundary), upper_boundary)

    return {"LaserPowerHatch": next_x, "LaserSpeedHatch": next_y}


def make_next_generation(previous_population):
    next_generation = []
    sorted_by_fitness_population = sort_population_by_fitness(previous_population)
    population_size = len(previous_population)
    fitness_sum = sum(model_predict(individual) for individual in population)

    for i in range(population_size):
        first_choice = choice_by_roulette(sorted_by_fitness_population, fitness_sum)
        second_choice = choice_by_roulette(sorted_by_fitness_population, fitness_sum)

        individual = crossover(first_choice, second_choice)
        individual = mutate(individual)
        next_generation.append(individual)

    return next_generation

def model_predict(features, model, X_scale, y_scale, energy=False):
    '''
    input:
        features - 1D list to predict value
        model - model to run prediction on
        X_scale, y_scale - scalers used to transform data
        energy - boolean value, whether or not EnergyDensity is the main parameter
    output:
        prediction of the model given the feature set 
    '''
    features = X_scale.transform([features])

    if energy == True:
        features = features[:,-1].reshape(-1,1)
    else:
        features = features[:,:-1]

    return y_scale.inverse_transform(model.predict(features))[0]