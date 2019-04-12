# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 15:23:07 2018

@author: M1MALANG
"""
import os
env = os.environ
env.update({'QT_API':'pyside'})

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

parser.add_option('-b', '--block',
    action="store", dest="block",
    help="set to False for non interactive behaviour", default="True")

# read command line arguments 
options, args = parser.parse_args()
savename = options.filename[:-4] + '.png'
print('Filename: ', options.filename)
print('Savename: ', savename)

block = True
if options.block == 'False':
	block = False

# define plot layout
style.use('fivethirtyeight')
fig = plt.figure(figsize=(10,8))
ax1 = fig.add_subplot(1,1,1)  
plt.title('Ratio CH1/CH2')
plt.xlabel('Frame Nr.')
plt.ylabel('Ratio')  

    
def animate(i):
    
    try:       
        graph_data = np.genfromtxt(options.filename, dtype=float, invalid_raise=False, delimiter='\t')          
        ax1.plot(graph_data[:,0], graph_data[:,1:], '-', lw=2)                                
        #save plot
        plt.savefig(savename)
        if block == False:
            plt.close()
    except:
        print('No file loaded')
ani = animation.FuncAnimation(fig, animate, interval=500, repeat=False)
plt.show()