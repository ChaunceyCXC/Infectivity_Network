
from data import dataOperation
from analysis import learning_MLE_withText


if __name__ == '__main__':
    filepath = "/home/xucan/Downloads/Telegram Desktop/Credit/Chat/chat.csv"
    reply = dataOperation.read_reply_embedding("../data/reply_embedding_100.json")
    A_t, mu_t = learning_MLE_withText.learning_sequence_by_mle_withtext(filepath, reply, 100)


    print(A_t)
    print(mu_t)