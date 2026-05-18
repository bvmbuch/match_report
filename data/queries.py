import streamlit as st
import psycopg2
import pandas as pd
from data.supabase_client import get_connection

@st.cache_data(ttl=3600)
def get_available_seasons():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT season FROM match_events")
            query_result = cursor.fetchall()
            df=pd.DataFrame(query_result, columns=[desc[0] for desc in cursor.description])
            return df['season'].to_list()
        
@st.cache_data(ttl=3600)
def get_available_leagues(season):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT league FROM match_events WHERE season = %s", (season,))
            query_result = cursor.fetchall()
            df=pd.DataFrame(query_result, columns=[desc[0] for desc in cursor.description])
            return df['league'].to_list()
        

@st.cache_data(ttl=3600)
def get_available_teams(season, league):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT team FROM match_events WHERE season = %s AND league = %s", (season, league))
            query_result = cursor.fetchall()
            df=pd.DataFrame(query_result, columns=[desc[0] for desc in cursor.description])
            return df['team'].to_list()


@st.cache_data(ttl=3600)
def get_available_matches(season, league, team):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT game_id, game FROM match_events WHERE season = %s AND league = %s AND team = %s", (season, league, team))
            query_result = cursor.fetchall()
            df=pd.DataFrame(query_result, columns=[desc[0] for desc in cursor.description])
            return df
        
@st.cache_data(ttl=3600)
def get_match_events(game_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM match_events WHERE game_id = %s", (game_id,))
            query_result = cursor.fetchall()
            df=pd.DataFrame(query_result, columns=[desc[0] for desc in cursor.description])
            return df
        
@st.cache_data(ttl=3600)
def get_match_goals(game_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM match_events WHERE game_id = %s AND is_goal = 'true'", (game_id,))
            query_result = cursor.fetchall()
            df=pd.DataFrame(query_result, columns=[desc[0] for desc in cursor.description])
            return df



@st.cache_data(ttl=3600)
def get_teams_and_teams_id(season, league):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT team, team_id FROM match_events WHERE season = %s AND league = %s", (season, league))
            query_result = cursor.fetchall()
            df=pd.DataFrame(query_result, columns=[desc[0] for desc in cursor.description])
            return df
        

def get_all_shots(game_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM match_events WHERE game_id = %s AND is_shot = 'true'", (game_id,))
            query_result = cursor.fetchall()
            df=pd.DataFrame(query_result, columns=[desc[0] for desc in cursor.description])
            return df