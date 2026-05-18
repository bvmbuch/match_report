import pandas as pd
from data.queries import get_available_seasons, get_available_leagues, get_available_teams, get_available_matches, get_match_events, get_match_goals



def has_qualifier(qualifiers, display_name):
    return any(q['type']['displayName'] == display_name for q in qualifiers)


def sort_data(df):

    df=df[df['period'].isin(['FirstHalf', 'SecondHalf'])].copy()

    mapping = {
        'FirstHalf': 1,
        'SecondHalf': 2
    }

    df['period'] = df['period'].map(mapping)
    df = df.sort_values(['period', 'minute', 'second'])

    return df

TEAM_NAME_MAPPING = {
    'Manchester United': 'Man Utd',
    'Manchester City': 'Man City',
}

def get_match_teams(game_id):
    events = get_match_events(game_id)
    game = events['game'].iloc[0]
    home_team, away_team = game[11:].split('-', maxsplit=1)
    home_team = TEAM_NAME_MAPPING.get(home_team, home_team)
    away_team = TEAM_NAME_MAPPING.get(away_team, away_team)
    return home_team, away_team

def get_score(game_id):
    goals = get_match_goals(game_id)
    home_team, away_team = get_match_teams(game_id)

    home_goals = goals[
        (goals['team'] == home_team) & (~goals['qualifiers'].apply(lambda x: has_qualifier(x, 'OwnGoal')))
    ]
    away_goals = goals[
        (goals['team'] == away_team) & (~goals['qualifiers'].apply(lambda x: has_qualifier(x, 'OwnGoal')))
    ]
    own_goals_home = goals[
        (goals['team'] == away_team) & (goals['qualifiers'].apply(lambda x: has_qualifier(x, 'OwnGoal')))
    ]
    own_goals_away = goals[
        (goals['team'] == home_team) & (goals['qualifiers'].apply(lambda x: has_qualifier(x, 'OwnGoal')))
    ]

    home_score = len(home_goals) + len(own_goals_home)
    away_score = len(away_goals) + len(own_goals_away)

    return home_score, away_score

def get_matches_display(season, league, team):
    matches_df = get_available_matches(season, league, team)
    matches_df['date'] = pd.to_datetime(matches_df['game'].str[:10])
    matches_df = matches_df.sort_values('date', ascending=False)
    
    labels = []
    for _, row in matches_df.iterrows():
        game_id = row['game_id']
        home_team, away_team = get_match_teams(game_id)
        home_score, away_score = get_score(game_id)
        date = row['game'][:10]
        label = f"{home_team} {home_score} - {away_score} {away_team}"
        labels.append(label)
    
    return dict(zip(labels, matches_df['game_id']))

    


def get_league_season_date(game_id):
    events = get_match_events(game_id)
    league=events['league'].iloc[0]
    season=events['season'].iloc[0]
    date=pd.to_datetime(events['game'].iloc[0][:10]).strftime('%d-%m-%Y')

    return league, season, date

def is_start_in_final_3rd_pitch(df):
    
    df['is_start_in_final_3rd'] =df['x']>66.6
    
    return df

def is_end_in_final_3rd_pitch(df):
    df['is_end_in_final_3rd'] =df['end_x']>66.6

    return df

def get_passes(game_id):
    df=get_match_events(game_id)
    return df[df['type']=='Pass']
    
def get_passes_into_final_3rd_pitch(game_id):

    passes=get_passes(game_id)
    passes=is_start_in_final_3rd_pitch(passes)
    passes=is_end_in_final_3rd_pitch(passes)
   
    return passes[(passes['is_start_in_final_3rd'] == False) & (passes['is_end_in_final_3rd'] == True)]

def get_all_shots(game_id):
    df=get_match_events(game_id)
    
    return df[df['is_shot']=='true']


