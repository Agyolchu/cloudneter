import random
import numpy as np
from math import exp


class CloudDataGenerator(object):
    def __init__(self, number_of_packages, number_of_storages, sliced_parts, size_of_the_storage):
        self.size1 = number_of_packages
        self.size2 = number_of_storages
        self.a = sliced_parts
        self.b = size_of_the_storage

    def initial_solution(self):
        secure_random = random.SystemRandom()
        x = np.zeros((self.size1, self.size2))
        allowed_positions = list(range(self.size2))
        print(allowed_positions)
        ll = list(range(self.size1))
        while len(ll) > 0:
            idx_i = secure_random.choice(ll)
            idx_k = random.randint(0, len(allowed_positions) - 1)
            if self.a[idx_i] <= self.b[idx_k]:
                x[idx_i, idx_k] = 1
                self.b[idx_k] = self.b[idx_k] - self.a[idx_i]
            else:
                x[idx_i, idx_k] = 0
            ll.remove(idx_i)
        return x

    def data_transfer_cost(self, costf, solution):
        new_c = 0
        for i in range(solution.shape[0]):
            inn = np.inner(solution[i], costf[i])
            new_c += inn
        new_c = new_c * self.a[0]
        return new_c

    def neighbour_node(self, old_sol):
        list1 = self.a
        list2 = self.b
        new_x = np.zeros((self.size1, self.size2))
        allowed_positions = list(range(self.size2))
        ll = list(range(self.size1))
        secure_random = random.SystemRandom()

        while len(ll) == self.size1 - 1:

            idx_i = secure_random.choice(ll)
            idx_k = secure_random.choice(allowed_positions)
            if old_sol[idx_i] == np.zeros((self.size2,)):
                if list1[idx_i] <= list2[idx_k]:
                    new_x[idx_i, idx_k] = 1
                    list2[idx_k] = list2[idx_k] - list1[idx_i]
                else:

                    while list1[idx_i] > list2[idx_k]:
                        if idx_k < (self.size2 - 1):
                            idx_k = idx_k + 1
                        else:
                            idx_k = idx_k - 1
                    new_x[idx_i, idx_k] = 1
                    list2[idx_k] = list2[idx_k] - list1[idx_i]
            else:
                new_x[idx_i] = old_sol[idx_i]
                new_xi = np.sum(new_x[idx_i])
                list2[idx_k] = list2[idx_k] - list1[idx_i] * new_xi

            ll.remove(idx_i)

        while len(ll) > 0:

            idx_i = secure_random.choice(ll)
            idx_k = random.randint(0, len(allowed_positions) - 1)
            if list1[idx_i] <= list2[idx_k]:
                new_x[idx_i, idx_k] = 1
                list2[idx_k] = list2[idx_k] - list1[idx_i]
            else:
                new_x[idx_i, idx_k] = 0
            ll.remove(idx_i)
        return new_x

    def acceptance_probability(self, old_cost, new_cost, T):
        probability = exp((old_cost - new_cost) / T)
        return probability

    def simulated_annealing(self, sol, costf):
        old_cost = self.data_transfer_cost(costf, sol)
        Temperature = 1.0
        Minimum_Temprature = 0.00001
        alpha = 0.9
        while Temperature > Minimum_Temprature:
            i = 1
            while i <= 100:
                new_sol = self.neighbour_node(sol)
                new_cost = self.data_transfer_cost(costf, new_sol)
                acceptance_prob = self.acceptance_probability(old_cost, new_cost, Temperature)
                if acceptance_prob > random():
                    sol = new_sol
                    old_cost = new_cost
                i += 1
            Temperature = Temperature * alpha
        return sol, self.data_transfer_cost


if __name__ == '__main__':
    a = np.array((4, 4, 4))
    b = np.array((6, 2, 18, 16))
    size1 = a.shape[0]
    size2 = b.shape[0]
    cloudy = CloudDataGenerator(size1, size2, a, b)
    sol = cloudy.initial_solution()
    cost = np.array(((0.6, 0.2, 0.1, 0.5), (0.2, 0.3, 0.1, 0.2), (0.5, 0.2, 0.1, 0.6)))
    print(cloudy.acceptance_probability(1, 2, 1234))
    print(cloudy.neighbour_node(sol))
    print(cloudy.simulated_annealing(cost,sol))
