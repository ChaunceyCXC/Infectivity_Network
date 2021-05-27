import pandas as pd
from datetime import datetime
import json
from uti import utility
from data import dataOperation


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


def get_user_sequence_from_dict(sequence_df, dict):
    username_sequence = sequence_df["username"].tolist()
    user_sequence = []
    for username in username_sequence:
        user_sequence.append(dict[username])
    return user_sequence


def save_user_dict(sequence_df, dict_name):
    username_sequence = sequence_df["username"].tolist()
    dict = {}
    index = 0
    for username in username_sequence:
        if username not in dict.keys():
            dict[username] = index
            index += 1
    utility.write_to_json_file(dict_name, dict)


def save_user_dict_multiple(filepath, start_id, end_id, dict_name):
    df = utility.read_csv_todf(filepath)
    index = 0
    dict = {}
    for i in range(start_id, end_id+1):
        sequence_df = df[df.sequenceID == i]
        username_sequence = sequence_df["username"].tolist()
        for username in username_sequence:
            if username not in dict.keys():
                dict[username] = index
                index += 1
    utility.write_to_json_file(dict_name, dict)

def get_user_dict_multiple(filepath, start_id, end_id):
    df = utility.read_csv_todf(filepath)
    index = 0
    dict = {}
    for i in range(start_id, end_id+1):
        sequence_df = df[df.sequenceID == i]
        username_sequence = sequence_df["username"].tolist()
        for username in username_sequence:
            if username not in dict.keys():
                dict[username] = index
                index += 1
    return dict


if __name__ == '__main__':
    filepath = "/home/xucan/Downloads/Telegram Desktop/Credit/Chat/chat.csv"
    save_user_dict_multiple(filepath, 1, 1000, "user/dict_1000.json")

