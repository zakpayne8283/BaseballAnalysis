import os
import pandas as pd
import sys

CSV_ROOT = 'data/'

class Season:
    
    # Config values
    year_id = None
    csv_path = None

    # Stored data
    csv_data_raw = None

    def __init__(self, year, skip_setup=False):
        self.year_id = year
        self.csv_path = os.path.join(CSV_ROOT, f"{year}plays.csv")

        if skip_setup is False:
            # Load the CSV file
            self.__load_csv_data()

    def __load_csv_data(self):
        print(f"Loading CSV data for {self.year_id} season...")

        try:
            self.csv_data_raw = pd.read_csv(self.csv_path)
            print(f"Successfully loaded {self.csv_path}!")
        except FileNotFoundError as e:
            print(f"An error occurred while loading {self.csv_path}!")
            print(e)
            sys.exit()