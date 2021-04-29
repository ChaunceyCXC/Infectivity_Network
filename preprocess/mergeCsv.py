import os
import glob
import pandas as pd
from preprocess import dialogueParser as dp


class CsvMerger:
    def __init__(self, dir_path, combined_csv_filename):
        self.dir_path = dir_path
        self.combined_csv_filename = combined_csv_filename

    def merge(self):
        os.chdir(self.dir_path)
        if os.path.exists(self.combined_csv_filename):
            os.remove(self.combined_csv_filename)
        extension = 'csv'
        all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
        combined_csv.to_csv(self.combined_csv_filename, index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    folder = "Crypto"
    save_as_csv = True
    p_parser = dp.DialogueParser(folder, save_as_csv)
    p_parser.parse()
    n_parser = dp.NegDialogueParser(folder, save_as_csv)
    n_parser.parse()

    a_merger = CsvMerger("/home/xucan/Downloads/Telegram Desktop/" + folder + "/Dialogue", "train.csv")
    a_merger.merge()
