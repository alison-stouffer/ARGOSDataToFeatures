##---------------------------------------------------------------------
## ImportARGOS.py
##
## Description: Read in ARGOS formatted tracking data and create a line
##    feature class from the [filtered] tracking points
##
## Usage: ImportArgos <ARGOS folder> <Output feature class> 
##
## Created: Fall 2020
## Author: alison.stouffer@duke.edu (for ENV859)
##---------------------------------------------------------------------

#%% Import Packages

#Import modules:
import sys, os, arcpy

#%% Import Single File as File Object & Create Empty Feature Class

# Set input variables (hard-wired):
inputFile = 'V:/ARGOSTracking/Data/ARGOSData/1997dg.txt'
outputSR = arcpy.SpatialReference(54002)
outputFC = "V:/ARGOSTracking/Scratch/ARGOStrack.shp"

# Allow output to be overwritten:
arcpy.env.overwriteOutput = True

# Create an empty feature class:
outPath, outName = os.path.split(outputFC)
arcpy.management.CreateFeatureclass(outPath, outName, "POINT", "", "", "", outputSR)

# Add TagID, LC, IQ, and Date fields to the output feature class:
arcpy.management.AddField(outputFC,"TagID","LONG")
arcpy.management.AddField(outputFC,"LC","TEXT")
arcpy.management.AddField(outputFC,"Date","DATE")

#%% Iterate Through All Lines in the Datafile

# Open the ARGOS data file for reading:
inputFileObj = open(inputFile,'r')

# Get the first line of data:
lineString = inputFileObj.readline()

# Start the while loop:
while lineString:
    
    # Set code to run only if the line contains the string "Date: "
    if ("Date :" in lineString):
        
        # Parse the line into a list:
        lineData = lineString.split()
        
        # Extract attributes from the datum header line:
        tagID         = lineData[0]
        date          = lineData[3]
        time          = lineData[4]
        locationClass = lineData[7]
        
        # Extract location info from the next line:
        line2String = inputFileObj.readline()
        
        # Parse the line into a list:
        line2Data = line2String.split()
        
        # Extract the date we need to variables:
        obsLat = line2Data[2]
        obsLon= line2Data[5]
        
        # Print results to see how we're doing:
        print (tagID,"Lat:"+obsLat,"Long:"+obsLon, "Date: "+date, "Time: "+time, "LC:"+locationClass)
        
    # Move to the next line so the while loop progresses:
    lineString = inputFileObj.readline()
    
#Close the file object:
inputFileObj.close()