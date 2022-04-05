# The first thing we need to do is import the proper packages for our work.
# The packages we need are scipy, matplotlib.pyplot, and numpy
# Let's go ahead and import those
import scipy as sci
import matplotlib.pyplot as plt
import numpy as np

# The next thing we need to do is generate arrays in python from our csv file of the data from LoggerPro. We can use
# numpy to import this data. In this function, we first input the file name we want. Then we use "usecols" to tell
# the code what columns of the data to use. "skip_header" tells the code how much header is in this data and how much
# it should skip. There's 1 header box in here, so we'll use 1 for this value. delimiter tells the code where to say
# "this is a new value" since we're using  a csv, or comma separated value, file, we need this to be a comma

X_data = np.genfromtxt('HappyRyanNoises.csv', usecols=0, skip_header=1, delimiter=',')
Y_data = np.genfromtxt('HappyRyanNoises.csv', usecols=1, skip_header=1, delimiter=',')

# Real quick, we can double check that this did grab the right information in the right places. We can print out
# these arrays. Typically, I would use the debugger to check this, but this is quick and easy too.

print(X_data, Y_data)
yi = np.arange(len(Y_data))

# The other potential problem we can have is null data points, which will cause our entire fft to fail. To remove
# those, we can find all the null data points and try to interpolate what their values would have been. Not a great
# fix, but it works.

mask = np.isfinite(Y_data)
yfiltered = np.interp(yi, yi[mask], Y_data[mask])


# Now that our data is properly prepared, we can start our fft analysis. The first thing we need to do is take the
# fft of the data we care about. Our X_data is just time in steps of .05 each time, which is not very interesting and
# does not oscillate with time. Our Y_data however, does oscillate with time! So we want to take the fft of the y
# data that we just cleaned up. We can get the fft with a simple:

yTrans = sci.fft.fft(yfiltered)

# However, fft arrays often have the terrible annoyance of complex, negative, and otherwise unsavory values. We can
# fix that though. A quick absolute value should settle everything. After that, we can print our fft array to make
# sure it all worked!
yTrans = np.abs(yTrans)
print(yTrans)
# The variable "yTrans" is now the fast fourier transform of our Y_data. We will run into a problem if we try to
# graph this immediately though. We can illustrate the problem clearly here:

print(np.size(yTrans), np.size(X_data))

# Our Y data is in the frequency space. This is great. But our X data is still in time space. Luckily for us,
# we have a function that can fix this. The function "fftfreq" will convert our time steps into frequency steps.
# These new frequency steps will be compatible with our fourier transformed values. First we want to set "N" to be
# our sample size. We have evenly distributed data that takes steps of .05 each time. We can get our sample size by
# just taking the size of our X_data

N = np.size(X_data)

# And we can set "T" as our sample spacing. Again, from logger pro we know this is distributed evenly in steps of .05

T = .05

# Using these, we can make sure that our X and Y have the same dimensions with another fft package miracle. We want
# to transform our X axis into a range of frequencies that align with our Y data. This frequency range is dependent
# only on our number of samples, and our sampling frequency. We can finally use "fftfreq" to generate these values

xTrans = sci.fft.fftfreq(N, T)[:N//2]

# If you are curious why "[:N//2]" is included in this code, it is to cut off the data into only half of the value we
# generate. The meaning of the expression is "take this array, but only use its values from 0 to one half of N." The
# "//" means "integer divide" or "divide and lose the remainder so I get an integer at the end", which means we can
# use it to get an index in the array. The reason we half the expression is because the fourier transform mirrors
# itself across the x axis. If all values of the fourier transform are real, then this "mirror image" creates a
# perfectly symmetric copy of the other side. For complex values however, this "mirror image" is not a mirror at all,
# and the two sides of the transform can take different values. We will be dealing only in real numbers, and thus our
# "mirror image" would give us no additional information, so we exclude it. Including it can also compound the
# artefacts of the fourier transform that naturally arise in the data. We'll see another one of those later on.



# Finally, we can plot our wonderful creation on a plot using pyplot. In this case, I want to plot two graphs at once.
# I will be using pyplot's "subplot" method to do this

fig, axs = plt.subplots(2)
fig.suptitle('Fourier Transform and Initial Graph')

# Now right here comes a fun part. Try removing the number 5 from the code below and running it. You will (often) see
# a HUGE spike at a frequency of 0 that dwarfs all the rest of your data. But...a frequency of 0 is impossible. Think
# about the units of frequency, 1/s. a frequency of zero means it takes infinite seconds for this to oscillate. Which
# is clearly not the case. Don't worry though. I mentioned artifacts of the transform before, and this is one of
# them. If we skip past this artifact we can get a cleaner graph. If you run this code with the [5:] and [5:N//2],
# you'll get a fantastic graph of your frequencies and their relative amplitudes!
axs[0].plot(xTrans[5:], yTrans[5:N//2])
axs[1].plot(X_data, Y_data)
plt.show()

# If you are wondering how to interpret the graph you now have before you, do not worry. It's a confusing set of axes.
# Your x-axis is the frequency axis. You should be able to pick out a peak corresponding to either your resonance 
# frequency or your driving frequency on there. That should help you orient yourself on the x-axis.

# Your y-axis is the relative amplitudes of the frequencies present. Taller bar means more prevalent frequency essentially.
# I say relative amplitude because I have not run through the normalization of our y data for this fft. What that means is that
# the actual values of amplitude should not be compared to anything other than values of amplitude from the same graph. 
# Normalization is just me making sure that the transformation the correct values of the amplitudes.
# Consider it extra credit if you modify this code and normalize your amplitude values.

# There are obviously some limitations to fft analysis. For one, the fft does not identify the sources of the
# frequencies you identify. All it does is tell you what frequencies exist. This is less than ideal if you have two
# very similar frequencies and have difficulty knowing what is from what. However, it is also a very powerful tool
# used all across the world of signal processing, and yes, the whole world of oscillations and waves

# I hope you had fun on the wild ride that is my fft code.
# If you have any questions, my name is Holden Snyder and my email is hlsnyder@wpi.edu
# You can also contact Ryan Hanna or Shannon Song at rjhanna@wpi.edu and smsong@wpi.edu

# Have a fantastic day everyone! Happy analysis!

