
import numpy as np
from analysis import simulation, learning_MLE

# in this test case, we get a influence matrix of group chat which changed with time.
if __name__ == '__main__':
    D = 3
    A = np.random.rand(D, D)
    np.fill_diagonal(A, 0)
    A[0, 1] = 0.8
    A[0, 2] = 0.8
    A[1, 0] = 0.2
    A[1, 2] = 0.2
    A[2, 0] = 0.8
    A[2, 1] = 0.2
    A_t = np.zeros((D, D))
    ite_number = 0
    for i in range(10000):
        init = np.random.randint(0, D-1)
        simulator = simulation.Simulator(A, D, init)
        simulator.simulation()
        time_sequence = simulator.time_sequence
        user_sequence = simulator.user_sequence
        if len(time_sequence) < 10 :
            continue
        A_add, mu_t = learning_MLE.learning_by_mle(D, time_sequence, user_sequence, 100, 0.01)
        A_t = A_t + A_add
        ite_number+=1
        if ite_number ==500:
            break
    A_t = A_t/ite_number
    print(A_t)
    print(A)