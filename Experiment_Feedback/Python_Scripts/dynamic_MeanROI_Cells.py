#################################################################
# File       : dynamic_MeanROI_Cells.py
# Version    : 1.0
# Author     : czmla
# Date       : 06.12.2018
# Insitution : Carl Zeiss Microscopy GmbH
#
#
# Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
#################################################################


import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import optparse
import numpy as np

# configure parsing option for command line usage
parser = optparse.OptionParser()

parser.add_option('-f', '--file',
                  action="store", dest="filename",
                  help="query string", default="No filename passed")

# read command line arguments
options, args = parser.parse_args()
savename = options.filename[:-4] + '.png'
print('Filename: ', options.filename)
print('Savename: ', savename)

# define plot layout
style.use('fivethirtyeight')
fig = plt.figure(figsize=(10, 8))
ax1 = fig.add_subplot(1, 1, 1)
plt.title('Ratio CH1/CH2')
plt.xlabel('Frame Nr.')
plt.ylabel('Ratio')


def animate(i):

    try:
        graph_data = np.genfromtxt(options.filename, dtype=float,
                                   invalid_raise=False, delimiter='\t')

        ax1.plot(graph_data[:, 0], graph_data[:, 1:], '-', lw=2)
        # save plot
        plt.savefig(savename)

    except:
        print('No file loaded')


ani = animation.FuncAnimation(fig, animate, interval=500, repeat=False)
plt.show()
