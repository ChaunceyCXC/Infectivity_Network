import numpy as np
from uti import utility


class Simulator:
    def __init__(self, A, D, init):
        self.D = D
        self.A = A
        # self.mu = np.random.rand(D, 1)
        self.T = 200
        self.user_sequence = [init]
        self.time_sequence = [0]
        self.trigger_sequence = [0]
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
            #if v <= decayed_arr / arr:
            if v <= 1:
                possibility = decayed_arr_ls / decayed_arr
                d = np.random.choice(self.D, 1, p=possibility)
                newspeaker = d[0]
                influenceArray=[]
                for i in range(len(self.user_sequence)):
                    t_difference = t-self.time_sequence[i]
                    influencer = self.user_sequence[i]
                    decay = utility.g(0.01, t_difference)
                    influence_element = self.A[influencer][newspeaker] * decay
                    influenceArray.append(influence_element)
                poss = influenceArray/sum(influenceArray)
                index = np.random.choice(len(self.user_sequence),1,p=poss)
                max_value = max(influenceArray)
                max_index = influenceArray.index(max_value)
                self.trigger_sequence.append(max_index)
                self.user_sequence.append(newspeaker)
                self.time_sequence.append(t)


if __name__ == '__main__':
    D = 5
    A = np.random.rand(D, D)
    print(A)
    np.fill_diagonal(A, 0)
    init = np.random.randint(0, D - 1)
    simulator = Simulator(A, D,init)
    simulator.simulation()
    print(simulator.time_sequence)
    print(simulator.user_sequence)
