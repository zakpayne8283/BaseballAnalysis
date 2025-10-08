import os
import pandas as pd
import sys

# CSV File Information
CSV_ROOT = 'data/'
CSV_FILES = ['2024plays.csv']

# COLUMN INFORMATION
COLUMNS_TO_DROP = ['f2',
                   'f3',
                   'f4',
                   'f5',
                   'f6', 
                   'f7',
                   'f8',
                   'f9',
                   'bat_f',
                   'po1',
                   'po2',
                   'po3',
                   'po4',
                   'po5',
                   'po6',
                   'po7',
                   'po8',
                   'po9',
                   'po0',
                   'batout1',
                   'batout2',
                   'batout3',
                   'brout_b',
                   'brout1',
                   'brout2',
                   'brout3',
                   'a1',
                   'a2',
                   'a3',
                   'a4',
                   'a5',
                   'a6',
                   'a7',
                   'a8',
                   'a9',
                   'l1',
                   'l2',
                   'l3',
                   'l4',
                   'l5',
                   'l6',
                   'l7',
                   'l8',
                   'l9',
                   'lf1',
                   'lf2',
                   'lf3',
                   'lf4',
                   'lf5',
                   'lf6',
                   'lf7',
                   'lf8',
                   'lf9',
                   'umphome',
                   'ump1b',
                   'ump2b',
                   'ump3b',
                   'umplf',
                   'umprf',
                   'gametype',
                   'pbp']

def run():
    loaded_data = load_retrosheet_data()
    modified_data = modify_retrosheet_data(loaded_data)

def load_retrosheet_data():
    print("Loading retrosheet data...")

    # TODO: Actually handle multiple input files...

    for csv in CSV_FILES:
        file_path = os.path.join(CSV_ROOT, csv)

        try:
            loaded_data = pd.read_csv(file_path)
            print(f"Successfully loaded {file_path}!")
            return loaded_data
        except Exception as e:
            print(f"An error occurred while loading {file_path}!")
            print(e)
            sys.exit()


def modify_retrosheet_data(loaded_data):
    print("Modifying retrosheet data...")

    print("Removing unneeded columns...")
    modified_data = loaded_data.drop(COLUMNS_TO_DROP, axis='columns')
    __print_data_info(modified_data)


def __print_data_info(df):
    print(df.shape)
    print(df.columns)
    print(df.head())