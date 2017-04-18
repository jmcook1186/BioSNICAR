import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import scipy as sci
from scipy import stats

## For irregularly shaped particles, the equivalent spherical diameter
## will be used. Here we use a volume-equivalent. Therefore, the 
## actual volume of the particle must be approxiumated from length,
## breadth and width.

length = 500 
breadth = 15
width = 1

vol = length * breadth * width
D = ((6/np.pi)*vol)
eqd = np.math.pow(D,(1/3))

## generate random numbers with specified mean and SD
## For a collection of aspherical particles, mu should = eqd and
## std should = std of measured lengths (as this dimension varies most
## in real population)

mean = 2000000 ## if irregular particles, use mean = eqd
std = 5


mean, std = mean, std # mean and standard deviation
s = np.random.normal(mean, std, 10000)

plt.plot(s)

## Check result by plotting histogram

plt.figure()
count, bins, ignored = plt.hist(s, 30, normed=True)
plt.plot(bins, 1/(std * np.sqrt(2 * np.pi)) * np.exp( - (bins - mean)**2 / (2 * std**2) ),linewidth=2, color='r')
plt.show()

## calculate median ##

median = np.median(s)


## Calculate Surface area weighted effective radius ##

## 1. convert to integers for binning
temp = []

for i in s: 
    temp.append(int(i))
temp = np.array(temp)

## count frequency of each integer in range min-max

unique, counts = np.unique(temp, return_counts=True)

unique = np.array(unique)
counts = np.array(counts)

p = unique*counts
pp = p^3
ppp = p^2

SurfWeightMean = np.sum(pp) / np.sum(ppp)

## Calculate geometric mean and geometric standard deviation after 
## normalising dataset to ensure no divide by zero error
for i in np.arange(0,len(temp),1):
    if temp[i] < 1:
        temp[i] = 1

geomean = sci.stats.mstats.gmean(temp)
geostd = np.std(np.log(temp))


## Print relevant values ##
print('Median = ', median)
print('Surface weighted mean effective radius = ', SurfWeightMean)
print('Geometric Mean', geomean)
print('Geometric STD = ', geostd)