import os
env = os.environ
env.update({'QT_API':'pyside'})

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import optparse
import numpy as np
import time
    
##############################  
# configure parsing option for command line usage
##############################

parser = optparse.OptionParser()
    
parser.add_option('-f', '--file',
action="store", dest="filename",
help="query string", default="No filename passed.")
    
parser.add_option('-c', '--columns',
action="store", dest="columns",
help="query string", default="No number of columns passed.")
    
parser.add_option('-r', '--rows',
action="store", dest="rows",
help="query string", default="No number of rows passed.")

parser.add_option('-b', '--block',
    action="store", dest="block",
    help="set to False for non interactive behaviour", default="True")

# read command line arguments 
options, args = parser.parse_args()     
savename = options.filename[:-4] + '.png'
           
print ('Filename: ', options.filename)
print ('Savename: ', savename)

block = True
if options.block == 'False':
	block = False

# read in cell numbers
Nr = int(options.rows)      
Nc = int(options.columns)
#print ("Number of Wells: ", Nr*Nc)  

##############################
# define plot layout
##############################

fig = plt.figure(figsize=(6,4)) 
ax1 = fig.add_subplot(1,1,1)

posX = np.arange(0,Nc,1) #position of labels for plot
posY = np.arange(0,Nr,1) #position of labels for plot


LabelX = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]       
LabelY = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P'] 
       
labelx = LabelX[0:Nc]
labely = LabelY[0:Nr]

#print ("Label X: ",labelx)
#print ("Label Y: ",labely)

    
##############################
# Main part
##############################

def animate(i):          

    try: 
                        
        datain = np.genfromtxt(options.filename, delimiter='\t', usecols=(1,2,3))
        well = np.zeros([Nr, Nc]) # create a new array of Size Nr x Nc filled with zeros
                
        for j in range(0, datain.shape[0]):  
        
            # read entries        
            cn = datain[j,0]
            col = datain[j,1]-1 # numpy is zero-based ...   
            row = datain[j,2]-1
            # update well array at the correct position
            well[int(row), int(col)] = cn
            cn_max = np.max(datain[:,0]) 
            cn_min = np.min(datain[:,0])             
        
        fig.clear() 
        plt.title('Cell Count per Well') #plottitle              
        # do the plot
        cax = plt.imshow(well, cmap='plasma', interpolation='nearest')
        # define and plot colorbar                            
        plt.clim(cn_min, cn_max)
        cbar = plt.colorbar(cax, ticks=[cn_min, round((cn_min+cn_max)/2), cn_max], shrink = 0.7) 
        # plot ticks on positions
        plt.xticks(posX,labelx) 
        plt.yticks(posY,labely)

        # figure cannot be saved in first iteration.
		# if all data is available in the first iteration, nevertheless do one more with the same data
		# to be able to save the figure.
        if i != 0:
			# if last well is reached, save figure
            if datain.shape[0] == Nr * Nc:
                fig.savefig(savename)
                if block == False:
                    plt.close()

    except:
        print('No file loaded')

ani = animation.FuncAnimation(fig, animate, interval=500, repeat=False)
plt.show()

