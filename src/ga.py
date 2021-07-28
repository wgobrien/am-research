#!/usr/bin/python3
# ga.py
# William O'Brien 07/08/2021

import numpy as np
import joblib
import os

class GeneticAlgorithm:

    def __init__(self, model, X_scale, y_scale, parameters, boundaries, mode='maximize', pop_size=10):
        '''
        model - model to evalute fitness on (may need to adjust model_fitness() to work w different models)
        X_scale - Scaler model for features
        y_scale - Scaler model for labels
        parameters - list of parameters to optimize
        boundaries - list of tuples with lower and upper bounds of parameters
        mode - minimize or maximize input function (porosity=minimize, tensile_strength=maximize)
        pop_size - default=10, number of samples to keep in population at a time
        '''
        self.model = model
        self.X_scale = X_scale
        self.y_scale = y_scale 
        self.parameters = parameters
        self.boundaries = boundaries

        self.mode = mode
        self.pop_size = pop_size
        self.population = self.generate_population(pop_size)


    def generate_population(self, size):
        '''
        input:
            size - number of feature combinations to generate
        output:
            list of dictionaries with sample parameter values
        '''

        if len(self.parameters) != len(self.boundaries):
            raise ValueError('Parameter list must match boundaries')

        population = []
        for _ in range(size):
            individual = {}
            for idx, parameter in enumerate(self.parameters):
                individual[parameter] = np.random.uniform(low=self.boundaries[idx][0], high=self.boundaries[idx][1])
            population.append(individual)

        return population


    def model_fitness(self, parameters):
        '''
        Fitness function
        input:
            parameters - 1D dictionary of {parameter : value}
        output:
            prediction of the model given the feature set 
        '''
        parameters = self.X_scale.transform([list(parameters.values())])
        prediction = self.y_scale.inverse_transform(self.model.predict(parameters))[0]

        if type(prediction) is list:
            prediction = prediction[0]

        if self.mode == 'minimize':
            return prediction*-1
        else:
            return prediction

    
    def model_predict(self, parameters):
        '''
        Similar to fitness test but doesn't worry about minimization or maximization
        '''
        parameters = self.X_scale.transform([list(parameters.values())])
        prediction = self.y_scale.inverse_transform(self.model.predict(parameters))[0]

        if type(prediction) is np.ndarray:
            prediction = prediction[0]
        
        return prediction


    def choice_by_roulette(self, sorted_population, fitness_sum):
        offset = 0
        normalized_fitness_sum = fitness_sum

        lowest_fitness = self.model_fitness(sorted_population[0])
        if lowest_fitness < 0:
            offset = -lowest_fitness
            normalized_fitness_sum += offset * len(sorted_population)

        draw = np.random.uniform(0, 1)

        accumulated = 0
        for individual in sorted_population:
            fitness = self.model_fitness(individual) + offset
            probability = fitness / normalized_fitness_sum
            accumulated += probability

            if draw <= accumulated:
                return individual


    def sort_population_by_fitness(self, population):
        '''
        Takes a list of dictionaries (parameter : value pairs) and returns 
        sorted list by model_fitness, smallest to largest val
        '''
        return sorted(population, key=self.model_fitness)
        

    def crossover(self, a, b):
        '''
        crossover function takes two given individuals and returns
        a dictionary of paramter : value pairs based on averages
        '''
        cross = {}
        for (k,v), (_,v2) in zip(a.items(), b.items()):
            cross[k] = np.mean([v, v2])
        return cross


    def mutate(self, individual, mutation_rate=.01):
        '''
        Generates mutation of indiviudal. Mutation can be modified to increase or decrease by a higher amount.
        Mutation currently adjusts values by adding or decreasing by a random number between 5% of the mean of
        the feature's boundaries. This percentage could be adjusted to shrink dynamically as we approach a solution.
        '''
        x = 0
        for k in individual.keys():
            bound = mutation_rate*np.mean(self.boundaries[x])
            individual[k] += np.random.uniform(-bound, bound)
            x += 1
        return individual


    def make_next_generation(self, previous_population, mutation_rate=.01):
        next_generation = []
        sorted_by_fitness_population = self.sort_population_by_fitness(previous_population)
        fitness_sum = sum(self.model_fitness(individual) for individual in self.population)

        for _ in range(self.pop_size):
            x1 = self.choice_by_roulette(sorted_by_fitness_population, fitness_sum)
            x2 = self.choice_by_roulette(sorted_by_fitness_population, fitness_sum)

            individual = self.crossover(x1, x2)
            individual = self.mutate(individual, mutation_rate)
            next_generation.append(individual)

        return next_generation


    def run(self, mutation_rate=.01, generations=100, verbose=False):
        if verbose:
            print('Genetic Algorithm Walk\n----------------------')
        for x in range(generations):
            if verbose:
                print(f'\nGENERATION {x+1}')
                for indiviudal in self.population:
                    print(indiviudal)
            self.population = self.make_next_generation(self.population, mutation_rate)
        return self.sort_population_by_fitness(self.population)[-1]


    def export(self, best=None):
        '''
        input:
            best - genetic algorithm dictionary output
        Write output into reports folder
        '''

        if best==None:
            best = self.run()
        # open output file for writing
        out_path = os.path.join(os.path.dirname(__file__), '../report/optimize_parameters.txt')

        if os.path.exists(out_path):
            out = open(out_path, 'a')
        else:
            out = open(out_path, 'w')
            out.write('=======================\nOptimal Paramter Report\n=======================\n')
            
        out.write(f'\n=======================================\n')
        print(f'[{self.model}]\n---------------------------------------')
        out.write(f'[{self.model}]\n---------------------------------------\n')

        for k, v in best.items():
            print(f'{k}: {v}')
            out.write(f'{k}: {v}\n')
        
        print('---------------------------------------\nPorosity:', self.model_predict(best))
        out.write(f'---------------------------------------\nPorosity: {self.model_predict(best)}\n')
        out.write(f'=======================================\n')

        out.close()


if __name__ == '__main__':
    # path to models
    models_path = os.path.join(os.path.dirname(__file__), '../models/')

    # Load svr model
    svr1_path = os.path.join(models_path, 'svr_model.pkl')
    SVR = joblib.load(svr1_path)
    
    # Load scaler models for predictions
    X_scale_path = os.path.join(models_path, 'scalers/X_scale.pkl')
    y_scale_path = os.path.join(models_path, 'scalers/y_scale.pkl')
    X_scale = joblib.load(X_scale_path)
    y_scale = joblib.load(y_scale_path)

    # Create GA object
    parameters = ['LaserPowerHatch', 'LaserSpeedHatch']
    boundaries = [(100,400), (600,1200)]
    ga = GeneticAlgorithm(SVR, X_scale, y_scale, parameters, boundaries, pop_size=30, mode='minimize')
    
    # Make prediction
    predict = ga.model_predict({'LaserPowerHatch':300, 'LaserSpeedHatch':1200})
    
    # Run the algorithm to find optimal parameter set
    best = ga.run(generations=500,verbose=True)
    ga.export(best) # best is optional, can have export run the algorithm instead
    
