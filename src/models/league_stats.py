import pandas as pd

class LeagueStats:
    games = None

    def as_dataframe(self):
        return pd.DataFrame([vars(self)])