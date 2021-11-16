import numpy as np


def learning_by_TimeWindow(D, user_sequence, time_sequence):
    A = np.zeros((D, D))
    length = len(user_sequence)

    for i in range(1, length):
        last_user = user_sequence[i-1]
        current_user = user_sequence[i]
        current_time = time_sequence[i]
        for x in range(i-1,-1,-1):
            if time_sequence[i] - time_sequence[x] < 50:
                last_user = user_sequence[x]
                A[last_user][current_user]+=1
    ma= np.matrix(A)
    maxv= np.max(ma)
    A/maxv
    return A

def learning_by_replies(D, user_sequence, time_sequence ,reply_embedding):
    A = np.zeros((D, D))
    length = len(reply_embedding)

    for i in range(length):
        for j in range(i+1):
                di = user_sequence[i+1]
                dj = user_sequence[j]
                A[dj, di] += reply_embedding[i][j]
    ma = np.matrix(A)
    maxv = np.max(ma)
    A / maxv
    return A
  

