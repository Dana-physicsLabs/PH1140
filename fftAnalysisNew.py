import numpy as np
import math
from matplotlib import pyplot as plt
from scipy import fft
from scipy import signal
import csv


# Generate an X array and a Y array using Numpy from your CSV file. You need to change the
# name of the csv file to whatever the name of your csv file is in order for this to work. If the header is longer
# than two lines then you can increase the number of "skip_header" to skip more of the data.
X_data = []
Y_data = []
X_data = np.genfromtxt('HOLDENUSETHIS.csv', usecols=0, skip_header=2, delimiter=',')
Y_data = np.genfromtxt('HOLDENUSETHIS.csv', skip_header=2, usecols=1,delimiter = ',')

# Create a dummy variable to skip over the dead zone in the oscilliscope data
# I am considering the dead zone to be any part of the data where the data is negative, as the active region contains no negative points
count = 0
for data in Y_data:
    if data < 0:
        count = count + 1

# Perform a fourier transform on the active region of the data
print(X_data[count:-1])
ycon = fft.fft(Y_data[count:-1])
ycon = np.abs(ycon)/(np.size(Y_data))
print(ycon)

# Create x data to match the size of the y data, regardless of how much y data we have eliminated due to the dead zone above
xrange = (np.size(Y_data)/2 + 1)
if isinstance(xrange, float) and xrange//2 == 0:
    xrange = int(xrange)
elif isinstance(xrange, float):
    xrange = int(xrange-.5)

# If your xrange does not work, you can try to use this code here instead and comment out the previous code
# xrange = np.size(ycon)
f = []
for i in range(int(xrange)):
     f.append(i*(1/.05))
fig, axs = plt.subplots(2)
fig.suptitle('Fourier Transform and Initial Graph')
axs[0].plot(f, ycon[0:int(xrange)])
axs[1].plot(X_data[count:-1], Y_data[count:-1])
# If your graph is not scaled well, you can try running this bad practice code below instead to fix it

# axs[1].plot(X_data[count+90:-1], Y_data[count+90:-1])

# plt.plot(f, ycon[0:int(xrange)])
peaks= signal.find_peaks(np.concatenate(([min(ycon)],ycon,[min(ycon)])), height=.01)
print(peaks)
peakArr = (peaks[1]["peak_heights"])
print(peakArr)

# Now we can do all of our fun data analysis in python right here as well!

C = 5
L = 8
R = 3
w = peakArr[0]*2*math.pi
Xc = 1/(w*C)
Xl = w*L
z = math.sqrt(R**2 * (Xl-Xc)**2)

print("The impedence, z, of this circuit is: " + str(z))


plt.show()