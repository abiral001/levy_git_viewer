from datetime import datetime
import os

from .styles import *

import yaml
import pandas as pd

CONFIG_PATH = os.path.expanduser("~")+"/.levy/"

def log(message, type = "message"):
    if type == "message":
        print(message)
    elif type == "warning":
        print(CBEIGEBG+message+CEND)
    else:
        print(CRED+message+CEND)

def load_config(config_file):
    config_file = CONFIG_PATH+config_file
    try:
        with open(config_file, 'r') as f:
            file_contents = f.read()
            return yaml.full_load(file_contents)
    except:
        log('Config file not found. Please run '+CWHITE+CBOLD+CITALIC+'levi --configure'+CEND+CRED+' before using this logger.', 'error')
        return None

def prompt_question(question, key):
    print(question, end ="")
    value = input()
    print("")
    return key, value

def date_format(format, timestamp = datetime.today()):
    if type(timestamp) == type(1):
        return datetime.utcfromtimestamp(timestamp).strftime(format)
    else:
        return datetime.today().strftime(format)

def process_files(stats, fileToTrack, onlyName = True):
    files = [x.split('.')[0] for x in stats.keys() if x.endswith('.{}'.format(fileToTrack))]
    if onlyName == True:
        send = list()
        for onefile in files:
            if "/" in onefile:
                send.append(onefile.split('/')[1])
                continue
            send.append(onefile)
        return send
    else:
        return files

class Queue:
    def __init__(self):
        self.__data__ = list()
        self.__colname__ = ['CommitID', 'Author', 'FileName', 'Date']

    def get_columns(self):
        return self.__colname__

    def add_row(self, commitid, author, filename, date):
        self.__data__.append((commitid, author, filename, date))

    def export_to_csv(self, filename):
        df = pd.DataFrame(self.__data__, columns = list(self.__colname__))
        df = df.drop_duplicates(subset=['FileName', 'Date'])
        log("Exporting to {}".format(filename))
        df.to_csv(filename, index = False)
