#-------------------------------------------------------------------------------
# Name:        MoveLocatorRegions.py
# Purpose:     Move the LocatorRegions FC from the City's Y:Drive to ATLAS's
#               PUD_MISC Feature Dataset
# Author:      MGrue
#
# Created:     02/03/2016
# Copyright:   (c) MGrue 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy, logging, smtplib
from datetime import datetime
arcpy.env.overwriteOutput = True
isError = False

#------------------------------------------------------------------------------
                # Set variables that could change
locFGDB = r'\\ad\pubutil\PUMGMT\zPUMGMT_PublicShare\StrategicPrograms\AssetManagement\CompassGIS\Stage3\DataToQuartic\LocatorRegions.gdb'
nameOfFC = 'pudLocatorRegions'
outputLoc = r'C:\Users\mgrue\Quartic\Scripts\Tests\LocatorRegions.gdb\pudLocatorRegions'
#Below is to test with ATLASDEV
##outputLoc = r'Database Connections\zAtlasdev.sde (City ADMIN).sde\SDW.CITY.PUD_MISC\sdw.CITY.pudLocatorRegions'

#This list is all of the fields that should be in the new pudLocatorRegions layer
shouldContainFields = ['OBJECTID','Shape', 'sdw_CITY_pudLocatorRegions_AREA',
'PERIMETER', 'GRPH', 'PAGE', 'PAGEXT', 'ROW_', 'COLUMN_',
'DISPLAYCLA', 'PRODUCTARE', 'FIPS_CO', 'TBM', 'Shape_STArea__',
'Shape_STLength__', 'Radio_Number', 'Crew_name', 'Shape_Length', 'Shape_Area']
#------------------------------------------------------------------------------

#Set up logger.  If you need to debug, set the level=logging.INFO to logging.DEBUG
fileLog = r'C:\Users\mgrue\Quartic\Scripts\MoveFiles\MoveLocatorRegions.log'
logging.basicConfig(filename = fileLog, level=logging.DEBUG)

#Header for the log file
logging.info('--------------------------------------------------------------')
logging.info('                  ' + str(datetime.now()))
logging.info('                Running MoveLocatorRegions.py')
logging.info('--------------------------------------------------------------')

#Establish connection and test to make sure the field name on the Y:Drive
#is correct
logging.info('Establish connection to make sure the field name on the Y:Drive is correct')
arcpy.env.workspace = locFGDB
newFC = arcpy.ListFeatureClasses(nameOfFC)[0]
if newFC != nameOfFC:
    logging.error(newFC + ' does not equal nameOfFC' + nameOfFC)
    isError = True
else:
    logging.info(newFC + ' equals ' + nameOfFC)

if isError == False:
    #Test to make sure newFC has the correct field names
    logging.info('Testing to make sure newFC has the correct field names')
    newFieldNames = [f.name for f in arcpy.ListFields(newFC)]
    i = 0
    while (isError == False and i < len(shouldContainFields)):
        if shouldContainFields[i] in newFieldNames:
            i += 1
        else:
            logging.error('There was a shouldContainField that wasn\'t in the newFC')
            isError = True

if isError == False:
    logging.info('Correct fields in newFC, beginning to copy ' + newFC + ' to ' +
    outputLoc)
    #Copy features over from locFGDB
    arcpy.CopyFeatures_management(nameOfFC, outputLoc)
    logging.info('Copy Features completed')

logging.info('--------------------------------------------------------------')
logging.info('                  ' + str(datetime.now()))
logging.info('                Finished MoveLocatorRegions.py')
logging.info('--------------------------------------------------------------')