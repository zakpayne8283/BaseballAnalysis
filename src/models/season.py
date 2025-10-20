import os
import pandas as pd
import sys

import utils.formulas as formulas
from models.league_stats import LeagueStats

CSV_ROOT = 'data/'

class Season:
    
    # Config values
    year_id = None
    csv_path = None

    # Stored data
    csv_data_raw = None
    league_stats = LeagueStats()
    hitter_data = None

    def __init__(self, year, skip_setup=False, skip_steps=[]):
        self.year_id = year
        self.csv_path = os.path.join(CSV_ROOT, f"{year}plays.csv")

        if skip_setup is False:
            # Load the CSV file
            self.__load_csv_data()

            # Calculate all league-wide stats
            if 'league' not in skip_steps:
                self.__calc_league_stats()
            
            # Calculate all batter stats
            if 'batter' not in skip_steps:
                self.__calc_batter_stats()

    def print_data(self, dataframe_str):
        
        df = None
        
        if dataframe_str == 'batter':
            df = self.hitter_data
        elif dataframe_str == 'raw':
            df = self.csv_data_raw
        elif dataframe_str == 'league':
            df = self.league_stats.as_dataframe()
        
        print(df.columns)
        print(df.head())

    def __calc_league_stats(self):
        self.league_stats.games = self.csv_data_raw['gid'].nunique()
        self.__calc_run_expectancy_matrix()

    def __calc_batter_stats(self):

        # TODO: Also add a count of unique game IDs for each player,
        # representing # of games played

        self.hitter_data = self.csv_data_raw.copy(deep=True).groupby('batter').agg({
                        'gid': 'nunique',
                        'pa': 'sum',
                        'ab': 'sum',
                        'single': 'sum',
                        'double': 'sum',
                        'triple': 'sum',
                        'hr': 'sum',
                        'sh': 'sum',
                        'sf': 'sum',
                        'hbp': 'sum',
                        'walk': 'sum',
                        'iw': 'sum',
                        'k': 'sum',
                        'rbi_b': 'sum',
                        'rbi1': 'sum',
                        'rbi2': 'sum',
                        'rbi3': 'sum'
                    })
        
        # Rename columns as needed
        self.hitter_data = self.hitter_data.rename(columns={"gid": "g"})

        # Seperate out just hits
        self.hitter_data['h'] = formulas.calc_hits(self.hitter_data)
        # Seperate out just RBIs
        self.hitter_data['rbi'] = formulas.calc_rbis(self.hitter_data)
        
        # Calculate AVG
        self.hitter_data['avg'] = formulas.calc_avg(self.hitter_data)
        # Calculate OBP
        self.hitter_data['obp'] = formulas.calc_onbase(self.hitter_data)
        # Calculate SLG
        self.hitter_data['slg'] = formulas.calc_slugging(self.hitter_data)
        # Add OPS
        self.hitter_data['ops'] = self.hitter_data['obp'] + self.hitter_data['slg']

        # Drop the old columns now
        self.hitter_data = self.hitter_data.drop(['single', 'rbi_b', 'rbi1', 'rbi2', 'rbi3'], axis='columns')

        # Reset the index
        self.hitter_data = self.hitter_data.reset_index()

    def __calc_run_expectancy_matrix(self):
        re_data_needed = self.csv_data_raw.copy(deep=True)[[
            'gid',
            'inning',
            'top_bot',
            'outs_pre',
            'br1_pre',
            'br2_pre',
            'br3_pre',
            'runs'
        ]]

        re_data_needed['inning_runs'] = re_data_needed.groupby([
            'gid', 'inning', 'top_bot', 'outs_pre'
            ])['runs'].transform('sum')

        re_data_needed['br1_pre'] = re_data_needed['br1_pre'].notna().astype(int)
        re_data_needed['br2_pre'] = re_data_needed['br2_pre'].notna().astype(int)
        re_data_needed['br3_pre'] = re_data_needed['br3_pre'].notna().astype(int)

        re_data_needed['base_state'] = (
            re_data_needed['br1_pre'] +
            re_data_needed['br2_pre'] * 2 +
            re_data_needed['br3_pre'] * 4
            )
        
        re_matrix = (
            re_data_needed.groupby(['outs_pre', 'base_state'], as_index=False)
                          .agg(run_expectancy=('inning_runs', 'mean'))
                          .pivot(index='outs_pre', columns='base_state', values='run_expectancy')
        )

        print(re_matrix)

    def __load_csv_data(self):
        print(f"Loading CSV data for {self.year_id} season...")

        try:
            self.csv_data_raw = pd.read_csv(self.csv_path)
            print(f"Successfully loaded {self.csv_path}!")
        except FileNotFoundError as e:
            print(f"An error occurred while loading {self.csv_path}!")
            print(e)
            sys.exit()

