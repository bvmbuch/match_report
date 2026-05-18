import pandas as pd
from mplsoccer import Pitch, VerticalPitch
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from analysis.plots import shots_plot
from analysis.expected_goals import team_xg_events
from data.queries import get_available_seasons, get_available_leagues, get_available_teams, get_available_matches, get_match_events, get_match_goals
from data.processing import get_score, get_match_teams, has_qualifier, sort_data, get_passes_into_final_3rd_pitch, get_passes

def render_shots_tab(game_id):
    
    home_team, away_team = get_match_teams(game_id)
    

    team=st.pills("Select a team", [home_team, away_team], selection_mode="single", default=home_team)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        fig = shots_plot(game_id, team)
        st.pyplot(fig)