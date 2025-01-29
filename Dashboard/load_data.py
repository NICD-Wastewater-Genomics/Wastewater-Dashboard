import pandas as pd
import json, urllib.request
import requests

def load_rsa_cases_and_levels():
    return pd.read_feather("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/rsa_cases_vs_levels.feather")


def load_monthly_data():
    return pd.read_feather("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/NICD_monthly.feather")


def load_monthly_data_smoothed():
    return pd.read_feather("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/NICD_daily_smoothed.feather")


def load_provincial_cases_levels():
    return pd.read_feather("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/provincial_cases_vs_levels.feather")


def load_provincial_merged():
    return pd.read_feather("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/merged_data_exploded.feather")

def load_color_map():
    return pd.read_json("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Freyja-outputs-/main/scripts/color_map.json",typ='series')