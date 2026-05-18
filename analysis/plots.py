import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch


from analysis.passes import prepare_passes
from data.queries import get_available_seasons, get_available_leagues, get_available_teams, get_available_matches
from data.processing import get_score, get_match_teams, has_qualifier
from analysis.expected_goals import team_xg_events
from analysis.pass_network import average_location, prepare_for_pass_network, pass_between
#npxg - non penalty xg
def shots_plot(game_id, team, npxg=False, player=None):

    shots=team_xg_events(game_id, team)

    if player:
        shots = shots[shots['player'] == player]

    if npxg:
        shots = shots[~shots['qualifiers'].apply(lambda x: has_qualifier(x, 'Penalty'))]



    goals=shots[shots['is_goal']=='true']
    no_goals=shots[shots['is_goal']!='true']
    


    pitch = VerticalPitch(pitch_type='opta', pitch_color='#0C0D0E', line_color='#ebebeb', half=True, pad_bottom=.1)
    fig, ax = pitch.draw(figsize=(10, 8), constrained_layout=True, tight_layout=False)

   

   
    pitch.scatter(
        no_goals['x'], no_goals['y'],
        s=no_goals['xg'] * 1300,   
        ax=ax,
        color='red',
        alpha=0.6,
        edgecolors='white'
    )

    pitch.scatter(
        goals['x'], goals['y'],
        s=goals['xg'] * 1300,    
        ax=ax,
        color='green',
        alpha=0.6,
        edgecolors='white'
    )

    return fig





def passes_plot(game_id, team, player=None, successful_only=False, color="#3d91ce", pass_type='All'):
    passes=prepare_passes(game_id, team, player, successful_only, pass_type)

    pitch = VerticalPitch(pitch_type='opta', pitch_color='#0C0D0E', line_color='#ebebeb', pad_bottom=.1)
    fig, ax = pitch.draw(figsize=(10, 8), constrained_layout=True, tight_layout=False)

    pitch.arrows(
        passes['x'], passes['y'], 
        passes['end_x'], passes['end_y'], 
        ax=ax,
        color=color,
        alpha=0.6,
        width=2
    )

    return fig


def pass_network_plot(game_id, team, no_passes_threshold=2, include_substitution=False):
    df=prepare_for_pass_network(game_id, team, include_substitution)
    avg_loc = average_location(df)
    pb = pass_between(df, no_passes_threshold)

    pitch = VerticalPitch(pitch_type='opta', pitch_color='#0C0D0E', line_color='#ebebeb', pad_bottom=.1)
    fig, ax = pitch.draw(figsize=(10, 8), constrained_layout=True, tight_layout=False)

    pitch.lines(pb['x'], pb['y'], pb['x_end'], pb['y_end'], ax=ax, color="#d5ecfc", alpha=0.6, linewidth=pb['pass_count'], zorder=1, alpha_start=0.4)

    pitch.scatter(avg_loc['x'], avg_loc['y'], s=avg_loc['count']*20, ax=ax, color='#3d91ce', edgecolors='white', zorder=3)   
    
    return fig