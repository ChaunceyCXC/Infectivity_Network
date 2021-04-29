import pandas as pd
from datetime import datetime
import json
from uti import utility


def read_dialogue_sequence(file, sequence_id):
    df = utility.read_csv_todf(file)
    sequence_df = df[df.sequenceID == sequence_id]
    return sequence_df

def read_reply_embedding(file):
    with open(file) as f:
        data = json.load(f)
        return data

def get_time_sequence(sequence_df):
     date_sequence = sequence_df["date"].tolist()
     time_sequence = [0]
     first_datetime = datetime.strptime(date_sequence[0], '%d.%m.%Y %H:%M:%S')
     for i in range(1, len(date_sequence)):
         ith_datetime = datetime.strptime(date_sequence[i], '%d.%m.%Y %H:%M:%S')
         diff = (ith_datetime-first_datetime).total_seconds()
         time_sequence.append(diff)
     return time_sequence

def get_user_sequence(sequence_df):
    username_sequence = sequence_df["username"].tolist()
    user_sequence= []
    dict = {}
    index = 0
    for username in username_sequence:
        if username not in dict.keys():
            dict[username] = index
            index += 1
        user_sequence.append(dict[username])

    return user_sequence


def save_user_dict(sequence_df):
    username_sequence = sequence_df["username"].tolist()
    dict = {}
    index = 0
    for username in username_sequence:
        if username not in dict.keys():
            dict[username] = index
            index += 1
    utility.write_to_json_file("dict.json", dict)


if __name__ == '__main__':
    filepath = "/home/xucan/Downloads/Telegram Desktop/Credit/Chat/chat.csv"
    sequencedf = read_dialogue_sequence(filepath, 1)
    save_user_dict(sequencedf)
