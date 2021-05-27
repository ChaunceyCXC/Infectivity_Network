import json
import os
import numpy as np

from data import dataOperation
from uti.utility import g
from uti.utility import integral_g
from uti import utility

def learning_by_mle_withtext(time_sequence, user_sequence, reply_embedding, ite , w):
    seq_length = len(time_sequence)
    # d is the number of total users and T is the end of the sequence
    D = len(set(user_sequence))
    T = time_sequence[-1]
    T += 600
    A = np.ones((D, D))
    mu = np.ones((D))
    mu = mu*w
    sum_G = np.zeros(D)
    sum_Pii = np.zeros(D)
    sum_Pji = np.zeros((D, D))
    for iteration in range(ite):
        # E- Step
        for i in range(seq_length):
            di = user_sequence[i]
            ti = time_sequence[i]
            integral = integral_g(w, T - ti)
            sum_G[di] += integral

            if i == 0:
                sum_Pii[di] += 1
            else:
                sum_influence = mu[di]
                for j in range(i):
                    dj = user_sequence[j]
                    tj = time_sequence[j]
                    if dj!=di :
                        sum_influence += (A[dj, di] * g(w, ti - tj) * reply_embedding[i - 1][j])
                sum_Pii[di] += (mu[di] / sum_influence)

                for j in range(i):
                    dj = user_sequence[j]
                    tj = time_sequence[j]
                    Pji = (A[dj, di] * g(w, ti - tj) * reply_embedding[i - 1][j]) / sum_influence
                    if dj!=di:
                       sum_Pji[dj, di] += Pji
        # M-step
        for i in range(D):
            mu[i] = sum_Pii[i] / T
        for i in range(D):
            for j in range(D):
                if sum_G[j] == 0:
                    A[j, i] = 0
                else:
                    A[j, i] = sum_Pji[j, i] / sum_G[j]
        sum_Pii = sum_Pii*0.0
        sum_Pji = sum_Pji*0.0
        sum_G = sum_G*0.0
    return A, mu



def learning_sequence_by_mle_withtext(file, reply_dict, ite, w):
    df = utility.read_csv_todf(file)
    end_id = len(reply_dict)
    user_dict = dataOperation.get_user_dict_multiple(file, 1, end_id)
    # d is the number of total users and T is the end of the sequence
    D = len(user_dict)

    A = np.ones((D, D))
    mu = np.ones((D))
    mu = mu * w
    sum_G = np.zeros(D)
    sum_Pii = np.zeros(D)
    sum_Pji = np.zeros((D, D))
    for iteration in range(ite):
        # E- Step
        sum_T = 0
        for sequence_id in reply_dict:
        #for sequence_id in range(46,47):
            sequence = df[df.sequenceID == int(sequence_id)]
            if sequence.shape[0] == 0:
                continue
            time_sequence = dataOperation.get_time_sequence(sequence)
            user_sequence = dataOperation.get_user_sequence_from_dict(sequence, user_dict)
            reply_embedding = reply_dict[str(sequence_id)]
            seq_length = len(time_sequence)
            T = time_sequence[-1] + 600
            sum_T += T
            for i in range(seq_length):
                di = user_sequence[i]
                ti = time_sequence[i]
                integral = integral_g(w, T - ti)
                sum_G[di] += integral

                if i == 0:
                    sum_Pii[di] += 1
                else:
                    sum_influence = mu[di]
                    for j in range(i):
                        dj = user_sequence[j]
                        tj = time_sequence[j]
                        if dj != di:
                            sum_influence += (A[dj, di] * g(w, ti - tj) * reply_embedding[i - 1][j])
                    sum_Pii[di] += (mu[di] / sum_influence)

                    for j in range(i):
                        dj = user_sequence[j]
                        tj = time_sequence[j]
                        Pji = (A[dj, di] * g(w, ti - tj) * reply_embedding[i - 1][j]) / sum_influence
                        if dj != di:
                            sum_Pji[dj, di] += Pji
        # M-step
        for i in range(D):
            mu[i] = sum_Pii[i] / sum_T
        for i in range(D):
            for j in range(D):
                if sum_G[j] == 0:
                    A[j, i] = 0
                else:
                    A[j, i] = sum_Pji[j, i] / sum_G[j]

        sum_Pii = sum_Pii*0.0
        sum_Pji = sum_Pji*0.0
        sum_G = sum_G*0.0
    return A, mu

if __name__ == '__main__':
    filepath = "/home/xucan/Downloads/Telegram Desktop/Credit/Chat/chat.csv"
