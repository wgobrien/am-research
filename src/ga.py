# ga.py
# William O'Brien

import numpy as np
import joblib
import os

class GeneticAlgorithm:

    def __init__(self, model, parameters, boundaries, X_scale=None, y_scale=None, pop_size=10, precision=5):
        '''
        model - model to evalute fitness (may need to adjust _model_fitness() to work w different models);

        parameters - list of parameters to optimize

        boundaries - list of tuples with lower and upper bounds of parameters

        X_scale - Scaler model for features (must match data used for model training)

        y_scale - Scaler model for labels (must match data used for model training)

        pop_size - default=10, number of samples to keep in population at a time

        precision - degree of precision to round search
        '''

        # set upon initialization of object
        self.model = model
        self.parameters = parameters
        self.boundaries = boundaries
        self.population = self._initialize_pop(pop_size)

        # optional changes (scalers req if model data is scaled)
        self.X_scale = X_scale
        self.y_scale = y_scale
        self.pop_size = pop_size
        
        # initialized in run
        self._gen = None # save for export data
        self._exp = None
        self._precision = precision

    def _initialize_pop(self, size):
        '''
        Generates the initial population to be used, attributes are set
        at random numbers between the given boundaries.

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


    def _model_fitness(self, parameters):
        '''
        Fitness function, sends in a feature set and returns a prediction at that point.

        input:
            parameters - 1D dictionary of {parameter : value}

        output:
            prediction of the model given the feature set (scaler)
        '''
        if callable(self.model) and (str(type(self.model)) == '<class \'function\'>'):
            prediction = self.model(parameters)
        else:
            if self.X_scale and self.y_scale: 
                parameters = self.X_scale.transform([list(parameters.values())])
                prediction = self.y_scale.inverse_transform(self.model.predict(parameters))[0]
            else:
                vals = np.array(list(parameters.values()))
                prediction = self.model.predict(vals.reshape(1,-1))

        if type(prediction) is np.ndarray:
            prediction = prediction[0]

        if self.mode == 'minimize':
            return prediction*-1
        else:
            return prediction


    def model_predict(self, parameters):
        '''
        Delivers a prediction from the model, doesn't worry about minimization or maximization
        such as with model_fitness.

        input:
            parameters - 1D dictionary of {parameter : value}

        output:
            prediction of the model given the feature set (scaler)
        '''
        if callable(self.model) and (str(type(self.model)) == '<class \'function\'>'):
            prediction = self.model(parameters)
        else:
            if self.X_scale and self.y_scale: 
                parameters = self.X_scale.transform([list(parameters.values())])
                prediction = self.y_scale.inverse_transform(self.model.predict(parameters))[0]
            else:
                vals = np.array(list(parameters.values()))
                prediction = self.model.predict(vals.reshape(1,-1))

        if type(prediction) is np.ndarray:
            prediction = prediction[0]

        return prediction


    def _sort_pop(self, population):
        '''
        Takes a list of dictionaries (parameter : value pairs) and returns
        sorted list by model_fitness. Output list will be in order of
        worst to best values of fitness.
        '''
        return sorted(population, key=self._model_fitness)


    def roulette_select(self, sorted_pop, summation):
        '''
        Selection technique that gives higher probability of selection based on highest fitness.

        Pros:
            Free from bias

        Cons:
            Risk of premature convergence, requires sorting to scale negative fitness values,
            depends on variance present in the fitness function
        '''
        offset = 0

        lowest_fitness = self._model_fitness(sorted_pop[0])
        if lowest_fitness < 0:
            offset = -lowest_fitness
            summation += offset * len(sorted_pop)

        draw = np.random.uniform(0, 1)

        cumulative = 0
        for idx, individual in enumerate(sorted_pop, start=1):
            fitness = self._model_fitness(individual) + offset
            p = fitness / summation
            cumulative += p

            if draw <= cumulative:
                return individual, idx


    def rank_select(self, sorted_pop, summation):
        '''
        Selection technique that gives higher probability of selection to the highest ranks.

        Pros:
            Free from bias, preserves diversity, faster than roulette in this implementation

        Cons:
            Sorting required can be computationally expensive
        '''
        cumulative = 0
        draw = np.random.uniform(0,1)
        for idx, individual in enumerate(sorted_pop, start=1):
            p = idx / summation
            cumulative += p
            if draw <= cumulative:
                return individual, idx

    def _mutation(self, individual, mutation_prob):
        '''
        Generates mutation of indiviudal by adding a random number in [-bound, bound]
        to each value in the individual's feature set. The bound is determined
        by taking a percent of the mean of the feature's bounds. In dynamic mutation,
        this percent is passed in by mutation_prob, and in normal mutation, the percent
        is given by the set mutation_rate.

        input:
            individual - a dictionary with a feature set {parameter : value}
        output:
            returns a dictionary with mutated values
        '''
        x = 0
        for k in individual.keys():
            if self.dynamic:
                bound = mutation_prob*individual[k]
            else:
                bound = self.mutation_rate*individual[k]
            itr =  individual[k] + np.random.uniform(-bound, bound)
            individual[k] = min( max(itr, self.boundaries[x][0]), self.boundaries[x][1] )
            x += 1
        return individual


    def _crossover(self, a, b):
        '''
        Crossover function takes two given individuals and
        returns a dictionary of {paramter : value} pairs based on averages.

        input:
            a, b - two individuals to crossover (dictionaries with a feature
            set {parameter : value})

        output:
            returns a single individual crossed between the input individuals
        '''
        cross = {}
        for (k,v), (_,v2) in zip(a.items(), b.items()):
            cross[k] = np.mean([v, v2])
        return cross


    def _mating_pool(self):
        '''
        Generates a new population using selection, crossover, and mutation techniques.
        '''
        mpool = []
        sorted_pop = self._sort_pop(self.population)

        if self.select == self.roulette_select:
            # roulette selection, sum of the population's total fitness
            summation = sum(self._model_fitness(individual) for individual in self.population)
        elif self.select == self.rank_select:
            # rank selection - sum of the ranks
            summation = sum(range(1, self.pop_size+1))

        for _ in range(self.pop_size - self.top):
            x1, r1 = self.select(sorted_pop, summation)
            x2, r2 = self.select(sorted_pop, summation)

            # Used for dynamic shrinking of mutation rate
            # Inverts the ranking (rk 30 --> rk 1 since feature sets with
            # better fitness have higher index)
            r1 = self.pop_size - r1 + 1
            r2 = self.pop_size - r2 + 1

            if self.dynamic:
                # Gives a smaller % of noise to higher ranked individuals
                mutation_prob = self.mutation_rate*(np.mean([r1,r2]) / self.pop_size)
            else:
                mutation_prob = None

            x_new = self._crossover(x1, x2)
            mpool.append(self._mutation(x_new, mutation_prob))

        # Keeps the highest performing individuals from the previous pool, makes sure
        # we don't skip past the best individual (allows for higher exploration rates)
        for x in range(1, self.top + 1):
            mpool.append(sorted_pop[-x])
        return mpool


    def run(self, mode='maximize', select='rank', boltzmann=True, generations=500, exploration=.25, keep_top=1, verbose=False):
        '''
        inputs:
            mode - minimize or maximize input function (porosity=minimize, tensile_strength=maximize)

            select - option to choose selection technique between roulette and rank selection

            boltzmann - entropy-Boltzmann selection, 

            generations - set max number of generations to run

            exploration - For rank or roulette, the normal mutation rate. For entropy-Boltzmann selection, tells how much to explore
            vs exploit (higher will increase perturbation for worse fitness (expand search space),
            lower value will narrow search space for worse fitness)

            verbose - option to print generation #'s and populations for each generation

            keep_top - with every generation, keeps the top N individuals for the next generation

        output:
            dictionary feature set of the highest performing individual in the final population
        '''
        self._gen = generations # save for export data
        self._exp = exploration

        # set mutation rate before each run
        if boltzmann:
            self.dynamic = True
        else:
            self.dynamic = False
        
        self.mutation_rate = exploration

        # set selection technique
        if select == 'roulette':
            self.select = self.roulette_select
        elif select == 'rank':
            self.select = self.rank_select
        else:
            raise ValueError(f'{select} invalid : opt [roulette/rank]')

        if keep_top > self.pop_size:
            print('keep_top greater than population size, defaulting to standard')
            self.top = 1
        else:
            self.top = keep_top

        # set maximize or minimize function
        if mode != 'maximize' and mode != 'minimize':
            raise ValueError(f'{mode} invalid : opt [maximize/minimize]')
        self.mode = mode

        best_hist = []
        # Run through the generations
        if verbose:
            print('Genetic Algorithm Walk\n----------------------')
        for x in range(generations):
            # append prediction to convergence history (lets us analyze converge behavior)
            best = round(self.model_predict(self._sort_pop(self.population)[-1]),self._precision)
            best_hist.append(best)
            # generate new mating pool
            self.population = self._mating_pool()
            if verbose:
                print(f'\nGENERATION {x+1}')
                for indiviudal in self.population:
                    print(indiviudal)
        # The last item in the sorted population is the highest performer
        best = self._sort_pop(self.population)[-1]
        return best, best_hist


    def export(self, best=None):
        '''
        Writes output into reports folder. If no parameter given,
        will run genetic algorithm with default parameters.

        input:
            best - genetic algorithm dictionary output
        '''

        if best==None:
            best, _ = self.run()
        # open output file for writing
        out_path = os.path.join(f, 'report/optimize_parameters.txt')

        if os.path.exists(out_path):
            out = open(out_path, 'a')
        else:
            report_dir = os.path.exists(os.path.join(os.path.dirname(__file__), 'report'))
            if not report_dir:
                os.makedirs(report_dir)
            out = open(out_path, 'w')
            out.write('================================================='
                      '\n             Optimal Paramter Report'
                      '\n================================================='
                      '\nReport with all GA runs. Shows the model, the'
                      '\nGA run outputs, and which GA settings were used.\n')

        if self.dynamic:
            mr = f'dynamic >> exploration rate: {self._exp}'
        else:
            mr = str(self.mutation_rate)

        print('\n=======================================')
        print(f'{type(self.model).__name__} Model\n---------------------------------------')
        out.write(
            '\n================================================='
            f'\n{type(self.model).__name__} Model\n-------------------------------------------------'
            f'\nGA Parameters\n-------------'
            f'\nPopulation Size: {self.pop_size}'
            f'\nGenerations: {self._gen}'
            f'\nSelect: {self.select.__name__}'
            f'\nMutation Rate: {mr}'
            f'\nKeep Top: {self.top}'
            f'\n-------------------------------------------------\nFeatures\n--------\n'
            )
        for k, v in best.items():
            print(f'{k}: {v}')
            out.write(f'{k}: {v}\n')

        out.write(f'-------------------------------------------------'
            f'\nPrediction\n----------'
            f'\n{self.model_predict(best)}'
            '\n=================================================\n'
            )
        print('---------------------------------------\nPrediction:', round(self.model_predict(best), self._precision))
        print('=======================================')

        out.close()
