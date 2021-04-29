from bs4 import BeautifulSoup
import os
from uti.utility import update_message_id
from uti.utility import write_to_csv_file
from uti.utility import write_to_json_file
from uti.utility import deEmojify



class DialogueParser:
    def __init__(self, folder, save_as_csv=True):
        self.folder = folder  # folder we need to parser
        self.source_dir = os.path.join("/home/xucan/Downloads/Telegram Desktop",
                                       self.folder)  # source file folder from telegram
        self.output_file_json = os.path.join(self.source_dir, "Dialogue",
                                             self.folder.lower() + ".json")  # output1: parsed result saved as .json
        self.output_file_csv = os.path.join(self.source_dir, "Dialogue",
                                            self.folder.lower() + ".csv")  # output1: parsed result saved as .csv
        self.save_as_csv = save_as_csv  # save as CSV or json
        self.sequence_range = 1

    def parse(self):
        if not os.path.exists(os.path.join(self.source_dir, "Dialogue")):
            os.makedirs(os.path.join(self.source_dir, "Dialogue"))
        if self.save_as_csv and os.path.exists(self.output_file_csv):
            os.remove(self.output_file_csv)
        if not self.save_as_csv and os.path.exists(self.output_file_json):
            os.remove(self.output_file_json)

        csv_columns = ['label', 'sentence1', 'sentence2']

        files = os.listdir(self.source_dir)
        files.sort()
        all_messages = [csv_columns]
        label = 1
        for file in files:
            if file[-4:] == "html":
                file_path = self.source_dir + "/" + file
                a_chat_page = open(file_path, encoding='utf-8')
                a_beautiful_soup = BeautifulSoup(a_chat_page, features="html.parser")
                a_chat_page.close()
                history = a_beautiful_soup.find('div', {"class": "history"})
                divs = history.find_all('div', class_="reply_to details")
                for div in divs:
                    sentence1 = ""
                    sentence2 = ""
                    sentence2_div = div.find_next("div")
                    if sentence2_div["class"] != ["text"]:
                        continue
                    sentence2 = sentence2_div.text.strip()
                    sentence2 = deEmojify(sentence2)
                    go_to_message = div.find("a")['href']
                    message_id = go_to_message[7:]
                    reply_to_message_div = a_beautiful_soup.find('div', {"class": "message default clearfix",
                                                                         "id": message_id})
                    if reply_to_message_div is None:
                        reply_to_message_div = a_beautiful_soup.find('div', {"class": "message default clearfix joined",
                                                                             "id": message_id})
                    if reply_to_message_div is None:
                        continue
                    body_div = reply_to_message_div.find('div', class_="body")
                    if body_div is None:
                        continue
                    sentence1_div = body_div.find('div', class_="text")
                    if sentence1_div is None:
                        continue
                    sentence1 = sentence1_div.text.strip()
                    sentence1 = deEmojify(sentence1)

                    if sentence1 == "" or sentence2 == "":
                        continue

                    a_new_message = {"label": label, "sentence1": sentence1, "sentence2": sentence2}
                    all_messages.append([label, sentence1, sentence2])

                    if not self.save_as_csv:
                        write_to_json_file(self.output_file_json, a_new_message)

        if self.save_as_csv:
            write_to_csv_file(self.output_file_csv, all_messages)


class NegDialogueParser:
    def __init__(self, folder, save_as_csv=True):
        self.folder = folder  # folder we need to parser
        self.source_dir = os.path.join("/home/xucan/Downloads/Telegram Desktop",
                                       self.folder)  # source file folder from telegram
        self.output_file_json = os.path.join(self.source_dir, "Dialogue", "neg" + self.folder.lower() + ".json")
        self.output_file_csv = os.path.join(self.source_dir, "Dialogue", "neg" + self.folder.lower() + ".csv")
        self.save_as_csv = save_as_csv

    def parse(self):
        if not os.path.exists(os.path.join(self.source_dir, "Dialogue")):
            os.makedirs(os.path.join(self.source_dir, "Dialogue"))
        if self.save_as_csv and os.path.exists(self.output_file_csv):
            os.remove(self.output_file_csv)
        if not self.save_as_csv and os.path.exists(self.output_file_json):
            os.remove(self.output_file_json)

        csv_columns = ['label', 'sentence1', 'sentence2']

        files = os.listdir(self.source_dir)
        files.sort()
        all_messages = [csv_columns]
        label = 0
        for file in files:
            if file[-4:] == "html":
                file_path = self.source_dir + "/" + file
                a_chat_page = open(file_path, encoding='utf-8')
                a_beautiful_soup = BeautifulSoup(a_chat_page, features="html.parser")
                a_chat_page.close()
                history = a_beautiful_soup.find('div', {"class": "history"})
                divs = history.find_all('div', class_="reply_to details")
                for div in divs:
                    sentence1 = ""
                    sentence2 = ""
                    sentence2_div = div.find_next("div")
                    if sentence2_div["class"] != ["text"]:
                        continue
                    sentence2 = sentence2_div.text.strip()
                    sentence2 = deEmojify(sentence2)
                    go_to_message = div.find("a")['href']
                    if go_to_message[0] != "#":
                        continue
                    message_id = go_to_message[7:]
                    message_id = update_message_id(message_id)
                    reply_to_message_div = a_beautiful_soup.find('div', {"class": "message default clearfix",
                                                                         "id": message_id})
                    if reply_to_message_div is None:
                        reply_to_message_div = a_beautiful_soup.find('div', {"class": "message default clearfix joined",
                                                                             "id": message_id})
                    if reply_to_message_div is None:
                        continue
                    body_div = reply_to_message_div.find('div', class_="body")
                    if body_div is None:
                        continue
                    sentence1_div = body_div.find('div', class_="text")
                    if sentence1_div is None:
                        continue
                    sentence1 = sentence1_div.text.strip()

                    sentence1 = deEmojify(sentence1)

                    if sentence1 == "" or sentence2 == "":
                        continue

                    a_new_message = {"label": label, "sentence1": sentence1, "sentence2": sentence2}
                    all_messages.append([label, sentence1, sentence2])

                    if not self.save_as_csv:
                        write_to_json_file(self.output_file_json, a_new_message)

        if self.save_as_csv:
            write_to_csv_file(self.output_file_csv, all_messages)


# The main function, the entry point
if __name__ == '__main__':
    a_parser = DialogueParser("Crypto", True)
    a_parser.parse()
