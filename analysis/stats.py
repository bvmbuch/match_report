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
    