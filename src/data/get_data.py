import pandas as pd

def get_data():
    """ Get current data from Our World in Data """
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df_owid = pd.read_csv(url, sep=',')
    df_owid.to_csv("../data/raw/covid_full_data.csv", sep=";")


if __name__ == '__main__':
    get_data()