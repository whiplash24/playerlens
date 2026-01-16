import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/raw/database.sqlite")

def load_table(table_name):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

def load_players():
    return load_table("Player")

def load_matches():
    return load_table("Match")

def load_teams():
    return load_table("Team")

def load_player_attributes():
    return load_table("Player_Attributes")
