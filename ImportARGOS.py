##---------------------------------------------------------------------
## ImportARGOS.py
##
## Description: Read in ARGOS formatted tracking data and create a line
##              feature class from the [filtered] tracking points.
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

# Set input variables:
inputFolder = sys.argv[1] #'V:/ARGOSTracking/Data/ARGOSData'
outputSR = sys.argv[2] #arcpy.SpatialReference(54002)
outputFC = sys.argv[3] #"V:/ARGOSTracking/Scratch/ARGOStrack.shp"

# Create list of files in folder:
inputFiles = os.listdir(inputFolder)

# Allow output to be overwritten:
arcpy.env.overwriteOutput = True

# Create an empty feature class:
outPath, outName = os.path.split(outputFC)
arcpy.management.CreateFeatureclass(outPath, outName, "POINT", "", "", "", outputSR)

# Add TagID, LC, IQ, and Date fields to the output feature class:
arcpy.management.AddField(outputFC,"TagID","LONG")
arcpy.management.AddField(outputFC,"LC","TEXT")
arcpy.management.AddField(outputFC,"Date","DATE")

# Create the insert cursor:
cur = arcpy.da.InsertCursor(outputFC,['Shape@','TagID','LC','Date'])

#%% Iterate Through All Lines in the Datafile

# Iterate through each input file:
for inputFile in inputFiles:
    
    # Skip the README.txt file:
    if inputFile == 'README.txt':
        continue
    
    # Provide status update:
    arcpy.AddMessage(f'Working on file {inputFile}')
    
    #Prepend inputfile with path:
    inputFile = os.path.join(inputFolder,inputFile)
    
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
            
            # Try to convert coordinates to numbers:
            try:
                # Convert raw coordinate strings to numbers:
                if obsLat[-1] == 'N':
                    obsLat = float(obsLat[:-1])
                else:
                    obsLat = float(obsLat[:-1]) * -1
                if obsLon[-1] == 'E':
                    obsLon = float(obsLon[:-1])
                else:
                    obsLon = float(obsLon[:-1]) * -1
                        
                # Construct a point object from the lat/long coordinates:
                obsPoint = arcpy.Point()
                obsPoint.X = obsLon
                obsPoint.Y = obsLat
                
                # Convert the point to a point geometry object with spatial reference:
                inputSR = arcpy.SpatialReference(4326)
                obsPointGeom = arcpy.PointGeometry(obsPoint,inputSR)
                
                # Create a feature object:
                feature = cur.insertRow((obsPointGeom,tagID,locationClass,date.replace(".","/") + " " + time))
            
            #Handle any error:
            except Exception as e:
                print(f"Error adding record {tagID} to the output: {e}")
            
        # Move to the next line so the while loop progresses:
        lineString = inputFileObj.readline()
        
    #Close the file object:
    inputFileObj.close()

#Delete the cursor object:
del cur