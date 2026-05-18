import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch

from data.queries import get_available_seasons, get_available_leagues, get_available_teams, get_available_matches
from data.processing import get_score, get_match_teams
from analysis.expected_goals import team_xg_events

def shots_plot(game_id, team):

    shots=team_xg_events(game_id, team)

    goals=shots[shots['is_goal']=='true']
    no_goals=shots[shots['is_goal']!='true']
    


    pitch = VerticalPitch(pitch_type='opta', pitch_color='#0C0D0E', line_color='#ebebeb', half=True, pad_bottom=.1)
    fig, ax = pitch.draw(figsize=(10, 8), constrained_layout=True, tight_layout=False)

    plt.title(f'Shots for {team}')
   
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

