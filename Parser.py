import json
from bs4 import BeautifulSoup
import os
import csv


def write_to_json_file(file_path, data):
    with open(file_path, 'a',encoding='utf-8') as fp:
        json.dump(data, fp)
        fp.write("\n")


def write_to_csv_file(file_path, data):
    with open(file_path, "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)


class parser:
    def __init__(self):
        self.source_dir = "C:/Users/leoac/Desktop/ChatExport_29_05_2020"  # source file folder from telegram
        self.output_file_json = "C:/Users/leoac/Desktop/ChatExportFilter_29_05_2020.json"  # output1: parsed result
        self.output_file_csv = "C:/Users/leoac/Desktop/ChatExportFilter_29_05_2020.csv"
        self.dic_file_path = "C:/Users/leoac/Desktop/dict.json"  # outout2: usernmae to number dictionary
        self.have_text = False
        self.remove_deleted_account = True
        self.remove_consequent = True
        self.last_username = ""
        self.save_as_csv = True

    def parse(self):
        csv_columns = []
        if self.have_text:
            csv_columns = ['date', 'username', 'text']
        else:
            csv_columns = ['date', 'username']
        files = os.listdir(self.source_dir)
        files.sort()
        dict = {}
        all_messages = [csv_columns]
        index = 0
        for file in files:
            if file[-4:] == "html":
                file_path = self.source_dir + "/" + file
                a_products_desc_page = open(file_path, encoding='utf-8')
                a_beautiful_soup = BeautifulSoup(a_products_desc_page, features="html.parser")
                a_products_desc_page.close()
                history = a_beautiful_soup.find('div', {"class": "history"})
                divs = history.find_all('div', class_="body")
                date = ""
                username = ""
                text = ""
                for div in divs:
                    if div["class"] == ['body']:
                        date_div = div.find("div", class_="pull_right date details")
                        name_div = div.find("div", class_="from_name")
                        text_div = div.find("div", class_="text")
                        if date_div is not None:
                            date = date_div["title"]
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
                        if self.have_text:
                            a_new_message = {"date": date, "username": username, "text": text}
                            all_messages.append([date, username, text])
                        else:
                            a_new_message = {"date": date, "username": username}
                            all_messages.append([date, username])
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
    a_parser = parser()
    a_parser.parse()
