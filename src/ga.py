#!/usr/bin/python3
# ga.py
# William O'Brien 07/08/2021

import numpy as np
import joblib
import os

class GeneticAlgorithm:

    def __init__(self, model, X_scale, y_scale, parameters, boundaries, pop_size=10):
        '''
        model - model to evalute fitness on (may need to adjust model_fitness() to work w different models)
        X_scale - Scaler model for features
        y_scale - Scaler model for labels
        parameters - list of parameters to optimize
        boundaries - list of tuples with lower and upper bounds of parameters
        mode - minimize or maximize input function (porosity=minimize, tensile_strength=maximize)
        pop_size - default=10, number of samples to keep in population at a time
        '''

        # make on initialization of object
        self.model = model
        self.X_scale = X_scale
        self.y_scale = y_scale 
        self.parameters = parameters
        self.boundaries = boundaries

        # optional changes
        self.pop_size = pop_size
        self.population = self.initialize_pop(pop_size)


    def initialize_pop(self, size):
        '''
        input:
            size - size of the population
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
        Fitness function, sends in a feature set and returns a prediction at that point
        input:
            parameters - 1D dictionary of {parameter : value}
        output:
            prediction of the model given the feature set 
        '''
        parameters = self.X_scale.transform([list(parameters.values())])
        prediction = self.y_scale.inverse_transform(self.model.predict(parameters))[0]

        if type(prediction) is np.ndarray:
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


    def roulette_select(self, sorted, summation):
        '''
        Selection technique that gives higher probability of selection based on highest fitness
        Pros:
            Free from bias
        Cons:
            Risk of premature convergence, requires sorting to scale negative fitness values,
            depends on variance present in the fitness function
        '''
        offset = 0

        lowest_fitness = self.model_fitness(sorted[0])
        if lowest_fitness < 0:
            offset = -lowest_fitness
            summation += offset * len(sorted)

        draw = np.random.uniform(0, 1)

        range = 0
        for individual in sorted:
            fitness = self.model_fitness(individual) + offset
            p = fitness / summation
            range += p

            if draw <= range:
                return individual

    def rank_select(self, sorted, summation):
        '''
        Selection technique that gives higher probability of selection to the highest ranks
        Pros:
            Free from bias, preserves diversity, faster than roulette in this implementation
        Cons:
            Sorting required can be computationally expensive (although this version of roulette
            also requires sorting)
        '''
        range = 0
        draw = np.random.uniform(0,1)
        for idx, individual in enumerate(sorted, start=1):
            p = idx / summation
            range += p
            if draw <= range:
                return individual

    def sort_pop(self, population):
        '''
        Takes a list of dictionaries (parameter : value pairs) and returns 
        sorted list by model_fitness, smallest to largest val
        '''
        return sorted(population, key=self.model_fitness)


    def crossover(self, a, b):
        '''
        Crossover function takes two given individuals and returns
        a dictionary of {paramter : value} pairs based on averages
        --> Open to ideas for other crossover techniques
        '''
        cross = {}
        for (k,v), (_,v2) in zip(a.items(), b.items()):
            cross[k] = np.mean([v, v2])
        return self.mutation(cross)


    def mutation(self, individual):
        '''
        Generates mutation of indiviudal. Mutation can be modified to increase or decrease by a higher amount.
        Mutation currently adjusts values by adding or decreasing by a random number between 5% of the mean of
        the feature's boundaries.
        --> Open to ideas on ways to dynamically shrink mutation probability, maybe based on rank?
        '''
        x = 0
        for k in individual.keys():
            bound = self.mutation_rate*np.mean(self.boundaries[x])
            itr = individual[k] + np.random.uniform(-bound, bound)
            individual[k] = min( max(itr, self.boundaries[x][0]), self.boundaries[x][1] )
            x += 1
        return individual


    def mating_pool(self):
        '''
        Generates a new population using selection, crossover, and mutation techniques (mutation occurs in crossover)
        '''
        mpool = []
        sorted = self.sort_pop(self.population)

        if self.select == self.roulette_select:
            summation = sum(self.model_fitness(individual) for individual in self.population)
        elif self.select == self.rank_select:
            summation = sum(range(1, self.pop_size+1))

        for _ in range(self.pop_size):
            x1 = self.select(sorted, summation)
            x2 = self.select(sorted, summation)
            mpool.append(self.crossover(x1, x2))

        return mpool


    def run(self, mode='maximize', select='rank', mutation_rate=.01, generations=500, verbose=False):
        '''
        inputs:
            mutation_rate - have the option to set the probability at which an individual mutates
            generations - set max number of generations to run
            select - option to choose selection technique between roulette and rank selection
            verbose - option to print generation #'s and populations for each generation
        output:
            Dictionary feature value set of the highest performing individual in the final population
        '''
        # set mutation probability before each run
        if mutation_rate == 'dynamic':
            self.dynamic = True
            self.mutation_rate = .02
        else:
            self.dynamic = False
            self.mutation_rate = mutation_rate
        
        # set selection technique
        if select == 'roulette':
            self.select = self.roulette_select
        elif select == 'rank':
            self.select = self.rank_select
        else:
            raise ValueError(f'{select} invalid : opt [roulette/rank]')

        # set maximize or minimize function
        self.mode = mode
        if mode != 'maximize' and mode != 'minimize':
            raise ValueError(f'{mode} invalid : opt [maximize/minimize]')
        
        # Run the number of generations
        if verbose:
            print('Genetic Algorithm Walk\n----------------------')
        for x in range(generations):
            self.population = self.mating_pool()
            if verbose:
                print(f'\nGENERATION {x+1}')
                for indiviudal in self.population:
                    print(indiviudal)
        return self.sort_pop(self.population)[-1]


    def export(self, best=None):
        '''
        input:
            best - genetic algorithm dictionary output
        Writes output into reports folder
        If no parameter given, will run genetic algorithm with default parameters
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
    ga = GeneticAlgorithm(SVR, X_scale, y_scale, parameters, boundaries, pop_size=30)
    
    # Test make prediction
    predict = ga.model_predict({'LaserPowerHatch':300, 'LaserSpeedHatch':1200})
    
    # Run the algorithm to find optimal parameter set
    best_performer = ga.run(generations=200, verbose=True, select='rank', mode='minimize')
    ga.export(best_performer) # best is optional, can have export run the algorithm instead
