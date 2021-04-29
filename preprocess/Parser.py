from bs4 import BeautifulSoup
import os
import datetime
from uti.utility import write_to_csv_file
from uti.utility import write_to_json_file
from uti.utility import deEmojify
import string


class TelegramParser:
    def __init__(self, folder, save_as_csv=True):
        self.folder = folder
        self.source_dir = "/home/xucan/Downloads/Telegram Desktop/" + self.folder  # source file folder from telegram
        self.output_file_json = os.path.join(self.source_dir, "Chat/chat.json")  # output1: parsed result
        self.output_file_csv = os.path.join(self.source_dir, "Chat/chat.csv")
        self.dic_file_path = os.path.join(self.source_dir, "Chat/dict.json")  # outout2: usernmae to number dictionary
        self.have_text = True
        self.remove_deleted_account = True
        self.remove_consequent = False
        self.last_username = ""
        self.save_as_csv = save_as_csv
        self.sequence_range = 1

    def parse(self):
        if self.save_as_csv and os.path.exists(self.output_file_csv):
            os.remove(self.output_file_csv)
        if not self.save_as_csv and os.path.exists(self.output_file_json):
            os.remove(self.output_file_json)
        if os.path.exists(self.dic_file_path):
            os.remove(self.dic_file_path)
        csv_columns = []
        if self.have_text:
            csv_columns = ['sequenceID', 'date', 'username', 'text']
        else:
            csv_columns = ['sequenceID', 'date', 'username']
        files = os.listdir(self.source_dir)
        files.sort()
        dict = {}
        all_messages = [csv_columns]
        index = 0
        sequenceID = 0
        lastDate = "01.01.2000 00:00:00"
        for file in files:
            if file[-4:] == "html":
                file_path = self.source_dir + "/" + file
                a_products_desc_page = open(file_path, encoding='utf-8')
                a_beautiful_soup = BeautifulSoup(a_products_desc_page, features="html.parser")
                a_products_desc_page.close()
                history = a_beautiful_soup.find('div', {"class": "history"})
                divs = history.find_all('div', class_="body")
                for div in divs:
                    if div["class"] == ['body']:
                        date_div = div.find("div", class_="pull_right date details")
                        name_div = div.find("div", class_="from_name")
                        text_div = div.find("div", class_="text")
                        if date_div is not None:
                            date = date_div["title"]
                            y_date = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                            x_date = datetime.datetime.strptime(lastDate, '%d.%m.%Y %H:%M:%S')
                            diff = y_date - x_date
                            days, seconds = diff.days, diff.seconds
                            diff_hours = days * 24 + seconds / 3600
                            if diff_hours > self.sequence_range:
                                sequenceID = sequenceID + 1
                            lastDate = date

                        else:
                            continue
                        if name_div is not None:
                            username = name_div.text.strip()
                            if username == "Deleted Account":
                                if self.remove_deleted_account:
                                    continue
                        else:
                            continue
                        if text_div is not None:
                            text = text_div.text.strip()
                        else:
                            text = "NOT TEXT"
                        if self.remove_consequent:
                            if username == self.last_username:
                                continue
                        text = deEmojify(text)
                        if self.have_text:
                            if text != "NOT TEXT" and text != "":
                                if username != self.last_username:
                                    a_new_message = {"sequenceID": sequenceID, "date": date, "username": username, "text": text}
                                    all_messages.append([sequenceID, date, username, text])
                                else :
                                    last_message = all_messages.pop()
                                    the_text = last_message[3]
                                    if the_text[-1] in string.punctuation:
                                        last_message[3] = the_text + " " + text
                                    else:
                                        last_message[3] = the_text + ". " + text
                                    all_messages.append(last_message)


                        else:
                            a_new_message = {"sequenceID": sequenceID, "date": date, "username": username}
                            all_messages.append([sequenceID, date, username])
                        if not self.save_as_csv:
                            write_to_json_file(self.output_file_json, a_new_message)
                        self.last_username = username
                        if username not in dict.keys():
                            dict[username] = index
                            index = index + 1
        if self.save_as_csv:
            write_to_csv_file(self.output_file_csv, all_messages)

        write_to_json_file(self.dic_file_path, dict)


# The main function, the entry point
if __name__ == '__main__':
    a_parser = TelegramParser("Credit")
    a_parser.parse()
