import numpy as np


def learning_by_replies(user_sequence, reply_embeding):
    D = len(set(user_sequence))
    A = np.zeros((D, D))
    length = len(reply_embeding)

    for i in range(length):
        for j in range(i+1):
          # if reply_embeding[i][j] > 0.8:
                di = user_sequence[i+1]
                dj = user_sequence[j]
                A[dj, di] += reply_embeding[i][j]
    return A


  

