import pandas as pd

class LeagueStats:
    games = None
    pa = None
    ab = None
    h = None
    rbi = None
    double = None
    triple = None
    hr = None
    sh = None
    hbp = None
    walk = None
    iw = None
    k = None
    avg = None
    obp = None
    slg = None
    ops = None

    run_expectancy_matrix = None

    def as_dataframe(self):
        return pd.DataFrame([vars(self)])
    
    def add_aggregate_stats(self, series=None):
        if series is None:
            raise Exception

        self.pa = int(series['pa'])
        self.ab = int(series['ab'])
        self.h = int(series['h'])
        self.double = int(series['double'])
        self.triple = int(series['triple'])
        self.hr = int(series['hr'])
        self.rbi = int(series['rbi'])
        self.sh = int(series['sh'])
        self.sf = int(series['sf'])
        self.hbp = int(series['hbp'])
        self.walk = int(series['walk'])
        self.iw = int(series['iw'])
        self.k = int(series['k'])
        self.avg = series['avg']
        self.obp = series['obp']
        self.slg = series['slg']
        self.ops = series['ops']
        