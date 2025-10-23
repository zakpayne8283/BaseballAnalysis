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

    def print_data(self, dataframe_str, head_count=10):
        
        df = None
        
        if dataframe_str == 'batter':
            df = self.hitter_data
        elif dataframe_str == 'raw':
            df = self.csv_data_raw
        elif dataframe_str == 'league':
            df = self.league_stats.as_dataframe()
        
        print(df.columns)
        print(df.head(head_count))

    def __calc_league_stats(self):
        self.league_stats.games = self.csv_data_raw['gid'].nunique()
        self.__calc_aggregate_league_stats()
        self.__calc_run_expectancy_matrix()

    def __calc_batter_stats(self):

        # TODO: Also add a count of unique game IDs for each player,
        # representing # of games played

        # Copy the data from raw
        hitter_data = self.csv_data_raw.copy(deep=True)
        
        # Filter out all events which are
        # Irrelevant to hitter specific data:
        hitter_data = hitter_data[
            # no-pitch (NP) events
            (hitter_data['event'] != 'NP')
        ]

        # Now pull aggregate all data needed
        self.hitter_data = hitter_data.groupby('batter').agg({
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
        
        # Adjust the data as needed
        self.hitter_data = self.__fix_routine_stats(self.hitter_data)
        
        # Reset the index
        self.hitter_data = self.hitter_data.reset_index()

    def __calc_aggregate_league_stats(self):

        # Aggregate all applicable data fields
        league_agg_stats = self.csv_data_raw.copy(deep=True).agg({
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
        
        # Adjust the league stats as needed
        league_agg_stats = self.__fix_routine_stats(league_agg_stats)

        # Add the aggregated stats to the league stats
        self.league_stats.add_aggregate_stats(league_agg_stats)

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

        self.league_stats.run_expectancy_matrix = re_matrix

    def __fix_routine_stats(self, batting_stats):

        # Rename columns as needed
        if type(batting_stats) is pd.Series:
            batting_stats = batting_stats.replace("gid", "g")
        else:
            batting_stats = batting_stats.rename(columns={"gid": "g"})

        # Seperate out just hits
        batting_stats['h'] = formulas.calc_hits(batting_stats)
        # Seperate out just RBIs
        batting_stats['rbi'] = formulas.calc_rbis(batting_stats)
        
        # Calculate AVG
        batting_stats['avg'] = formulas.calc_avg(batting_stats)
        # Calculate OBP
        batting_stats['obp'] = formulas.calc_onbase(batting_stats)
        # Calculate SLG
        batting_stats['slg'] = formulas.calc_slugging(batting_stats)
        # Add OPS
        batting_stats['ops'] = batting_stats['obp'] + batting_stats['slg']

        # Drop the old columns now
        columns_to_drop = [
            'single',
            'rbi_b',
            'rbi1',
            'rbi2',
            'rbi3'
        ]

        if type(batting_stats) is pd.Series:
            batting_stats = batting_stats[~batting_stats.isin(columns_to_drop)]
        else:
            batting_stats = batting_stats.drop(columns_to_drop, axis='columns')
        
        return batting_stats

    def __load_csv_data(self, game_type='regular'):
        print(f"Loading {game_type} games CSV data for {self.year_id} season...")

        try:
            self.csv_data_raw = pd.read_csv(self.csv_path)
            self.csv_data_raw = self.csv_data_raw[self.csv_data_raw['gametype'] == game_type]
            print(f"Successfully loaded {self.csv_path}!")
        except FileNotFoundError as e:
            print(f"An error occurred while loading {self.csv_path}!")
            print(e)
            sys.exit()

