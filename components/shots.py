import pandas as pd
from mplsoccer import Pitch, VerticalPitch
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from analysis.plots import shots_plot
from analysis.expected_goals import team_xg_events, team_xg_table
from data.queries import get_available_seasons, get_available_leagues, get_available_teams, get_available_matches, get_match_events, get_match_goals
from data.processing import get_all_players, get_score, get_match_teams, has_qualifier, sort_data, get_passes_into_final_3rd_pitch, get_passes, get_players_with_shots


def render_shots_tab(game_id):
    
    home_team, away_team = get_match_teams(game_id)
    player=None
    
    col1, col2, col3 = st.columns([1, 3.5, 1.5])

    with col1:
            
        team=st.pills("Select a team", [home_team, away_team], selection_mode="single", default=home_team, key="team_shots")
        if team is None:
            st.warning("Select a team")
            return
        
        
        npxg=st.toggle("Show non-penalty xG", value=False, key="npxg_toggle")

        player_on=st.toggle("Show specific player", value=False, key="player_shots_toggle")

        if player_on:
                players_home, players_away = get_players_with_shots(game_id)
                if team == home_team:
                    player=st.selectbox("Select a player", players_home, key="player_shots_select")
                else:
                    player=st.selectbox("Select a player", players_away, key="player_shots_select")

    
    with col2:
        if player_on:
            fig = shots_plot(game_id, team, npxg, player)
            st.pyplot(fig, transparent=True)
        else:

            fig = shots_plot(game_id, team, npxg, player)
            st.pyplot(fig, transparent=True)


    with col3:
        xg_table = team_xg_table(game_id, team)
        st.subheader("Expected Goals (xG) by Player")
        st.table(xg_table)