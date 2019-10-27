import numpy as np
from math import exp
import random


class CloudDataGenerator:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.size1 = a.shape[0]
        self.size2 = b.shape[0]

    def initial_solution(self):
        parts = np.array([elem for elem in self.a])
        storage = np.array([elem for elem in self.b])
        size1 = self.size1
        size2 = self.size2
        secure_random = random.SystemRandom()
        x = np.zeros((size1, size2))
        allowed_positions = list(range(size2))
        ll = list(range(size1))
        while len(ll) > 0:
            print("l1", ll)
            idx_i = secure_random.choice(ll)
            idx_k = random.randint(0, len(allowed_positions) - 1)
            print(idx_k, idx_i)

            if parts[idx_i] <= storage[idx_k]:
                x[idx_i, idx_k] = 1
                storage[idx_k] = storage[idx_k] - parts[idx_i]
            else:
                while parts[idx_i] > storage[idx_k]:
                    idx_k = random.randint(0, len(allowed_positions) - 1)
                if parts[idx_i] <= storage[idx_k]:
                    x[idx_i, idx_k] = 1
                    storage[idx_k] = storage[idx_k] - parts[idx_i]
                    print("storage", storage)
                else:
                    x[idx_i, idx_k] = 0
            ll.remove(idx_i)
        return x

    def cost(self, costf, solution):
        new_c = 0
        for i in range(solution.shape[0]):
            inn = np.inner(solution[i], costf[i])
            new_c += inn
        new_c = new_c * a[0]
        return new_c

    def neghboar(self, old_sol, list1, list2, size1, size2):
        new_x = np.zeros((size1, size2))
        allowed_positions = list(range(size2))
        ll = list(range(size1))
        secure_random = random.SystemRandom()
        idx_i = secure_random.choice(ll)
        new_x[idx_i] = old_sol[idx_i]
        idx_k = np.argmax(new_x[idx_i])
        list2[idx_k] = list2[idx_k] - list1[idx_i] * new_x[idx_i, idx_k]
        ll.remove(idx_i)
        while len(ll) > 0:
            idx_i = secure_random.choice(ll)
            idx_k = random.randint(0, len(allowed_positions) - 1)
            if list1[idx_i] <= list2[idx_k]:
                new_x[idx_i, idx_k] = 1
                list2[idx_k] = list2[idx_k] - list1[idx_i]
            else:
                while list1[idx_i] > list2[idx_k]:
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
        allcost = []
        old_cost = self.cost(costf, sol)
        T = 1.0
        T_min = 0.1
        alpha = 0.5
        while T > T_min:
            i = 1
            while i <= 100:
                a = np.array([elem for elem in self.a])
                b = np.array([elem for elem in self.b])
                size1 = a.shape[0]
                size2 = a.shape[0]
                new_sol = self.neghboar(sol, a, b, size1, size2)
                new_cost = self.cost(costf, new_sol)
                acceptance_prob = self.acceptance_probability(old_cost, new_cost, T)
                if acceptance_prob > random.random():
                    if new_cost < old_cost:
                        sol = new_sol
                        old_cost = new_cost
                i += 1
                allcost.append(new_cost)
            T = T * alpha
        print("minimum cost:" + str(min(allcost)))
        return sol, old_cost

    def main(self, costem):
        sol = self.initial_solution()
        return self.simulated_annealing(sol, costem)


if __name__ == '__main__':
    # Parameters can be used for testing algorithm of the model

    a = np.array((4, 4, 4, 4, 4))
    b = np.array((6, 2, 8, 6, 9))
    costem = np.array(((0.6, 0.2, 0.1, 0.5, 0.1), (0.2, 0.3, 0.1, 0.2, 0.1), (0.2, 0.3, 0.1, 0.2, 0.1),
                       (0.5, 0.2, 0.1, 0.6, 0.1), (0.6, 0.2, 0.1, 0.5, 0.1), (0.2, 0.3, 0.1, 0.2, 0.1),
                       (0.2, 0.3, 0.8, 0.2, 0.1), (0.2, 0.3, 0.1, 0.2, 0.71)))
    print("packet size:", a)
    print("bucket size", b)
    cloudy = CloudDataGenerator(a, b)
    new_m = cloudy.main(costem)
    print(new_m)
