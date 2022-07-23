import pandas as pd

def process_owid_data():
    """ Processes the data fetched ffrom Our World in Data by selecting the relevant columns """
    df_owid = pd.read_csv("../data/raw/covid_full_data.csv", sep=";")
    df_selection = df_owid[['date', 'location', 'total_cases', 'people_vaccinated_per_hundred']].sort_values('date',ascending=True).reset_index(drop=True).copy()
    df_selection = df_selection.drop(df_selection[df_selection['location'] == 'Western Sahara'].index)     # Drop Western Sahara as it has too little data for the rolling window
    df_selection.to_csv("../data/processed/data_owid_selection.csv", sep=";")

if __name__ == '__main__':
    process_owid_data()