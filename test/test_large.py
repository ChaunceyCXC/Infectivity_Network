
from data import dataOperation
from analysis import learning_MLE_withText
import matplotlib.pyplot as plt
import numpy as np
from uti.utility import savegraphtotxt
from communities.algorithms import louvain_method
from communities.visualization import draw_communities
from communities.visualization import louvain_animation

# in this test case, we get a influence matrix of group chat with more than 100 users.
if __name__ == '__main__':
    filepath = "/home/xucan/Downloads/Telegram Desktop/Credit/Chat/chat.csv"
    reply = dataOperation.read_reply_embedding("../data/reply_embedding_100.json")
    A_t, mu_t = learning_MLE_withText.learning_sequence_by_mle_withtext(filepath, reply, 20, 0.005)
    sumin = np.sum(A_t, axis=0)
    sumout = np.sum(A_t, axis=1)
    #savegraphtotxt(A_t, "graph100.txt")

    l = len(sumin)
    x = np.arange(1,l+1)
    f, axarr = plt.subplots(1, 3)
    axarr[0].imshow(A_t)
    axarr[1].bar(x, sumin)
    axarr[2].bar(x, sumout)
    plt.show()

   # communities, frames = louvain_method(A_t)
    # draw_communities(A_t, communities)