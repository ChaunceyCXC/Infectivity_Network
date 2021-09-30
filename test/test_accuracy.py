
import numpy as np
from analysis import simulation, learning_MLE

# in this test case, we get a influence matrix of group chat which changed with time.
if __name__ == '__main__':
    D = 3
    A = np.random.rand(D, D)
    np.fill_diagonal(A, 0)
    A[0, 1] = 1
    A[0, 2] = 0.5
    A[1, 0] = 0.3
    A[2, 0] = 0.5
    A_t = np.zeros((D, D))
    for i in range(500):
        init = np.random.randint(0, D-1)
        simulator = simulation.Simulator(A, D, init)
        simulator.simulation()
        time_sequence = simulator.time_sequence
        user_sequence = simulator.user_sequence
        A_add, mu_t = learning_MLE.learning_by_mle(D, time_sequence, user_sequence, 30, 0.01)
        A_t = A_t + A_add
    A_t = A_t/50
    print(A_t)
    print(A)