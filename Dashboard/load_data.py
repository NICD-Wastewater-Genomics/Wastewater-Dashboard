import pandas as pd

def load_rsa_cases_and_levels():
    return pd.read_csv("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/rsa_cases_vs_levels.csv")


def load_monthly_data():
    return pd.read_csv("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/NICD_monthly.csv",index_col=0)


def load_monthly_data_smoothed():
    return pd.read_csv("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/NICD_daily_smoothed.csv",index_col=0)


def load_provincial_cases_levels():
    return pd.read_csv("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/provincial_cases_vs_levels.csv")


def load_provincial_merged():
    return pd.read_csv("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/merged_data.tsv",sep='\t',index_col=0)