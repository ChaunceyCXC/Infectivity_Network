import json
import csv
import re

import numpy as np
import pandas as pd
from math import exp

def write_to_json_file(file_path, data):
    with open(file_path, 'a', encoding='utf-8') as fp:
        json.dump(data, fp)
        fp.write("\n")

def write_to_csv_file(file_path, data):
    with open(file_path, "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def read_csv_todf(file):
    df = pd.read_csv(file)
    return df

def read_json(file):
    with open(file) as f:
        data = json.load(f)
        return data

def update_message_id(message_id):
    message = int(message_id[7:]) - 10
    new_message_id = "message" + str(message)
    return new_message_id

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)
def adjust(A):
    A = A/np.amax(A)
    return A

def g(w,t):
    return w*exp(-w*t)

def integral_g(w,t):
    return 1-exp(-w*t)


def savegraphtotxt(graph, file):
   np.savetxt(file,graph,fmt='%.2f')


if __name__ == '__main__':
    filepath = "/home/xucan/Downloads/Telegram Desktop/Credit/Chat/chat.csv"
    read_csv_sequence(filepath, 1)
