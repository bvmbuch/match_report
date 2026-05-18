import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch

from data.queries import get_available_seasons, get_available_leagues, get_available_teams, get_available_matches
from data.processing import get_score, get_match_teams, has_qualifier
from analysis.expected_goals import team_xg_events
#npxg - non penalty xg
def shots_plot(game_id, team, npxg=False, player=None):

    shots=team_xg_events(game_id, team)

    if player:
        shots = shots[shots['player'] == player]

    npxg_shots= shots[~shots['qualifiers'].apply(lambda x: has_qualifier(x, 'Penalty'))]

    npxg_goals=npxg_shots[npxg_shots['is_goal']=='true']
    npxg_no_goals=npxg_shots[npxg_shots['is_goal']!='true']

    goals=shots[shots['is_goal']=='true']
    no_goals=shots[shots['is_goal']!='true']
    


    pitch = VerticalPitch(pitch_type='opta', pitch_color='#0C0D0E', line_color='#ebebeb', half=True, pad_bottom=.1)
    fig, ax = pitch.draw(figsize=(10, 8), constrained_layout=True, tight_layout=False)

    if npxg:

        pitch.scatter(
            npxg_no_goals['x'], npxg_no_goals['y'],
            s=npxg_no_goals['xg'] * 1300,   
            ax=ax,
            color='red',
            alpha=0.6,
            edgecolors='white'
        )

        pitch.scatter(
            npxg_goals['x'], npxg_goals['y'],
            s=npxg_goals['xg'] * 1300,    
            ax=ax,
            color='green',
            alpha=0.6,
            edgecolors='white'
        )


    else:
   
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
