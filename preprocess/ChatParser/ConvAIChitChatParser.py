import os
from uti.utility import write_to_csv_file
from uti.utility import read_json
from uti.utility import read_csv_todf


class BSTParser:
    def __init__(self, file):
        self.file = file
        self.folder = "ConvAIChitChat"
        self.source_dir = "/home/xucan/PycharmProjects/Parsing_Telegram_Chat_History/data/Chat/"+self.folder+"/" + self.file  # source file from chitchat
        self.synthesizer_folder = os.path.join("/home/xucan/PycharmProjects/Parsing_Telegram_Chat_History/data/synthesizer_data/",self.folder)
        self.output_file_csv = os.path.join( self.synthesizer_folder, "train.csv")
        self.train_csv = os.path.join(self.synthesizer_folder, "train_bert.csv")
        self.have_text = True

    def parse(self):
        if  os.path.exists(self.output_file_csv):
            os.remove(self.output_file_csv)


        csv_columns = ['sequenceID','text']
        data = read_json(self.source_dir)
        all_messages = [csv_columns]
        sequenceID = 1

        for chat in data:

            dialog = chat["thread"]
            if dialog!=None:
                for chitchat in dialog:
                    all_messages.append([sequenceID,chitchat["text"]] )
            sequenceID+=1

        write_to_csv_file(self.output_file_csv, all_messages)


    def create_train_for_bert(self):

        if os.path.exists(self.train_csv):
            os.remove(self.train_csv)
        first_sequenceID=0
        first_text=""
        csv_columns = ['label', 'sentence1','sentence2']

        allcon=[csv_columns]
        df = read_csv_todf(self.output_file_csv)
        for index, row in df.iterrows():
            second_sequenceID=row["sequenceID"]
            second_text = row["text"]
            if first_sequenceID!=0:
                if second_sequenceID == first_sequenceID:
                    allcon.append([1,first_text,second_text])
                    if len(allcon) >= 50:
                        earlyfirsttext = allcon[-50][1]
                        allcon.append([0,earlyfirsttext,second_text])

                else:
                    allcon.append([0,first_text,second_text])

            first_sequenceID = second_sequenceID
            first_text = second_text
        write_to_csv_file(self.train_csv, allcon)






# The main function, the entry point
if __name__ == '__main__':
    a_parser = BSTParser("train.json")
    a_parser.create_train_for_bert()