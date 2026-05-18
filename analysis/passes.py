import pandas as pd
import numpy as np

#from data.queries import get_available_seasons, get_available_leagues, get_available_teams, get_available_matches, get_match_events, get_match_goals
from data.processing import has_qualifier, is_in_final_3rd_pitch, is_into_final_3rd_pitch, sort_data, get_passes, add_progressive_flags_opta


def prepare_passes(game_id, team, player=None, successful_only=False, pass_type='All'):
    passes = get_passes(game_id)
    team_passes = passes[passes['team'] == team]

    if pass_type == 'Progressive':
        team_passes=add_progressive_flags_opta(team_passes)
        team_passes = team_passes[team_passes['is_prog_pass'] == True]
    elif pass_type == 'In final 3rd':
        team_passes = is_in_final_3rd_pitch(team_passes)
        team_passes = team_passes[team_passes['is_final_3rd'] == True]
    elif pass_type == 'Into final 3rd':
        team_passes = is_into_final_3rd_pitch(team_passes)
        team_passes = team_passes[team_passes['is_into_final_3rd'] == True]
    elif pass_type=='Key Pass':
        team_passes = team_passes[team_passes['qualifiers'].apply(lambda x: has_qualifier(x, 'KeyPass'))]
    if player:
        player_passes = team_passes[team_passes['player'] == player]

        if successful_only:
            player_passes = player_passes[player_passes['outcome_type'] == 'Successful']
            return player_passes
    
        return player_passes
    
    if successful_only:
        team_passes = team_passes[team_passes['outcome_type'] == 'Successful']
        return team_passes

    return team_passes
     

def team_passes_table(game_id, team):
    passes = prepare_passes(game_id, team)
    table_df = passes.groupby('player').agg(
        total_passes=('type', 'count'),
        comp_ratio=('outcome_type', lambda x: (x == 'Successful').sum() / len(x) if len(x) > 0 else 0),
    ).sort_values(by='total_passes', ascending=False).reset_index()
    
    return table_df