import os

import numpy as np
from analysis.simulation import Simulator
from data import dataOperation
from data.dataOperation import combineTopicChat
from uti.utility import write_to_json_file, read_csv_todf, write_to_csv_file, create_fix_random_matrix


class Synthesizer:
    def __init__(self,  text_source, output_tu_json, output_synthesized_text_s, sequence_max):
        self.sequence_max = sequence_max
        self.output_tu_json = output_tu_json
        self.text_source = text_source
        self.output_synthesized_text_s = output_synthesized_text_s
    def synthesize(self, A):
        if  os.path.exists(self.output_tu_json):
            os.remove(self.output_tu_json)
        if  os.path.exists(self.output_synthesized_text_s):
            os.remove(self.output_synthesized_text_s)
        chatSequence = []
        sequence_ID = 1
        csv_columns = ['sequenceID','text']
        all_messages = [csv_columns]
        df = read_csv_todf(self.text_source)
        index = 1
        for i in range(10000):
            simulator1 = Simulator(A, D, 0)
            simulator2 = Simulator(A, D, 2)
            simulator1.simulation()
            if len(simulator1.time_sequence) < 7 or len(simulator1.time_sequence)>12:
                continue
            simulator2.simulation()
            if len(simulator2.time_sequence) < 7 or len(simulator2.time_sequence)>12:
                continue
            result, l1, l2 = combineTopicChat(simulator1, simulator2)
            group_sequence = result["group_sequence"]

            sequence1 = df[df.sequenceID ==index]
            index+=1
            indexlist = sequence1.index
            count = len(indexlist)
            while l1 > count:
                sequence1 = df[df.sequenceID == index]
                indexlist = sequence1.index
                count = len(indexlist)
                index+=1
            sequence2 = df[df.sequenceID == index]
            indexlist = sequence2.index
            count = len(indexlist)
            while l2 > count:
                sequence2 = df[df.sequenceID == index]
                indexlist = sequence2.index
                count = len(indexlist)
                index += 1

            textlist1 = sequence1.text.to_list()
            textlist2 = sequence2.text.to_list()
            p1=p2=0
            for group_id in group_sequence:
                if group_id == 0:
                    all_messages.append([sequence_ID, textlist1[p1]])
                    p1+=1
                else :
                    all_messages.append([sequence_ID, textlist2[p2]])
                    p2+=1
            chatSequence.append(result)
            sequence_ID+=1
            if sequence_ID == self.sequence_max:
                break

        write_to_csv_file(self.output_synthesized_text_s, all_messages)
        write_to_json_file(self.output_tu_json, chatSequence)

    def synthesize_random(self, A):
        if  os.path.exists(self.output_tu_json):
            os.remove(self.output_tu_json)
        if  os.path.exists(self.output_synthesized_text_s):
            os.remove(self.output_synthesized_text_s)
        chatSequence = []
        sequence_ID = 1
        csv_columns = ['sequenceID','text']
        all_messages = [csv_columns]
        df = read_csv_todf(self.text_source)
        index = 1
        for i in range(10000):
            simulator1 = Simulator(A, D, 0)
            simulator1.simulation()
            if len(simulator1.time_sequence) < 7 or len(simulator1.time_sequence)> 12:
                continue

            l1 = len(simulator1.time_sequence)
            group_sequence = simulator1.group_sequence

            sequence1 = df[df.sequenceID ==index]
            index+=1
            indexlist = sequence1.index
            count = len(indexlist)
            while l1 > count:
                sequence1 = df[df.sequenceID == index]
                indexlist = sequence1.index
                count = len(indexlist)
                index+=1


            textlist1 = sequence1.text.to_list()

            p1=0
            for group_id in group_sequence:
                all_messages.append([sequence_ID, textlist1[p1]])
                p1+=1

            chatSequence.append({"time_sequence":simulator1.time_sequence, "user_sequence":simulator1.user_sequence})
            sequence_ID+=1
            if sequence_ID == self.sequence_max:
                break

        write_to_csv_file(self.output_synthesized_text_s, all_messages)
        write_to_json_file(self.output_tu_json, chatSequence)



if __name__ == '__main__':
    D = 4
    A = create_fix_random_matrix(D)
    np.fill_diagonal(A, 0)
    '''
        A[0, 1] = 0.9
        A[0, 2] = 0.01
        A[0, 3] = 0.01
        A[1, 0] = 0.9
        A[1, 2] = 0.01
        A[1, 3] = 0.01
        A[2, 0] = 0.01
        A[2, 1] = 0.01
        A[2, 3] = 0.9
        A[3, 0] = 0.01
        A[3, 1] = 0.01
        A[3, 2] = 0.9
                          '''
    folder = "/home/chauncey/PycharmProjects/Parsing_Telegram_Chat_History/data/synthesizer_data/blended_skill_talk/"
    source_file = os.path.join(folder, "test.csv" )
    output_tu_json =os.path.join(folder, "/tu_sequence.json" )
    output_synthesized_text_s = os.path.join(folder, "/text_sequence.csv")
    synthesizer =Synthesizer(source_file,output_tu_json,output_synthesized_text_s,201)
    synthesizer.synthesize(A)