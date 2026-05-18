import pandas as pd
from data.queries import get_available_seasons, get_available_leagues, get_available_teams, get_available_matches, get_match_events, get_match_goals
from data.processing import get_score, get_match_teams, has_qualifier, sort_data, get_passes

def prepare_for_pass_network(match_id, team, include_substitution=False):
    events = get_match_events(match_id)
    events = sort_data(events)
    events = events[events['team'] == team]

    if not include_substitution:
        sub_idx = events[events['type'] == 'SubstitutionOff'].index
        if len(sub_idx) > 0:
            events = events.loc[:sub_idx[0]]

    passes = events[events['type'] == 'Pass']
    passes = passes.copy()
    passes['recipient_id'] = passes['player_id'].shift(-1)
    passes = passes[passes['recipient_id'].notna()]
    passes = passes[passes['outcome_type'] == 'Successful']
   
    last_minute = passes['minute'].max()

    return passes, last_minute

def average_location(df):
    average_locations = df.groupby('player_id').agg({'x':['mean'], 'y':['mean', 'count']})
    average_locations.columns=['x', 'y', 'count']

    return average_locations.reset_index()

def pass_between(df, no_passes_threshold=3):
    pb = df.groupby(['player_id', 'recipient_id'])['x'].count().reset_index()
    pb.rename(columns={'x': 'pass_count'}, inplace=True)
    
    avg_loc = average_location(df)
    
    pb = pb.merge(avg_loc, on='player_id')
    pb = pb.merge(avg_loc, left_on='recipient_id', right_on='player_id', suffixes=['', '_end'])
    
    pb = pb[pb['pass_count'] >= no_passes_threshold]
    
    return pb





