import os
import pandas as pd
import numpy as np


def create_if_not_exists(df, col):
    """
    Create new Dataframe column in case it doesn't exist yet.
    """
    if col not in df.columns:
        df[col] = np.nan

def drop_if_exists(df, col):
    """
    Drop Dataframe column in case it exists.
    """
    if col in df.columns:
        df = df.drop([col], axis=1)
    return df

def rename_if_exists(df, oldcol, newcol):
    """
    Rename Dataframe column in case it exists.
    """
    if oldcol in df.columns:
        df = df.rename(columns={oldcol: newcol})
    return df

def rename_or_create(df, oldcol, newcol):
    """
    Rename Dataframe column in case it exists, otherwise create it.
    """
    if newcol not in df.columns:
        if oldcol in df.columns:
            df = df.rename(columns={oldcol: newcol})
        else:
            df[newcol] = np.nan
    return df

def check_and_convert_dtype(df, col, dtype):
    """
    Compare current dtype with reference and convert if needed.
    """
    # handle missing values for int
    if 'int' in dtype:
        df[col] = df[col].fillna(0)
    # if dtype not as expected -> convert dtype
    if df[col].dtypes != dtype:
        df[col] = df[col].astype(dtype)
    return df

def main():
    """
    Read CSV files, add date, harmonize and rewrite them.
    """
    # get filelist from current folder
    filelist = os.listdir('./')

    for file in filelist:
        # only consider csv files
        if '.csv' in file:
            # extract and reformat date from filename
            date = file.split('.')[0]
            date_parts = date.split('-')
            date_formatted = '{}-{}-{}'.format(date_parts[2],
                                               date_parts[0],
                                               date_parts[1])
            # read current csv file
            df = pd.read_csv(file, encoding="utf-8-sig")
            # add new date column
            if 'Date' not in df.columns:
                df['Date'] = date_formatted

            # harmonize columns
            create_if_not_exists(df, 'FIPS')
            create_if_not_exists(df, 'Admin2')
            create_if_not_exists(df, 'Active')

            df = rename_if_exists(df, 'Province/State', 'Province_State')
            df = rename_if_exists(df, 'Country/Region', 'Country_Region')

            df = drop_if_exists(df, 'Last Update')
            df = drop_if_exists(df, 'Last_Update')
            df = drop_if_exists(df, 'Combined_Key')
            df = drop_if_exists(df, 'Incidence_Rate')
            df = drop_if_exists(df, 'Case-Fatality_Ratio')

            df = rename_or_create(df, 'Latitude', 'Lat')
            df = rename_or_create(df, 'Longitude', 'Long_')

            # ensure all CSV columns are ordered in the same way
            df = df.sort_index(axis=1)

            # set expected output data schema
            schema = {'Active': 'int64',
                      'Admin2': 'object',
                      'Confirmed': 'int64',
                      'Country_Region': 'object',
                      'Date': 'datetime64',
                      'Deaths': 'int64',
                      'FIPS': 'int64',
                      'Lat': 'float64',
                      'Long_': 'float64',
                      'Province_State': 'object',
                      'Recovered': 'int64'}

            # enforce data schema
            for col, dtype in schema.items():
                check_and_convert_dtype(df, col, dtype)
            
            # rewrite current csv
            df.to_csv(file, index=False)

if __name__ == "__main__":
    main()
