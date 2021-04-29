import numpy as np

from data import dataOperation
from uti import utility
from analysis import learning_MLE
from analysis import learning_MLE_withText

if __name__ == '__main__':
    filepath = "/home/xucan/Downloads/Telegram Desktop/Credit/Chat/chat.csv"
    sequence = dataOperation.read_dialogue_sequence(filepath, 1)
    time = dataOperation.get_time_sequence(sequence)
    user = dataOperation.get_user_sequence(sequence)
    reply = dataOperation.read_reply_embedding("../data/reply_embedding.json")
    A , mu = learning_MLE.learning_by_mle(time, user, 10)
    As, mus = learning_MLE_withText.learning_by_mle_withtext(time, user, reply["1"], 10)
    maxvalue = np.amax(A)
    A = A/maxvalue
    print(A)
    print(mu)