#################################################################
# File       : test_wellplate_from_ZEN.py
# Version    : 1.0
# Author     : czsrh
# Date       : 06.12.2018
# Institution : Carl Zeiss Microscopy GmbH
#
# Copyright(c) 2019 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

import pandas as pd
import wellplate_tools_pandas as wpt
import matplotlib.pyplot as plt
import argparse
import os
import re
import time
import numpy as np

parser = argparse.ArgumentParser(description='Read Filename and Parameters.')
parser.add_argument('-f', action="store", dest='filename')
parser.add_argument('-w', action="store", dest='platetype')
parser.add_argument('-p', action="store", dest='parameter')
parser.add_argument('-sp', action="store", dest='showplot')
parser.add_argument('-dpi', action="store", dest='dpi')


# get the arguments
args = parser.parse_args()
print('CSV Filename: ', args.filename)
print('PlateType: ', args.platetype)
print('Parameter to display: ', args.parameter)
print('DPI: ', args.dpi)

############################ TEST #########################################

# define the filenames
filename_single = args.filename
Nr, Nc = wpt.getrowandcolumn(args.platetype)

# check the used separator
sep = wpt.check_separator(filename_single)

# read the csv file
df_single = pd.read_csv(filename_single, sep=sep)

# get headers and number of measurement parameters
headers = df_single.head(0)

# define wellplate type (this has to be done by user)
platetype = args.platetype

print('Columns : ', df_single.columns)

# default number of non-measurement parameters
num_nonmp = 6

# list for renaming the parameters - please check your input CSV is the respective columns
# (might have different names) exits and if their order is reflected inside the parameterlist

parameterlist = ['ParentID',     # ParentID::ID of the parent!!I
                 'ID',           # ID::ID!!I
                 'WellID',       # ImageSceneContainerName::Image Scene Container Name
                 'RowID',        # ImageSceneRow::Image Scene Row Index!!I
                 'ColumnID',     # ImageSceneColumn::Image Scene Column Index!!I
                 'Index',        # Index::Index!!I
                 'Area',         # Area::Area!!R
                 'NucMeanDapi',  # IntensityMean_DAPI::Intensity Mean Value of channel 'DAPI'!!R
                 'NucMeanGFP',   # IntensityMean_EGFP::Intensity Mean Value of channel 'EGFP'!!R
                 'RingMeanGFP',  # CopyRingIntensityMean1::Ring Mean Intensity 1!!R
                 'RingArea']     # CopyRingArea::Ring Area!!R

"""
parameterlist = ['WellID',          # ImageSceneContainerName::Image Scene Container Name
                 'RowID',           # ImageSceneRow::Image Scene Row Index!!I
                 'ColumnID',        # ImageSceneColumn::Image Scene Column Index!!I
                 'ID',              # ID::ID!!I
                 'Index',           # Index::Index!!I
                 'MeanInt mCherry', # IntensityMean_mCher::Intensity Mean Value of channel 'mCher'!!R
                 'Area',            # Area::Area!!R
                 'Perimeter',       # Perimeter::Perimeter!!R
                 'Roundness',       # Roundness::Roundness!!R
                 'FeretRatio']      # FeretRatio::Feret Ratio!!R
"""

# rename columns
df_single = wpt.rename_columns(df_single, parameterlist)

# remove rows with units
df_single = wpt.remove_units(df_single)

# convert decimal separators
df_single = wpt.convert_dec_sep(df_single, num_nonmp)

# add another column and calculate the ratio between GFP in nucleus and GFP in Ring
df_single['Ratio'] = df_single['NucMeanGFP']/df_single['RingMeanGFP']

# replace infinity values with nan
df_single = df_single.replace([np.inf, -np.inf], np.nan)

num_param = len(df_single.columns) - num_nonmp
print('Number of Object Parameters: ', num_param)

# show part of dataframe
df_single[:6]

# use statistics --> we just calculate the mean values
# for a wells to be displayed inside the heatmaps.
# currently implemented are mean, median, min, max.
stf = 'mean'

# create a dictionary containing a dataframe for every measure parameters
# as a heatmap and a dictionary containing the mean values for all wells
# containing actual data points.
heatmap_dict, well_dict = wpt.fill_heatmaps(df_single, num_param, num_nonmp, Nr, Nc,
                                            statfunc=stf,
                                            showbar=True,
                                            verbose=False,
                                            wellID_key='WellID',
                                            rowID_key='RowID',
                                            colID_key='ColumnID')

# show all keys
heatmap_dict.keys()

# define parameters to display the heatmap
parameter2display = args.parameter

# check filename
parameter2display = re.sub(r'[\\/*!?:"<>|]', "", parameter2display)
hm = heatmap_dict[parameter2display]

# colormap='Blues'
colormap = 'YlGnBu'
# colormap ='RdBu_r'
# colormap = 'RdYlBu'

# show the heatmap for a single parameter
savename_single = wpt.showheatmap(hm, parameter2display,
                                  fontsize_title=16,
                                  fontsize_label=12,
                                  colormap=colormap,
                                  linecolor='black',
                                  linewidth=5.0,
                                  save=True,
                                  filename=filename_single,
                                  dpi=np.int(args.dpi))

plotgrid, deletelastplot = wpt.determine_plotgrid(num_param + 1, columns=2)


# show all heatmaps
savename_all = wpt.showheatmap_all(heatmap_dict, plotgrid,
                                   fontsize_title=10,
                                   fontsize_label=8,
                                   colormap=colormap,
                                   linecolor='black',
                                   linewidth=1.0,
                                   save=True,
                                   filename=filename_single,
                                   deletelast=deletelastplot,
                                   dpi=np.int(args.dpi))

# show all key = measure parameters for that dictionary
print(heatmap_dict.keys())

# modify the layout so the the axis labels and titles do not overlap
if args.showplot == 'True':
    plt.tight_layout()
    # show plots
    plt.show()

print('Exiting ...')
# time.sleep(5)
# os._exit(42)
