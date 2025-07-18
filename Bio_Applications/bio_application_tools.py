# coding: utf-8

import pandas as pd
import csv
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
# from ipy_progressbar import ProgressBar
import progressbar
try:
    from IPython.display import display
    from ipywidgets import FloatProgress
except:
    print('Could not import IPython.Display or ipywidgets')
import os


def get_well_all_parameters(df, wellid,
                            colname='all',
                            wellID_key='WellID',
                            rowID_key='RowID',
                            colID_key='ColumnID'):
    """
    Gets all or specific columns for specific well.
    If the colname was specified, only this specific column will be returned.

    :param df: original dataframe
    :param wellid: wellID, e.g. 'B4'
    :param colname: name of column(s) from the original dataframe to be extracted
    :return: new_df - new dataframe containing only data for a specific well
    """

    new_df = df.loc[df[wellID_key] == wellid]

    if colname != 'all':
        new_df = new_df[[wellID_key, rowID_key, colID_key, colname]]

    return new_df


def get_well_row(df, rowid, rowID_key='RowID'):
    """
    This function extracts all data based on the row index.

    :param df: original dataframe containing all wells
    :param rowid: index of row to be extracted
    :return: df_row - dataframe that only contains data for a specific row af a wellplate
    """

    rowindex = convert_row_index(rowid)
    df_row = df.loc[df[rowID_key] == rowindex]

    return df_row


def rename_columns(dfs, paramlist, verbose=False):

    for i in range(0, len(paramlist)):
        # rename the columns with measured parameters and correct types
        if verbose:
            print('Renamed : ', dfs.columns[i], ' to ', paramlist[i])
        try:
            dfs.rename(columns={dfs.columns[i]: paramlist[i]}, inplace=True)
        except:
            print('Column not find inside table for renaming. Doing nothing.')

    return dfs


def addWellinfoColumns(dataframe):

    # add WellID, RowID and ColumnID to the existing dataframe
    dataframe.insert(0, 'WellID', 'A1')
    dataframe.insert(1, 'RowID', 1)
    dataframe.insert(2, 'ColumnID', 1)

    return dataframe


def remove_units(df):

    # remove units from table
    df.drop([0], inplace=True)

    return df


def convert_dec_sep(df, np):

    for id in range(np, len(df.columns)):
        #print('Index: ', id)
        try:
            df.iloc[:, id] = df.iloc[:, id].str.replace(',', '.').astype('float')
        except:
            print('No correction of types possible for column: ', df.columns[id])

    return df


def check_separator(csvfile):

    reader = pd.read_csv(csvfile, sep=None, engine='python', iterator=True)
    sep = reader._engine.data.dialect.delimiter
    reader.close()

    return sep


def determine_plotgrid(num_parameter, columns=2):

    if np.mod(num_parameter, columns) == 0:
        plotrows = np.int(num_parameter /columns)
        empty = False
    if np.mod(num_parameter, columns) == 1:
        plotrows = np.int(num_parameter / columns) + 1
        empty = True

    plotgrid = [plotrows, columns]

    return plotgrid, empty
    
    
def get_csvdata(filename, num_nonmp=2):

    # check the used separator
    sep = check_separator(filename)

    # read the CSV table containing all the single object data
    df = pd.read_csv(filename, sep=sep)

    # get headers and number of measurement parameters
    headers = df.head(0)
    
    # remove rows with units from datafrane
    df = remove_units(df)

    # convert decimal separators to point "."
    df = convert_dec_sep(df, num_nonmp)
    
    return df, headers, sep

