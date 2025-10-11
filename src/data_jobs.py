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
    plot_data(translated_data)

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

    # print(modified_data[modified_data['days_since_last_seen'] < -1])

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
                        'hr',
                        'sh',
                        'sf',
                        'hbp',
                        'walk',
                        'iw',
                        'k',
                        'xi',
                        'rbi_b',
                        'rbi1',
                        'rbi2',
                        'rbi3'
                    ]].sum().sort_values('days_since_last_seen', ascending=True)

    # Collapse some stats
    print("Calculating stats...")
    # Just hits
    data_by_days_since['h'] = data_by_days_since['single'] + data_by_days_since['double'] + data_by_days_since['triple'] + data_by_days_since['hr']
    # Just RBIs
    data_by_days_since['rbi'] = data_by_days_since['rbi_b'] + data_by_days_since['rbi1'] + data_by_days_since['rbi2'] + data_by_days_since['rbi3']
    # AVG
    data_by_days_since['avg'] = data_by_days_since.apply(__calc_average, axis=1)
    # OBP
    data_by_days_since['obp'] = data_by_days_since.apply(__calc_onbase, axis=1)
    # SLG
    data_by_days_since['slg'] = data_by_days_since.apply(__calc_slugging, axis=1)
    # OPS
    data_by_days_since['ops'] = data_by_days_since['obp'] + data_by_days_since['slg']

    data_by_days_since = data_by_days_since.drop(['single', 'rbi_b', 'rbi1', 'rbi2', 'rbi3'], axis='columns')

    __print_data_info(data_by_days_since)

    return data_by_days_since.reset_index()


def plot_data(dataframe):
    dataframe.plot(x="days_since_last_seen", y=["avg", "obp", "slg", "ops"], kind="line")
    plt.title("Rate Stats by Days Since Last Seen")
    plt.xlabel("Days Since")
    plt.ylabel("Rate")
    plt.legend(title="Players")
    plt.show()
    
    # modified_data[modified_data["days_since_last_seen"] > 0].hist(bins=3)
    # plt.xlabel("Days Since Last Seen")
    # plt.ylabel("Count")
    # plt.title("Distribution of 'Days Since Last Seen'")
    # plt.show()

def __get_days_between_games(row):
    first_game = str(row['last_date_seen']).split('.')[0]
    second_game = str(row['date']).split('.')[0]

    if first_game == "-1":
        return -1

    first_game = datetime.strptime(first_game, "%Y%m%d").date()
    second_game = datetime.strptime(second_game, "%Y%m%d").date()

    return (second_game - first_game).days

def __calc_average(row):
    return round(row['h'] / row['ab'], 3)

def __calc_onbase(row):
    # OBP = (Hits + Walks + Hit by Pitch) ÷ (At Bats + Walks + Hit by Pitch + Sacrifice Flies)
    return round((row['h'] + row['walk'] + row['hbp']) / (row['ab'] + row['walk'] + row['hbp'] + row['sf']), 3)

def __calc_slugging(row):
    # SLG = (Singles + (2 × Doubles) + (3 × Triples) + (4 × Home Runs)) ÷ At Bats
    return round((row['single'] + (2 * row['double']) + (3 * row['triple']) + (4 * row['hr'])) / row['ab'], 3)

def __print_data_info(df):
    print(df.shape)
    print(df.columns)
    print(df.head(20))