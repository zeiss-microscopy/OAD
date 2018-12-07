#################################################################
# File       : EF_ScratchAssay.py
# Version    : 1.0
# Author     : czmla
# Date       : 06.12.2018
# Insitution : Carl Zeiss Microscopy GmbH
#
#
# Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
# or: M1MALANG

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


def animate(i):

    try:
        graph_data = np.genfromtxt(options.filename, delimiter='\t')

        xs = graph_data[:, 0]  # get frame Nr.
        ys1 = graph_data[:, 1]  # get absolute Scratch area
        ys2 = graph_data[:, 2]  # get Sratch area in percent of Frame Area
        ys1_max = np.max(ys1, axis=0)  # get maximum Scratch Area
        ys1_percent = ys1/ys1_max*100  # normalize Scratch Area

        # labels and legend for plot
        ax1.clear()
        plt.title('Wound Healing Assay')
        plt.xlabel('Frame Nr.')
        plt.ylabel('Scratch Area [%]')
        ax1.plot(xs, ys1_percent, label='Percent of Initial Wound Area')
        ax1.plot(xs, ys2, label='Percent of Frame Area')
        ax1.legend(loc='upper right')

        # save plot
        plt.savefig(savename)

    except:
        print('No file loaded')


ani = animation.FuncAnimation(fig, animate, interval=1000, repeat=False)
plt.show()
