from datetime import datetime
import matplotlib.pyplot as plt
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
    translated_data = translate_data(modified_data)
    # plot_data(modified_data)

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
    print("Modifying retrosheet data ->")

    print("Removing unneeded columns...")
    modified_data = loaded_data.drop(COLUMNS_TO_DROP, axis='columns')
    # __print_data_info(modified_data)

    print("Adding last seen data...")
    modified_data['last_date_seen'] = (
        modified_data.sort_values(['batter', 'pitcher', 'date'])
                        .groupby(['batter', 'pitcher'])
                        ['date'].shift(1)
    )

    # Udpate all NaN to -1
    modified_data = modified_data.fillna(-1)

    # Add days since last seen
    modified_data['days_since_last_seen'] = modified_data.apply(__get_days_between_games, axis=1)

    # Filter to only show data we care about
    # modified_data = modified_data[['batter', 'pitcher', 'gid', 'last_date_seen', 'days_since_last_seen']]

    print(modified_data[modified_data['days_since_last_seen'] < -1])

    # __print_data_info(modified_data[modified_data['days_since_last_seen'] == 20])

    return modified_data


def translate_data(modified_data):
    data_by_days_since = modified_data.groupby('days_since_last_seen')[
                    [
                        'pa',
                        'ab',
                        'single',
                        'double',
                        'triple',
                        'hr'
                    ]].sum().sort_values('days_since_last_seen', ascending=True)

    __print_data_info(data_by_days_since)

    return data_by_days_since


def plot_data(modified_data):
    modified_data[modified_data["days_since_last_seen"] > 0].hist(bins=3)
    plt.xlabel("Days Since Last Seen")
    plt.ylabel("Count")
    plt.title("Distribution of 'Days Since Last Seen'")
    plt.show()

def __get_days_between_games(row):
    first_game = str(row['last_date_seen']).split('.')[0]
    second_game = str(row['date']).split('.')[0]

    if first_game == "-1":
        return -1

    first_game = datetime.strptime(first_game, "%Y%m%d").date()
    second_game = datetime.strptime(second_game, "%Y%m%d").date()

    return (second_game - first_game).days

def __print_data_info(df):
    print(df.shape)
    print(df.columns)
    print(df.head(20))