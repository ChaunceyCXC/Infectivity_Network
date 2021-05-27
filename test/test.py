import numpy as np
from data import dataOperation
from analysis import learning_MLE
from analysis import learning_MLE_withText
from analysis import learning_replies
from uti.utility import savegraphtotxt
import matplotlib.pyplot as plt
# in this test case, we try to get influence matrix on small group chat based on normal hawkes process and hawkes process with text. And compare the matrix we have



if __name__ == '__main__':
    ite = 100
    w = 0.01
    filepath = "/home/xucan/Downloads/Telegram Desktop/Credit/Chat/chat.csv"
    sequence = dataOperation.read_dialogue_sequence(filepath, 1)
    time = dataOperation.get_time_sequence(sequence)
    user = dataOperation.get_user_sequence(sequence)
    reply = dataOperation.read_reply_embedding("../data/reply_embedding.json")
    #A, mu = learning_MLE.learning_by_mle(time, user, ite, w)
    # A_100, mu_100 = learning_MLE.learning_by_mle(time, user, 200, w)
    A_t, mu_t = learning_MLE_withText.learning_by_mle_withtext(time, user, reply["1"], ite, w)
    # A_t100, mu_t100 = learning_MLE_withText.learning_by_mle_withtext(time, user, reply["1"], 200, w)
    plt.imshow(A_t)
    plt.colorbar()
    plt.show()

