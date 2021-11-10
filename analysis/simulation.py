import numpy as np
from uti import utility
from data.dataOperation import combineTopicChat

class Simulator:
    def __init__(self, A, D, init1):
        self.D = D
        self.A = A
        # self.mu = np.random.rand(D, 1)
        self.T = 300
        self.user_sequence = [init1]
        self.time_sequence = [0]
        self.trigger_sequence = [0]
        self.group_sequence =[0 ]
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
            w = -np.log(u) /(arr)
            t = t + w
            t = int(t)
            v = np.random.uniform(0, 1)
            decayed_arr_ls = self.getArr_rate(t)
            decayed_arr = np.sum(decayed_arr_ls)
            #if v <= decayed_arr / arr:
            if v <= 1:
                possibility = decayed_arr_ls / decayed_arr
                d = np.random.choice(self.D, 1, p=possibility)
                newspeaker = int(d[0])

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
                group = self.group_sequence[max_index]
                self.group_sequence.append(group)


if __name__ == '__main__':
    D =4
    A = np.random.rand(D, D)
    np.fill_diagonal(A, 0)
    A[0, 1] = 0.8
    A[0, 2] = 0
    A[0, 3] = 0
    A[1, 0] = 0.8
    A[1, 2] = 0
    A[1, 3] = 0
    A[2, 0] = 0
    A[2, 1] = 0
    A[2, 3] = 0.8
    A[3, 0] = 0
    A[3, 1] = 0
    A[3, 2] = 0.8
    np.fill_diagonal(A, 0)
    init = np.random.randint(0, D - 1)
    simulator1 = Simulator(A, D,0)
    simulator2 = Simulator(A,D,2)
    simulator1.simulation()
    simulator2.simulation()
    result = combineTopicChat(simulator1,simulator2)
    print(result)

