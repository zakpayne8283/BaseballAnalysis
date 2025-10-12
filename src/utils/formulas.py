def calc_hits(hitter_data):
    return(
            hitter_data['single'] +
            hitter_data['double'] +
            hitter_data['triple'] +
            hitter_data['hr']
        )

def calc_rbis(hitter_data):
    return (
        hitter_data['rbi_b'] + hitter_data['rbi1'] + hitter_data['rbi2'] + hitter_data['rbi3']
    )

def calc_avg(hitter_data):
    return round(hitter_data['h'] / hitter_data['ab'], 3)

def calc_onbase(hitter_data):
    # OBP = (Hits + Walks + Hit by Pitch) ÷ (At Bats + Walks + Hit by Pitch + Sacrifice Flies)
    return round(
        (hitter_data['h'] + hitter_data['walk'] + hitter_data['hbp']) /
        (hitter_data['ab'] + hitter_data['walk'] + hitter_data['hbp'] + hitter_data['sf']), 3)

def calc_slugging(hitter_data):
    # SLG = (Singles + (2 × Doubles) + (3 × Triples) + (4 × Home Runs)) ÷ At Bats
    return round(
        (hitter_data['single'] + (2 * hitter_data['double']) + (3 * hitter_data['triple']) + (4 * hitter_data['hr'])) /
        hitter_data['ab'], 3)