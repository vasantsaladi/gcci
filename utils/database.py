# utils/database.py
import pandas as pd

def load_partnerships():
    try:
        return pd.read_csv("data/partnerships.csv")
    except:
        return pd.DataFrame({
            "name": [],
            "type": [],
            "description": [],
            "status": []
        })

def save_partnership(data):
    partnerships = load_partnerships()
    partnerships = partnerships.append(data, ignore_index=True)
    partnerships.to_csv("data/partnerships.csv", index=False)