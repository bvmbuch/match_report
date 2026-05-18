import streamlit as st
import pandas as pd
import ast
import numpy as np
import pickle
import os
from data.processing import get_match_teams, has_qualifier, get_all_shots


POST1 = (100, 45.2)
POST2 = (100, 54.8)
GOAL_CENTER = (100, 50)

QUALIFIER_COLS = [
    'FromCorner', 'IndividualPlay', 'FirstTouch',
    'RegularPlay', 'Head', 'Volley', 'BigChance',
    'ThrowinSetPiece', 'DirectFreekick', 'OneOnOne',
    'SetPiece', 'Penalty', 'OtherBodyPart', 'FastBreak',
]
# Dokładna kolejność features wymagana przez model
FEATURE_COLS = ['x', 'y', *QUALIFIER_COLS, 'angle', 'distance_to_center']



@st.cache_resource
def load_xg_model():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'xg_model.pkl')
    with open(model_path, 'rb') as f:
        return pickle.load(f)

def get_angle(x, y):
    v1 = np.array([POST1[0] - x, POST1[1] - y])
    v2 = np.array([POST2[0] - x, POST2[1] - y])
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    cos_angle = np.clip(cos_angle, -1, 1)
    angle_rad = np.arccos(cos_angle)
    return np.degrees(angle_rad)

def get_distance(x, y):
    v = np.array([GOAL_CENTER[0] - x, GOAL_CENTER[1] - y])
    return np.linalg.norm(v)


def prepare_shots_for_xg(df, parse_qualifiers=False):
    """
    Przygotowuje DataFrame strzałów do predykcji xG.
    
    Parameters
    ----------
    df : pd.DataFrame
        Surowy DataFrame z kolumnami: x, y, qualifiers (i opcjonalnie is_goal).
        Zakłada że są to już strzały (is_shot=True), filtrowanie wykonaj wcześniej.
    parse_qualifiers : bool
        True jeśli kolumna 'qualifiers' jest stringiem (np. z CSV) i trzeba ją sparsować.
        False jeśli to już lista dictów (np. z bezpośredniego scrape'u).
    
    Returns
    -------
    pd.DataFrame
        DataFrame z features w odpowiedniej kolejności (FEATURE_COLS),
        gotowy do model.predict_proba().
    """
    df = df.copy()
    df['x'] = pd.to_numeric(df['x'], errors='coerce')
    df['y'] = pd.to_numeric(df['y'], errors='coerce')
    
    # 1. Parsowanie qualifierów ze stringa jeśli trzeba
    if parse_qualifiers:
        def parse_qualifiers_value(value):
            if value is None:
                return []
            if isinstance(value, str):
                value = value.strip()
                if value == '':
                    return []
                try:
                    return ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    return []
            if isinstance(value, dict):
                return [value]
            if isinstance(value, (list, tuple, set, pd.Series, np.ndarray)):
                return list(value)
            return []

        df['qualifiers'] = df['qualifiers'].apply(parse_qualifiers_value)
    
    # 2. Ekstrakcja qualifierów do bool/int kolumn
    for q in QUALIFIER_COLS:
        df[q] = df['qualifiers'].apply(lambda quals: bool(has_qualifier(quals, q)))
    
    df[QUALIFIER_COLS] = df[QUALIFIER_COLS].fillna(False).astype('int8')
    
    # 3. Feature engineering geometryczny
    df['angle'] = df.apply(lambda row: get_angle(row['x'], row['y']), axis=1)
    df['distance_to_center'] = df.apply(lambda row: get_distance(row['x'], row['y']), axis=1)
    
    df['angle'] = pd.to_numeric(df['angle'], errors='coerce')
    df['distance_to_center'] = pd.to_numeric(df['distance_to_center'], errors='coerce')
    
    # 4. Zwróć tylko features w odpowiedniej kolejności
    return df[FEATURE_COLS].copy()


def predict_xg(df, model, parse_qualifiers=True, return_full=False):
    """
    Liczy xG dla DataFrame strzałów.
    
    Parameters
    ----------
    df : pd.DataFrame
        Surowy DataFrame strzałów.
    model : trained XGBClassifier
        Wytrenowany model xG.
    parse_qualifiers : bool
        Patrz prepare_shots_for_xg.
    return_full : bool
        True - zwraca cały df z dodanymi kolumnami xg, npxg, features.
        False - zwraca tylko Series z xg.
    
    Returns
    -------
    pd.Series lub pd.DataFrame
    """
    X = prepare_shots_for_xg(df, parse_qualifiers=parse_qualifiers)
    xg = model.predict_proba(X)[:, 1]
    
    if not return_full:
        return pd.Series(xg, index=df.index, name='xg')
    
    result = df.copy()
    result['xg'] = xg
    
    # jeśli parsowaliśmy qualifiery, zwróć je już przeparsowane
    if parse_qualifiers and 'qualifiers' in result.columns:
        result['qualifiers'] = result['qualifiers'].apply(
            lambda v: ast.literal_eval(v) if isinstance(v, str) and v.strip() else (v if isinstance(v, list) else [])
        )
    
    return result


def add_xg_to_shots(shots_df, parse_qualifiers=True):
    model = load_xg_model()
    return predict_xg(shots_df, model, parse_qualifiers=True, return_full=True)



def team_xg_events(game_id, team):
    shots = get_all_shots(game_id)
    shots_with_xg = add_xg_to_shots(shots)
    team_shots = shots_with_xg[shots_with_xg['team'] == team]

    return team_shots
