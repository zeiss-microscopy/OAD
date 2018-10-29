import numpy as np
import optparse
import matplotlib.pyplot as plt

# configure parsing option for command line usage
parser = optparse.OptionParser()

parser.add_option('-f', '--file',
    action="store", dest="filename",
    help="query string", default="spam")

# read command line arguments 
options, args = parser.parse_args()

print ('Filename:', options.filename)
savename = options.filename[:-4] + '.png'
print ('Savename: ', savename)


# load data
data = np.loadtxt(options.filename, delimiter='\t')
# create figure
figure = plt.figure(figsize=(12,6), dpi=100)
ax1 = figure.add_subplot(211)
ax2 = figure.add_subplot(212)

# create subplot 1
ax1.bar(data[:,0],data[:,1],width=0.8, bottom=0)
ax1.grid(True)
ax1.set_xlim([0,data[:,0].max() + 1])
ax1.set_ylim([0,data[:,1].max() + 0.5])
ax1.set_ylabel('Cells Active')

# create subplot 2
ax2.bar(data[:,0],data[:,2], width=0.8, bottom=0, color = 'red')
ax2.set_xlim([0,data[:,0].max() + 1])
ax2.set_ylim([data[:,2].min()-0.5,data[:,2].max()+0.5])
ax2.set_xlabel('Frame Number')
ax2.set_ylabel('Delta')
ax2.grid(True)
figure.subplots_adjust(left=0.10, bottom=0.12, right=0.95, top=0.95,wspace=0.10, hspace=0.20)

# save figure
plt.savefig(savename)

# show graph
plt.show()