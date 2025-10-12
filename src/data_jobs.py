from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
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

available_data = {}

def run():
    available_data['loaded_data'] = load_retrosheet_data()
    available_data['days_since_last_seen_raw'] = add_days_since_last_seen(available_data['loaded_data'])
    available_data['days_since_last_seen'] = add_stats_to_data(available_data['days_since_last_seen_raw'], groupby='days_since_last_seen')
    available_data['times_seen_data_raw'] = add_times_seen_this_season(available_data['loaded_data'])
    available_data['times_seen_data'] = add_stats_to_data(available_data['times_seen_data_raw'], groupby='times_seen')

    # __print_data_info(available_data['times_seen_data'])

    plot_data(available_data)

def load_retrosheet_data():
    print("Loading retrosheet data...")

    # TODO: Actually handle multiple input files...

    for csv in CSV_FILES:
        file_path = os.path.join(CSV_ROOT, csv)

        try:
            loaded_data = pd.read_csv(file_path)
            print(f"Successfully loaded {file_path}!")

            # TODO: Put this somewhere better
            print("Removing unneeded columns...")
            loaded_data = loaded_data.drop(COLUMNS_TO_DROP, axis='columns')

            return loaded_data
        except Exception as e:
            print(f"An error occurred while loading {file_path}!")
            print(e)
            sys.exit()

def add_days_since_last_seen(loaded_data):
    print("Modifying retrosheet data ->")

    output_data = loaded_data.copy(deep=True)

    print("Adding days since last seen data...")
    output_data['last_date_seen'] = (
        output_data.sort_values(['batter', 'pitcher', 'date'])
                        .groupby(['batter', 'pitcher'])
                        ['date'].shift(1)
    )

    # Udpate all NaN to -1
    output_data = output_data.fillna(-1)

    # Add days since last seen
    output_data['days_since_last_seen'] = output_data.apply(__get_days_between_games, axis=1)

    return output_data

def add_times_seen_this_season(loaded_data):
    print("Modifying retrosheet data ->")
    
    output_data = loaded_data.copy(deep=True)

    print("Adding # times seen that season...")
    output_data['times_seen'] = output_data.sort_values(['batter', 'pitcher', 'date']).groupby(['batter', 'pitcher']).cumcount()

    return output_data

def plot_data(dataframes):

    days_seen_data = dataframes['days_since_last_seen']

    days_seen_data.plot(x="days_since_last_seen", y=["avg", "obp", "slg", "ops"], kind="line")
    plt.title("Rate Stats by Days Since Last Seen")
    plt.xlabel("Days Since")
    plt.ylabel("Rate")
    plt.legend(title="Players")

    ######################

    times_seen = dataframes['times_seen_data']

    # Need to aggregate all times_seen >12
    times_seen["times_seen_grouped"] = np.where(times_seen["times_seen"] > 12, "13+", times_seen["times_seen"].astype(str))

    times_seen = (
        times_seen.groupby("times_seen_grouped", as_index=False)
        .agg({"ab": "sum"})
        .sort_values("times_seen_grouped", key=lambda x: x.replace({"13+": 13}).astype(int))
    )

    times_seen.plot(x="times_seen", y=["avg", "obp", "slg", "ops"], kind="line")
    plt.title("Rate Stats by Times Seen this Season")
    plt.xlabel("Times Seen")
    plt.ylabel("Rate")
    plt.legend(title="Players")

    ######################

    plt.show()
    
def __get_days_between_games(row):
    first_game = str(row['last_date_seen']).split('.')[0]
    second_game = str(row['date']).split('.')[0]

    if first_game == "-1":
        return -1

    first_game = datetime.strptime(first_game, "%Y%m%d").date()
    second_game = datetime.strptime(second_game, "%Y%m%d").date()

    return (second_game - first_game).days
