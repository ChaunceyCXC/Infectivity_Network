import os.path

import numpy as np
from analysis import simulation, learning_MLE, learning_MLE_withText
from analysis.learning_replies import learning_by_TimeWindow, learning_by_replies
from analysis.metric import averageError, pearsoner
from data import dataOperation
from uti.utility import read_json


class synthesizer_tester:
    def __init__(self,folder):
        self.folder = folder
        self.source_dir = "/home/chauncey/PycharmProjects/Parsing_Telegram_Chat_History/data/synthesizer_data/"+self.folder+"/"   # source file from chitchat
        self.time_user = os.path.join(self.source_dir,"tu_sequence.json")
        self.embedding = os.path.join(self.source_dir,"reply_embeding.json")
    def test_accuracy(self, count):
        D=4
        Aw = np.zeros((D, D))
        Ar = np.zeros((D, D))
        A_t = np.zeros((D, D))
        A_t_text = np.zeros((D, D))
        time_user = read_json(self.time_user)
        embedding = read_json(self.embedding)
        for i in range(1,count+1):
            group = time_user[i-1]
            user_sequence = group["user_sequence"]
            time_sequence = group["time_sequence"]
            reply_embedding = embedding[str(i)]

            w = 0.01
            A_add_tw = learning_by_TimeWindow(4,user_sequence,time_sequence)
            A_add_r = learning_by_replies(4,user_sequence,time_sequence, reply_embedding)
            A_add, mu_t = learning_MLE.learning_by_mle(4, time_sequence, user_sequence, 100, w)
            A_add_text, mu_t_text = learning_MLE_withText.learning_by_mle_withtext(4, time_sequence, user_sequence,
                                                                                   reply_embedding, 100, w)
            Aw += A_add_tw
            Ar += A_add_r
            A_t = A_t + A_add
            A_t_text += A_add_text

        Aw/= count
        Ar/=count
        A_t /= count
        A_t_text /= count
        return Aw, Ar, A_t, A_t_text
        print(A_t)
        print(A_t_text)

if __name__ == '__main__':
    a_test = synthesizer_tester("cmu_dog")
    A_tw, A_r, A_t, A_t_text = a_test.test_accuracy(100)
    A = np.random.rand(4, 4)
    A[0, 1] = 0.9
    A[0, 2] = 0.1
    A[0, 3] = 0.1
    A[1, 0] = 0.9
    A[1, 2] = 0.1
    A[1, 3] = 0.1
    A[2, 0] = 0.1
    A[2, 1] = 0.1
    A[2, 3] = 0.9
    A[3, 0] = 0.1
    A[3, 1] = 0.1
    A[3, 2] = 0.9
    np.fill_diagonal(A, 0)
    error1 = averageError(A, A_tw)
    error2 = averageError(A, A_r)
    error3= averageError(A, A_t)
    error4= averageError(A, A_t_text)
    pear1 = pearsoner(A, A_tw)
    pear2 = pearsoner(A, A_r)
    pear3  = pearsoner(A, A_t)
    pear4 = pearsoner(A, A_t_text)

    print(error1,error2, error3, error4)
    print(pear1,pear2, pear3, pear4)














