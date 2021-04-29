import json
import os
import numpy as np
import datetime


class influence_graph:
    def __init__(self):
        self.source_file = "C:/Users/leoac/Desktop/groupChat/ChatExportFilter_29_05_2020.json"
        self.dic_file_path = "C:/Users/leoac/Desktop/groupChat/dict.json"
        self.saved_influence_matrix = "C:/Users/leoac/Desktop/groupChat/influenceMatrix.npy"
        self.session_range = 1

    def get_influence_matrix(self):
        with open(self.dic_file_path) as f:
            dic = json.load(f)
        size = len(dic)
        reply_counts = np.zeros((size, size))
        involved_sessions = np.zeros((size, size))
        new_session = np.ones((size, size))
        total_reply = 0
        total_session = 1
        a_post = {}
        lines = open(self.source_file, "r")
        for line in lines:
            if total_reply == 0:
                a_post = json.loads(line)
                total_reply = total_reply + 1
                continue
            else:
                consequent_post = json.loads(line)

                x_date = datetime.datetime.strptime(a_post["date"], '%d.%m.%Y %H:%M:%S')
                y_date = datetime.datetime.strptime(consequent_post["date"], '%d.%m.%Y %H:%M:%S')
                diff = y_date - x_date
                days, seconds = diff.days, diff.seconds
                diff_hours = days * 24 + seconds / 3600
                if diff_hours > self.session_range:
                    new_session[new_session == 0] = 1
                    total_session = total_session + 1
                else:
                    x = dic[a_post["username"]]
                    y = dic[consequent_post["username"]]
                    reply_counts[x, y] = reply_counts[x, y] + 1
                    total_reply = total_reply + 1

                    if new_session[x, y] == 1:
                        involved_sessions[x, y] = involved_sessions[x, y] + 1
                        new_session[x, y] == 0

                a_post = consequent_post
        involved_sessions[involved_sessions == 0] = 1
        influence_matrix = (reply_counts / total_reply) / (np.log(total_session / involved_sessions + 1) + 1)
        influence_matrix = influence_matrix/np.max(influence_matrix)
        i, j = np.unravel_index(influence_matrix.argmax(), influence_matrix.shape)
        np.save(self.saved_influence_matrix, influence_matrix)


if __name__ == '__main__':
    a_influence_graph = influence_graph()
    a_influence_graph.get_influence_matrix()
