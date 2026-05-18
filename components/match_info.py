import streamlit as st

import pandas as pd
from data.queries import get_available_seasons, get_available_leagues, get_available_teams, get_available_matches, get_match_events
from data.processing import get_score, get_match_teams, get_league_season_date
from analysis.stats import get_passes_count, get_completed_passes_count, get_completion_rate, get_passes_into_final_3rd_count, get_xg, get_npxg, get_bigChances
from analysis.plots import pass_network_plot



def match_info(game_id):
    events=get_match_events(game_id)
    home_team, away_team = get_match_teams(game_id)
    home_score, away_score = get_score(game_id)
    league, season, date = get_league_season_date(game_id)
    #text_team=f"{home_team} {home_score} - {away_score} {away_team}"

    info_text=f"{league} | {season} | {date}"

    col1, col2, col3 = st.columns([5, 8, 5])

    with col1:
        st.markdown(f"<h1 style='text-align: right;'>{home_team}</h1>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<h1 style='text-align: center;'>{home_score} - {away_score}</h1>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<h1 style='text-align: left;'>{away_team}</h1>", unsafe_allow_html=True)

    st.markdown(f"<p style='text-align: center;'>{info_text}</p>", unsafe_allow_html=True)



    col1, col2, col3 = st.columns([4,2,4])

    with col1:
        fig= pass_network_plot(game_id, home_team)
        st.pyplot(fig, transparent=True)

    with col2:
        home_passes, away_passes = get_passes_count(game_id)
        home_completed_passes, away_completed_passes = get_completed_passes_count(game_id)
        home_completion_rate, away_completion_rate = get_completion_rate(game_id)
        home_passes_final_3rd, away_passes_final_3rd = get_passes_into_final_3rd_count(game_id)
        home_xg, away_xg = get_xg(game_id)
        home_npxg, away_npxg = get_npxg(game_id)
        home_big_chances, away_big_chances = get_bigChances(game_id)
        st.markdown("<br><br>", unsafe_allow_html=True)
        stats_html = f"""
        <div style="
            background-color: #1e1e2e;
            border: 1px solid #444;
            border-radius: 12px;
            padding: 24px;
            margin: 100 px 0 16px 0;
            width: 100%;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #333;">
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: left;">{home_score}</span>
                <span style="color: #888; width: 40%; text-align: center;">Goals</span>
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: right;">{away_score}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #333;">
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: left;">{home_xg:.2f}</span>
                <span style="color: #888; width: 40%; text-align: center;">xG</span>
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: right;">{away_xg:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #333;">
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: left;">{home_npxg:.2f}</span>
                <span style="color: #888; width: 40%; text-align: center;">npxG</span>
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: right;">{away_npxg:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #333;">
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: left;">{home_passes}</span>
                <span style="color: #888; width: 40%; text-align: center;">Passes</span>
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: right;">{away_passes}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #333;">
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: left;">{home_big_chances}</span>
                <span style="color: #888; width: 40%; text-align: center;">Big Chances</span>
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: right;">{away_big_chances}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #333;">
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: left;">{home_completed_passes}</span>
                <span style="color: #888; width: 40%; text-align: center;">Completed Passes</span>
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: right;">{away_completed_passes}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #333;">
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: left;">{home_completion_rate:.1%}</span>
                <span style="color: #888; width: 40%; text-align: center;">Completion Rate</span>
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: right;">{away_completion_rate:.1%}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #333;">
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: left;">{home_passes_final_3rd}</span>
                <span style="color: #888; width: 40%; text-align: center;">Passes into Final Third</span>
                <span style="font-size: 20px; font-weight: bold; width: 40%; text-align: right;">{away_passes_final_3rd}</span>
            </div>
            

        </div>
        """

        st.markdown(stats_html, unsafe_allow_html=True)

    with col3:
        fig= pass_network_plot(game_id, away_team)
        st.pyplot(fig, transparent=True)
        


    return 