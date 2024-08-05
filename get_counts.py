# Copyright Lars Quentin, Klara Henrike Frahnert 2024
# License: MIT
import os

from dataclasses import dataclass

CURRENT_DIR_OF_SCRIPT = os.path.dirname(os.path.realpath(__file__))
OUTPUT_CSV = os.path.join(CURRENT_DIR_OF_SCRIPT, "counts.csv")

def find_txt_files(directory):
    ret = []
    for root, dir, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt") and file.startswith("threshold"):
                ret.append(os.path.join(root, file))
    return ret

@dataclass
class CSVEntry:
    count: int
    picture_name: str
    classifier: str


def path_to_csv_entry(path):
    # example path
    # C:\Users\Klara\Documents\data\Dokumente\Studium\Promotion\aktuell\PRO060_48h\PM\AsPc1_total\threshold_PM5_2.txt
    
    # First we want to get the name.
    # It, by definition, always starts with threshold_
    # But we only want the stuff after that
    # and we do not want the extension
    picture_name = path.split(os.path.sep)[-1].split(".")[0][len("threshold_"):]
    
    # Next the classifier
    classifier = path.split(os.path.sep)[-2]

    # lastly the count
    # A file looks like:
    #
    # Slice	Count	Total Area	Average Size	%Area	Mean
    # threshold_DMSO1.tif	10	0.230	0.023	0.076	255
    #
    with open(path, "r") as fp:
        lines = fp.readlines()
    
    # sanity check: is that a correct file
    assert lines[0].strip().startswith("Slice")

    count = int(lines[1].split("\t")[1])

    return CSVEntry(count=count, picture_name=picture_name, classifier=classifier)

def save_as_csv(entries, path):
    with open(path, "w") as fp:
        for entry in entries:
            entry_str = f"\"{entry.picture_name}\",\"{entry.classifier}\",\"{entry.count}\"\n"
            fp.write(entry_str)


ALL_TXT_FILES = find_txt_files(CURRENT_DIR_OF_SCRIPT)
ALL_ENTRIES = []
for file in ALL_TXT_FILES:
    ALL_ENTRIES.append(path_to_csv_entry(file))
save_as_csv(ALL_ENTRIES, OUTPUT_CSV)
print(OUTPUT_CSV)
