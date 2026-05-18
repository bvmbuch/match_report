from asyncio import events

import pandas as pd
from analysis.expected_goals import add_xg_to_shots
from data.queries import get_available_seasons, get_available_leagues, get_available_teams, get_available_matches, get_match_events, get_match_goals
from data.processing import get_all_shots, get_score, get_match_teams, has_qualifier, sort_data, get_passes_into_final_3rd_pitch, get_passes

#stats: goals, xg, shots, xg on target, xg/shot,  podania, xT, field tilt

def get_passes_count(game_id):
    passes = get_passes(game_id)
   
    home_team, away_team = get_match_teams(game_id)

    passes_home = passes[passes['team'] == home_team]
    passes_away = passes[passes['team'] == away_team]


    return len(passes_home), len(passes_away)

def get_completed_passes_count(game_id):
    passes = get_passes(game_id)
   
    home_team, away_team = get_match_teams(game_id)

    completed_passes_home = passes[(passes['team'] == home_team) & (passes['outcome_type']=='Successful')]
    completed_passes_away = passes[(passes['team'] == away_team) & (passes['outcome_type']=='Successful')]

    return len(completed_passes_home), len(completed_passes_away)

def get_completion_rate(game_id):
    passes = get_passes(game_id)
   
    home_team, away_team = get_match_teams(game_id)

    completed_passes_home = passes[(passes['team'] == home_team) & (passes['outcome_type']=='Successful')]
    completed_passes_away = passes[(passes['team'] == away_team) & (passes['outcome_type']=='Successful')]

    total_passes_home = passes[passes['team'] == home_team]
    total_passes_away = passes[passes['team'] == away_team]

    completion_rate_home = len(completed_passes_home) / len(total_passes_home) if len(total_passes_home) > 0 else 0
    completion_rate_away = len(completed_passes_away) / len(total_passes_away) if len(total_passes_away) > 0 else 0

    return completion_rate_home, completion_rate_away

def get_passes_into_final_3rd_count(game_id):
    passes_final_3rd = get_passes_into_final_3rd_pitch(game_id)
    home_team, away_team = get_match_teams(game_id)
    

    passes_final_3rd_home = passes_final_3rd[(passes_final_3rd['team'] == home_team) & (passes_final_3rd['outcome_type']=='Successful')]
    passes_final_3rd_away = passes_final_3rd[(passes_final_3rd['team'] == away_team) & (passes_final_3rd['outcome_type']=='Successful')]

    return len(passes_final_3rd_home), len(passes_final_3rd_away)


def get_xg(game_id):
    shots = get_all_shots(game_id)
    home_team, away_team = get_match_teams(game_id)

    shots=add_xg_to_shots(shots)

    shots_home = shots[shots['team'] == home_team]
    shots_away = shots[shots['team'] == away_team]


    home_xg = shots_home['xg'].sum()
    away_xg = shots_away['xg'].sum()

    return home_xg, away_xg

def get_npxg(game_id):
    shots= get_all_shots(game_id)
    home_team, away_team = get_match_teams(game_id)
    shots=add_xg_to_shots(shots)

    np_shots=shots[~shots['qualifiers'].apply(lambda x: has_qualifier(x, 'Penalty'))]

    np_shots_home = np_shots[np_shots['team'] == home_team]
    np_shots_away = np_shots[np_shots['team'] == away_team]

    home_npxg = np_shots_home['xg'].sum()
    away_npxg = np_shots_away['xg'].sum()

    return home_npxg, away_npxg


def get_bigChances(game_id):
    shots = get_all_shots(game_id)
    home_team, away_team = get_match_teams(game_id)

    shots=add_xg_to_shots(shots)

    big_chances_home = shots[(shots['team'] == home_team) & (shots['qualifiers'].apply(lambda x: has_qualifier(x, 'BigChance')))]
    big_chances_away = shots[(shots['team'] == away_team) & (shots['qualifiers'].apply(lambda x: has_qualifier(x, 'BigChance')))]

    return len(big_chances_home), len(big_chances_away)
    
def get_longpass_prcnt(game_id):
    events=get_match_events(game_id)
    passes=events[events['type']=='Pass']
    home_team, away_team = get_match_teams(game_id)

    long_passes_home = passes[(passes['team'] == home_team) & (passes['qualifiers'].apply(lambda x: has_qualifier(x, 'Longball')))]
    long_passes_away = passes[(passes['team'] == away_team) & (passes['qualifiers'].apply(lambda x: has_qualifier(x, 'Longball')))]

    total_passes_home = passes[passes['team'] == home_team]
    total_passes_away = passes[passes['team'] == away_team]

    long_pass_prcnt_home = len(long_passes_home) / len(total_passes_home) if len(total_passes_home) > 0 else 0
    long_pass_prcnt_away = len(long_passes_away) / len(total_passes_away) if len(total_passes_away) > 0 else 0

    return long_pass_prcnt_home, long_pass_prcnt_away

def get_field_tilt(game_id):
    events = get_match_events(game_id)
    passes = events[events['type'] == 'Pass']
    home_team, away_team = get_match_teams(game_id)

    home_final_third = len(passes[(passes['team'] == home_team) & (passes['x'] > 66.6)])
    away_final_third = len(passes[(passes['team'] == away_team) & (passes['x'] > 66.6)])
    total = home_final_third + away_final_third

    home_tilt = home_final_third / total if total > 0 else 0
    away_tilt = away_final_third / total if total > 0 else 0

    return home_tilt, away_tilt

def get_ppda(game_id):
    events = get_match_events(game_id)
    home_team, away_team = get_match_teams(game_id)

    defensive_actions = ['Tackle', 'Interception', 'Challenge', 'Foul', 'BlockedPass']

    home_passes = len(events[(events['team'] == home_team) & (events['type'] == 'Pass') & (events['x'] > 40.0)])
    away_passes = len(events[(events['team'] == away_team) & (events['type'] == 'Pass') & (events['x'] >40.0)])

    home_def = len(events[(events['team'] == home_team) & (events['type'].isin(defensive_actions)) & (events['x'] > 40.0)])
    away_def = len(events[(events['team'] == away_team) & (events['type'].isin(defensive_actions)) & (events['x'] > 40.0)])

    ppda_home = away_passes / home_def if home_def > 0 else 0
    ppda_away = home_passes / away_def if away_def > 0 else 0

    return ppda_home, ppda_away