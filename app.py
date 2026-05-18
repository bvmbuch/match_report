import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mplsoccer as mpl

from data.queries import get_available_seasons, get_available_leagues, get_available_teams, get_available_matches
from components.match_info import match_info
from components.shots import render_shots_tab
from data.processing import get_score, get_match_teams, get_matches_display



st.set_page_config(layout="wide")



st.title("Match Report")
st.write("This is a test")
st.sidebar.title("Options")

option1 = st.sidebar.selectbox("Select a season", ["Select a season"] + get_available_seasons())

if option1 != "Select a season":
    option2 = st.sidebar.selectbox("Select a league", ["Select a league"] + get_available_leagues(option1))
else:
    option2 = "Select a league"

if option2 != "Select a league":
    option3 = st.sidebar.selectbox("Select a team", ["Select a team"] + get_available_teams(option1, option2))
else:
    option3 = "Select a team"

if option3 != "Select a team":
    matches_dict = get_matches_display(option1, option2, option3)
    option4 = st.sidebar.selectbox("Select a match", ["Select a match"] + list(matches_dict.keys()))
else:
    option4 = "Select a match"


tab1, tab2, tab3 = st.tabs(["Match Info", "Shots", "Passes"])

with tab1:
    st.header("Match Info")
    if option4 != "Select a match":
        match_info(matches_dict[option4])
with tab2:
    st.header("Shots")
    if option4 != "Select a match":

        render_shots_tab(matches_dict[option4])
with tab3:
    st.header("Passes")
    st.write("This is where the passes will be displayed.")