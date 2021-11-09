import os.path

import numpy as np
from analysis import simulation, learning_MLE, learning_MLE_withText
from data import dataOperation


class synthesizer_tester:
    def __init__(self,folder):
        self.folder = folder
        self.source_dir = "/home/chauncey/PycharmProjects/Parsing_Telegram_Chat_History/data/synthesizer_data/"+self.folder+"/"   # source file from chitchat
        self.time_user = os.path.join(self.source_dir,"tu_sequence.json")
        self.embedding = os.path.join(self.source_dir,"reply_BST_1_98.json")
    def test_accuracy(self):

        for i in range(10000):
            time_sequence = simulator.time_sequence
            user_sequence = simulator.user_sequence

            w = 0.01
            A_add, mu_t = learning_MLE.learning_by_mle(D, time_sequence, user_sequence, 100, w)
            A_add_text, mu_t_text = learning_MLE_withText.learning_by_mle_withtext(D, time_sequence, user_sequence,
                                                                                   replyembedding, 100, w)

        A_t /= 200
        A_t_text /= 200
















if __name__ == '__main__':
    D = 3
    A = np.random.rand(D, D)
    np.fill_diagonal(A, 0)
    A[0, 1] = 0.8
    A[0, 2] = 0.8
    A[1, 0] = 0.3
    A[1, 2] = 0.3
    A[2, 0] = 0.8
    A[2, 1] = 0.3

    A_t = np.zeros((D, D))
    A_t_text = np.zeros((D, D))
    ite_number = 0
    for i in range(10000):
        init = np.random.randint(0, D - 1)
        simulator = simulation.Simulator(A, D, init)
        simulator.simulation()
        time_sequence = simulator.time_sequence
        user_sequence = simulator.user_sequence
        trigger_sequence = simulator.trigger_sequence
        simulated_replyembedding = dataOperation.simulate_reply_embedding(trigger_sequence)
        if len(time_sequence) < 10:
            continue
        w = 0.01
        simulated_replyembedding = dataOperation.simulate_reply_embedding(trigger_sequence)
        A_add, mu_t = learning_MLE.learning_by_mle(D, time_sequence, user_sequence, 100, w)
        A_add_text, mu_t_text = learning_MLE_withText.learning_by_mle_withtext(D, time_sequence, user_sequence,
                                                                               simulated_replyembedding, 100, w)
        A_t = A_t + A_add
        A_t_text += A_add_text
        ite_number += 1
        if ite_number == 200:
            break
    A_t /= 200
    A_t_text /= 200

    print(A_t)
    print(A_t_text)

    print(A)
