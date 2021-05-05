import numpy as np
from data import dataOperation
from analysis import learning_MLE
from analysis import learning_MLE_withText
from analysis import learning_replies
if __name__ == '__main__':
    filepath = "/home/xucan/Downloads/Telegram Desktop/Credit/Chat/chat.csv"
    sequence = dataOperation.read_dialogue_sequence(filepath, 1)
    time = dataOperation.get_time_sequence(sequence)
    user = dataOperation.get_user_sequence(sequence)
    reply = dataOperation.read_reply_embedding("../data/reply_embedding.json")
    A , mu = learning_MLE.learning_by_mle(time, user, 100)
    A_t, mu_t = learning_MLE_withText.learning_by_mle_withtext(time, user, reply["1"], 100)
    A_r =learning_replies.learning_by_replies(user, reply["1"])

    A_sum= A.sum(axis=1)
    A_t_sum = A_t.sum(axis=1)
    A_r_sum = A_r.sum(axis=1)

    maxvalue = np.amax(A)
    A = A/maxvalue
    print(A)
    print(mu)