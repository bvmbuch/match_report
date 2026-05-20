import pandas as pd
from mplsoccer import Pitch, VerticalPitch
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from analysis.passes import team_passes_table
from analysis.plots import passes_plot
from analysis.expected_goals import team_xg_events
from data.queries import get_available_seasons, get_available_leagues, get_available_teams, get_available_matches, get_match_events, get_match_goals
from data.processing import get_all_players, get_players_with_passes, get_score, get_match_teams, has_qualifier, sort_data, get_passes_into_final_3rd_pitch, get_passes, get_players_with_shots

def render_passes_tab(game_id):
    home_team, away_team = get_match_teams(game_id)
    player=None
    
    col1, col2, col3 = st.columns([1, 1.3, 1.1])

    with col1:
            
        team=st.pills("Select a team", [home_team, away_team], selection_mode="single", default=home_team, key="team_pass")
        if team is None:
            st.warning("Select a team")
            return
        
        player_on=st.toggle("Show specific player", value=False, key="player_pass_toggle")

        if player_on:
            players_home, players_away = get_players_with_passes(game_id)
            if team == home_team:
                player=st.selectbox("Select a player", players_home, key="player_pass_select")
            else:
                player=st.selectbox("Select a player", players_away, key="player_pass_select")

        successful_only=st.toggle("Show only successful passes", value=False, key="successful_pass_toggle")
        color = "#048520" if successful_only else "#4093FF"

        pass_type=st.pills("Select pass type", ["All", "Progressive", "In final 3rd", "Into final 3rd", "Key Pass", "Long Pass"], selection_mode="single", default="All", key="pass_type")
    
    with col2:
        if player_on:
            fig = passes_plot(game_id, team, player, successful_only, color, pass_type)
            st.pyplot(fig, use_container_width=False, transparent=True)
        else:

            fig = passes_plot(game_id, team, None, successful_only, color, pass_type)
            st.pyplot(fig, use_container_width=False, transparent=True)

    with col3:
        passes_table = team_passes_table(game_id, team)
        st.subheader("Passes by Player")
        st.table(passes_table)

    with st.expander("How to read this tab"):
        st.write("""
        Pass map for the selected team. Filter by player or pass type: Progressive, In Final Third, Into Final Third, Key Pass, or Long Pass. Toggle to show only successful passes.
        
        The table on the right shows total passes and completion ratio per player.
        """)