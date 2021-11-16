import numpy as np
from analysis import simulation, learning_MLE, learning_MLE_withText
from analysis.learning_replies import learning_by_TimeWindow, learning_by_replies
from analysis.metric import averageError, pearsoner
from data import dataOperation

# in this test case, we get a influence matrix of group chat which changed with time.
if __name__ == '__main__':
    D = 4
    A = np.random.rand(D, D)
    np.fill_diagonal(A, 0)
    Aw = np.zeros((D, D))
    Ar = np.zeros((D, D))
    A_t = np.zeros((D, D))
    A_t_text = np.zeros((D, D))
    ite_number = 0
    for i in range(10000):
        init = np.random.randint(0, D - 1)
        simulator = simulation.Simulator(A, D, 0)
        simulator.simulation()
        time_sequence = simulator.time_sequence
        user_sequence = simulator.user_sequence
        trigger_sequence = simulator.trigger_sequence
        simulated_replyembedding = dataOperation.simulate_reply_embedding(trigger_sequence)
        if len(time_sequence) < 10:
            continue
        w = 0.01
        simulated_replyembedding = dataOperation.simulate_reply_embedding(trigger_sequence)
        A_add_tw = learning_by_TimeWindow(4, user_sequence, time_sequence)
        A_add_r = learning_by_replies(4, user_sequence, time_sequence, simulated_replyembedding)
        A_add, mu_t = learning_MLE.learning_by_mle(D, time_sequence, user_sequence, 100, w)
        A_add_text, mu_t_text = learning_MLE_withText.learning_by_mle_withtext(D, time_sequence, user_sequence,
                                                                               simulated_replyembedding, 100, w)
        Aw += A_add_tw
        Ar += A_add_r
        A_t = A_t + A_add
        A_t_text += A_add_text
        ite_number += 1
        if ite_number == 100:
            break
    Aw /= 100
    Ar /= 100
    A_t /= 100
    A_t_text /= 100

    error1 = averageError(A, Aw)
    error2 = averageError(A, Ar)
    error3= averageError(A, A_t)
    error4= averageError(A, A_t_text)
    pear1 = pearsoner(A, Aw)
    pear2 = pearsoner(A, Ar)
    pear3  = pearsoner(A, A_t)
    pear4 = pearsoner(A, A_t_text)

    print(error1,error2, error3, error4)
    print(pear1,pear2, pear3, pear4)
