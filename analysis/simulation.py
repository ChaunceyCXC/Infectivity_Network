import numpy as np
from uti import utility


class Simulator:
    def __init__(self, A, D, init):
        self.D = D
        self.A = A
        # self.mu = np.random.rand(D, 1)
        self.T = 300
        self.user_sequence = [init]
        self.time_sequence = [0]

    def getArr_rate(self, t):
        arr_rate = np.zeros(self.D)
        for i in range(len(self.user_sequence)):
            time_diff = t - self.time_sequence[i]
            user = self.user_sequence[i]
            decay = utility.g(0.01, time_diff)
            influ_i = self.A[user] * decay
            arr_rate = arr_rate + influ_i
        return arr_rate

    def simulation(self):
        t = 0
        while t < self.T:
            arr_ls = self.getArr_rate(t)
            arr = np.sum(arr_ls)
            u = np.random.uniform(0, 1)
            w = -np.log(u) / arr
            t = t + w
            v = np.random.uniform(0, 1)
            decayed_arr_ls = self.getArr_rate(t)
            decayed_arr = np.sum(decayed_arr_ls)
            if v <= decayed_arr / arr:
                possibility = decayed_arr_ls / decayed_arr
                d = np.random.choice(self.D, 1, p=possibility)
                self.user_sequence.append(d[0])
                self.time_sequence.append(t)


if __name__ == '__main__':
    D = 5
    A = np.random.rand(D, D)
    np.fill_diagonal(self.A, 0)
    simulator = Simulator(A, D)
    simulator.simulation()
    print(simulator.time_sequence)
    print(simulator.user_sequence)
