import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch
from scipy.ndimage import gaussian_filter, gaussian_filter1d


from analysis.passes import prepare_passes
from analysis.xthreat import get_xT_df, get_xT_flow_data
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
    df, last_minute=prepare_for_pass_network(game_id, team, include_substitution)
    avg_loc = average_location(df)
    pb = pass_between(df, no_passes_threshold)
    
    pitch = VerticalPitch(pitch_type='opta', pitch_color='#0C0D0E', line_color='#ebebeb', pad_bottom=.1)
    fig, ax = pitch.draw(figsize=(10, 8), constrained_layout=True, tight_layout=False)
    ax.set_title(f"0 - {last_minute}'", color='white', fontsize=12)

    pitch.lines(pb['x'], pb['y'], pb['x_end'], pb['y_end'], ax=ax, color="#d5ecfc", alpha=0.6, linewidth=pb['pass_count'], zorder=1, alpha_start=0.4)

    pitch.scatter(avg_loc['x'], avg_loc['y'], s=avg_loc['count']*20, ax=ax, color='#3d91ce', edgecolors='white', zorder=3)   
    
    return fig

def xT_flow_plot(game_id):
    home_team, away_team = get_match_teams(game_id)
    home_xT, away_xT = get_xT_flow_data(game_id)

    diff =home_xT - away_xT
    diff_smooth = pd.Series(gaussian_filter1d(diff.values, sigma=2), index=diff.index)




    fig, ax = plt.subplots(figsize=(12, 5), facecolor='#0C0D0E')
    ax.set_facecolor('#0C0D0E')

    ax.bar(diff_smooth.index[diff_smooth >= 0], diff_smooth[diff_smooth >= 0], color='#3d91ce', alpha=0.6, label=home_team, width=0.71, linewidth=0)
    ax.bar(diff_smooth.index[diff_smooth < 0], diff_smooth[diff_smooth < 0], color='red', alpha=0.6, label=away_team, width=0.71, linewidth=0)
    ax.axhline(0, color='white', linewidth=0.8, alpha=0.5)
    ax.axhline(0, color='white', linewidth=0.8, alpha=0.5)
    
    ax.set_xlabel('Minute', color='white')
    ax.set_ylabel('xT difference', color='white')
    ax.tick_params(colors='white')
    ax.legend(facecolor='#1e1e2e', labelcolor='white')
    ax.spines['bottom'].set_color('#444')
    ax.spines['left'].set_color('#444')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return fig

def xT_heatmap(game_id, team):
    passes = get_xT_df(game_id, team, regular_play=True)

    pitch = VerticalPitch(pitch_type='opta', pitch_color='#0C0D0E', line_color='#ebebeb', pad_bottom=.1)
    fig, ax = pitch.draw(figsize=(10, 8), constrained_layout=True, tight_layout=False)

    bin_statistic = pitch.bin_statistic(passes['x'], passes['y'], values=passes['xT'], statistic='sum', bins=(18, 10))
    bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 1.2)
    
    pitch.heatmap(bin_statistic, ax=ax, cmap='gist_heat', edgecolors='none', alpha=0.7)

    return fig
