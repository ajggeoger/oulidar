# -*- coding: utf-8 -*-
"""
Initially created on Mon Jun 16 14:22 2014

A series of functions to help process .all datafiles from the Optech ALTM 3033
as delivered by the NERC ARSF

Inputs:
    folderIn = "/data/002_Projects/20140001_OULiDAR/01_Data/1_Incoming/datadownload/may08/"
    fileIn = 'Str_322.all' 
    coordsIn = [445000,206600,449000,210000]
    res = 4 #cell size
    
Assumptions: 
    A folder exists that contains multiple .all files for a single site on a 
    single date. The .all file should contain 9 columns. 

Functions:
    lidarFilt - splits every .all file in a folder into Last and First Pulse
    lidarSite - cuts out the area required based on LL/UR corner coords for a site
    lidarPlot - shows the density of points for specified grid size

@author: ajggeoger
"""

from os import listdir
import numpy as np
import matplotlib.pyplot as plt

def lidarFilt(foldername):

    # Set up output files for Last Pulse (LP) and First Pulse (FP)    
    outFileLP = open((foldername + 'filteredLP.txt'), 'a')
    outFileFP = open((foldername + 'filteredFP.txt'), 'a')
    #outFileDiff = open((foldername + 'diff_' + filename), 'a')
    #inList = open((foldername + filename), 'rU')
    
    c = 0
    for f in listdir(foldername):
        if f.endswith('.all'):
            inList = open((foldername + f), 'rU')
    
            while True:
                activeLine = inList.readline()
                
                if len(activeLine) == 90:
                    # split the file into LP and FP and count the points with 
                    # differences larget than 0.5 m
                    if (float(activeLine.split()[3]) - float(activeLine.split()[7])) >= abs(0.5):
                        c +=1

                    outFileLP.write(activeLine[18:53]+'\n')
                    outFileFP.write(activeLine[55:])
    
                if len(activeLine) == 88:
                    # catch those lines that have 2x whitespace missing
                    if (float(activeLine.split()[3]) - float(activeLine.split()[7])) >= abs(0.5):
                        c +=1

                    outFileLP.write(activeLine[16:51]+'\n')
                    outFileFP.write(activeLine[53:])
                    
                if len(activeLine) == 56:
                    # output lines with a single return
                    outFileLP.write(activeLine[18:53]+'\n')
                                 
                elif len(activeLine.split()) == 0:
                    break

                else:
                    pass

            inList.close()    

    print c # print number of records with large difference

    outFileLP.close()
    outFileFP.close()        
    #outFileDiff.close()        
        
    
def lidarSite(foldername, filename, coords):

    # Set output file
    outFile = open((foldername + 'Site' + filename), 'a')
    
    xmin = float(coords[0])
    ymin = float(coords[1])
    xmax = float(coords[2])
    ymax = float(coords[3])
    
    inList = open((foldername + filename), 'rU')
    
    # If data point is within the bounding box then write to file
    while True:
        activeLine = inList.readline()
        if xmin <= float(activeLine.split()[0]) <= xmax:
            if ymin <= float(activeLine.split()[1]) <= ymax:
                outFile.write(activeLine)
    
    inList.close()    
    outFile.close()
      
    
def lidarPlot(foldername, filename, coords, res):
    xmin = float(coords[0])
    ymin = float(coords[1])
    xmax = float(coords[2])
    ymax = float(coords[3])
    
    myData = np.genfromtxt((foldername + filename)) # create numpy array
    print myData.shape # confirm size
    
    # use a 2d histogram function to work out the number of points per cell
    # set up the bin (cell) size using the bounding coords and cell size
    xbin = np.asarray(range(int(xmin), int(xmax), res))
    ybin = np.asarray(range(int(ymin), int(ymax), res))
    
    xdata, ydata = myData[:,0], myData[:,1] # extract data
    grid, _, _ = np.histogram2d(xdata, ydata, bins=[xbin, ybin])
    
    # use imshow to plot the histogram result
    plt.imshow(grid, origin='lower', extent=[xmin, xmax, ymin, ymax], interpolation='nearest',alpha=0.75)    
    plt.colorbar()
    plt.xlabel('easting')
    plt.ylabel('northing')
    plt.show()
    
def main():
    pass
    
if __name__ == "__main__":
    print 'Need to import'