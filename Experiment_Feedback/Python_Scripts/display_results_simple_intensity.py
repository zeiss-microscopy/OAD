# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 11:26:27 2012

@author:Sebastian Rhode
"""
import numpy as np #scientific computing with Python
import optparse   #library for parsing command-line options
import matplotlib.pyplot as plt #Python 2D plotting library
import matplotlib.gridspec as gridspec

# configure parsing option for command line usage
# create an OptionParser instance
parser = optparse.OptionParser()

# define parsing options
parser.add_option('-f', '--file',
    action="store", dest="filename",
    help="query string", default="No filename passed")

# read command line arguments 
options, args = parser.parse_args()

savename = options.filename[:-4] + '.png'
print('Filename: ', options.filename)
print('Savename: ', savename)

# Load data from the textfile, specify delimiter
data = np.loadtxt(options.filename, delimiter='\t')

# create figure
figure = plt.figure(figsize=(10,5), dpi=100) #top level container for all plot elements
gs = gridspec.GridSpec(nrows=2, ncols=2, height_ratios=[1, 1])
ax1 = figure.add_subplot(121)
ax2 = figure.add_subplot(122)


# create subplot 1
ax1.plot(data[:,0],data[:,1],'bo-', lw=2, label='Cell Count')
ax1.grid(True)
ax1.set_xlim([data[0,0]-1,data[-1,0]+1]) # limit X and Y axis
ax1.set_xlabel('Timepoint')
ax1.set_ylabel('DAPI Mean Intensity')

# create subplot 2
ax2.bar(data[:,0],data[:,1],width=0.7, bottom=0)
ax2.grid(True)
ax2.set_xlim([data[0,0]-1,data[-1,0]+1])
ax2.set_xlabel('Timepoint')



# adjust subplots
figure.subplots_adjust(left=0.10, bottom=0.12, right=0.95, top=0.95,wspace=0.20, hspace=0.40)

# save figure
plt.savefig(savename)

# show graph
plt.show()
