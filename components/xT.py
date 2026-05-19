import pandas as pd
from mplsoccer import Pitch, VerticalPitch
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from analysis.plots import xT_flow_plot, xT_heatmap
from analysis.xthreat import get_xT_flow_data

from data.processing import get_score, get_match_teams, has_qualifier, sort_data

def render_xT_tab(game_id):
    
    
    home_team, away_team = get_match_teams(game_id)
    team = st.pills("Select a team", [home_team, away_team], selection_mode="single", default=home_team, key="xT_team_pills")
    if team is None:
        st.warning("Select a team")
        return


    col1, col2 = st.columns([1.2, 2.8])
    
    with col1:
        fig = xT_heatmap(game_id, team)
        st.pyplot(fig, transparent=True)
    
    with col2:
        
        fig = xT_flow_plot(game_id)
        st.pyplot(fig, transparent=True)