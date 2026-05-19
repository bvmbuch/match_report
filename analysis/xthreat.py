import pandas as pd
import numpy as np 
import os

from data.queries import get_match_events
from data.processing import get_match_teams, has_qualifier, sort_data, SET_PIECE_QUALIFIERS


def get_xT():
    xT_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'xT_Grid.csv')
    xT = pd.read_csv(xT_path, header=None).values
    xT_rows , xT_cols = xT.shape

    return xT_rows, xT_cols, xT

def assign_xT_values(df):
    xT_rows, xT_cols, xT = get_xT()
    
    df=df.copy()
    df['x1_bin']= pd.cut(df['x'], bins=xT_cols, labels=False)
    df['y1_bin']= pd.cut(df['y'], bins=xT_rows, labels=False)
    df['x2_bin']= pd.cut(df['end_x'], bins=xT_cols, labels=False)
    df['y2_bin']= pd.cut(df['end_y'], bins=xT_rows, labels=False)

    df['xT_start'] = df.apply(lambda r: xT[int(r['y1_bin'])][int(r['x1_bin'])] 
                            if pd.notna(r['y1_bin']) and pd.notna(r['x1_bin']) else 0, axis=1)
    
    df['xT_end'] = df.apply(lambda r: xT[int(r['y2_bin'])][int(r['x2_bin'])] 
                            if pd.notna(r['y2_bin']) and pd.notna(r['x2_bin']) else 0, axis=1)
    

    df['xT'] = df['xT_end'] - df['xT_start']

    return df
def get_xT_df(game_id, team, regular_play=True):
    events = get_match_events(game_id)
    events = sort_data(events)
    passes = events[events['type'] == 'Pass']
    if regular_play:
        passes = passes[~passes['qualifiers'].apply(lambda x: any(has_qualifier(x, q) for q in SET_PIECE_QUALIFIERS.keys()))]
    passes = assign_xT_values(passes)
    passes = passes[(passes['team'] == team) & (passes['xT'] > 0)]

    return passes

def get_xT_flow_data(game_id):
    events = get_match_events(game_id)
    events = sort_data(events)
    home_team, away_team = get_match_teams(game_id)

    passes = events[events['type'] == 'Pass']
    passes = passes.copy()
    passes= assign_xT_values(passes)

    passes = passes[passes['xT'] > 0]
    
    passes['cumulative_mins'] = passes['minute'] + passes['second'] / 60
    first_half_max = passes[passes['period'] == 1]['cumulative_mins'].max()
    second_half_min = passes[passes['period'] == 2]['cumulative_mins'].min()
    passes.loc[passes['period'] == 2, 'cumulative_mins'] += first_half_max - second_half_min
    passes['minute_bin'] = passes['cumulative_mins'].apply(np.floor)
    
    home = passes[passes['team'] == home_team].groupby('minute_bin')['xT'].sum()
    away = passes[passes['team'] == away_team].groupby('minute_bin')['xT'].sum()
    
    all_mins = pd.RangeIndex(0, int(passes['minute_bin'].max()) + 1)
    home = home.reindex(all_mins, fill_value=0)
    away = away.reindex(all_mins, fill_value=0)
    
    home_rolling = home.rolling(9, min_periods=1).mean()
    away_rolling = away.rolling(9, min_periods=1).mean()

    return home_rolling, away_rolling