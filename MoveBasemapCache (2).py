#-------------------------------------------------------------------------------
# Name:        MoveBasemapCache.py
# Purpose:     Move the cache from VMGISDEV04 to VMGIDPROD04
# Author:      MGrue
#
# Created:     03/15/2016
# Copyright:   (c) MGrue 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#import arcpy
import logging, smtplib, shutil, zipfile
from datetime import datetime
from os import rename
from os import remove
from os import path
from time import sleep
isError = False

#------------------------------------------------------------------------------
                # Set variables that could change

#Below are the locations for (1) the location you want to put the zip file
#This location is just one folder level above the file you want to zip
#(2) The location of the folder you want to zip
outputZipLoc = r"\\vmgisdev04\D$\arcgisserver\directories\arcgiscache\PUD_CompassGIS_PUD_Basemap_Cache_Publish"
inputZipFile = outputZipLoc + r"\PUD GIS Basemap"


#Below are the locations (1) where you want the new zip file to be placed
#(2) where you want the zip file to be unzipped to (with a _NEW appended to it)
#(3) the path / name of the current cache file on prod that you are going to
#    rename to _OLD to act as a backup
newZipLoc =    r"\\vmgisprod04\D$\arcgisserver\directories\arcgiscache\PUD_CompassGIS_PUD_Basemap_Cache\CacheFromDev.zip"
unZipLoc =     r"\\vmgisprod04\D$\arcgisserver\directories\arcgiscache\PUD_CompassGIS_PUD_Basemap_Cache\CacheFromDev"
oldCacheFile = r"\\vmgisprod04\D$\arcgisserver\directories\arcgiscache\PUD_CompassGIS_PUD_Basemap_Cache\PUD GIS Basemap"

#Where you want the log file to be placed
fileLog = r'\\vmgisprod04\e$\Data\PUD_CompassGIS\LocalExtractedFGDBs\Scripts\MoveBasemapCache.log'

#------------------------------------------------------------------------------

#Set up logger.  If you need to debug, set the level=logging.INFO to logging.DEBUG
logging.basicConfig(filename = fileLog, level=logging.INFO)

#Header for the log file
logging.info('--------------------------------------------------------------')
logging.info('                  ' + str(datetime.now()))
logging.info('                Running MoveBasemapCache.py')
logging.info('--------------------------------------------------------------')

#Zip the inputZipFile and locate it to outputZipLoc
try:
    logging.debug('Starting to zip file at:\n ' + inputZipFile + '\nTO\n' + outputZipLoc)
    shutil.make_archive(outputZipLoc, 'zip', inputZipFile)
    logging.info('FINISHED Zip the inputZipFile and locate it to outputZipLoc')
except Exception as e:
    logging.error('Zip the inputZipFile and locate it to outputZipLoc FAILED')
    logging.error('Error: ' + str(e))
    isError = True

#Now move the zipped file from outputZipLoc to newZipLoc
if isError == False:
    try:
        logging.debug('Starting to copy file at:\n ' + outputZipLoc + '\nTO\n ' + newZipLoc)
        src = outputZipLoc + '.zip'
        dst = newZipLoc
        shutil.copyfile(src, dst)
        logging.info('FINISHED Now move the zipped file from outputZipLoc to newZipLoc')
    except Exception as e:
        logging.error('Now move the zipped file from outputZipLoc to newZipLoc FAILED')
        logging.error('Error: ' + str(e))
        isError = True

#If the move was successful:  Unzip the newly moved cache
if isError == False:
    try:
        with zipfile.ZipFile(newZipLoc, 'r') as z:
            z.extractall(unZipLoc)
            logging.info('FINISHED If the move was successful:  Unzip the newly moved cache')
    except Exception as e:
        logging.error('If the move was successful:  Unzip the newly moved cache FAILED')
        logging.error('Error: ' + str(e))
        isError = True

#If unzip was successful: Rename the old Cache file
if isError == False:
    try:
        if path.exists(oldCacheFile + '_OLD'):
            #This will execute if there is a current cache file with the suffix "_OLD"
            shutil.rmtree(oldCacheFile + '_OLD')
            logging.debug('FINISHED removing the old cache file from the last script run')
        else:
            logging.debug('There was no existing "_OLD" folder to remove')
        #This will now rename the existing cache file to "_OLD"
        #and the new file to the correct cache file name
        rename(oldCacheFile, oldCacheFile + '_OLD')
        #Now rename the new Cache file to the correct name
        sleep(0.5)
        rename(unZipLoc, oldCacheFile)
        logging.debug('FINISHED If unzip was successful: Rename the old Cache file')
    except Exception as e:
        logging.error('If unzip was successful: Rename the old Cache file  FAILED')
        logging.error('Error: ' + str(e))
        isError = True

#If rename was successful: remove the zip files
if isError == False:
    try:
        remove(outputZipLoc + '.zip')
        remove(newZipLoc)
        logging.info('FINISHED If rename was successful: remove the zip files')
    except Exception as e:
        logging.error('If rename was successful: remove the zip files FAILED')
        logging.error('Error: ' + str(e))
        isError = True


# Setup Email notification
try:
    sender = 'vmgisprod04@sannet.gov'
    receivers = ['mike@quarticsolutions.com'] #'chris@quarticsolutions.com','tyler@quarticsolutions.com','drew@quarticsolutions.com', 'rob@quarticsolutions.com', 'timo@quarticsolutions.com']

    if isError == False:
        Subject = "MoveBasemapCache.py ran successfully"
        EmailText = ("MoveBasemapCache.py ran successfully")
    else:
        Subject = "Error with MoveBasemapCache.py"
        EmailText = ("Please check log at:\n" + fileLog + '\n for explanation.')
except Exception as e:
        logging.error('ERROR: Email not sent!')
        logging.error('ERROR: ' + str(e))

message = """\
From: %s
To: %s
Subject: %s

%s
""" % (sender, ", ".join(receivers), Subject, EmailText)

try:
    smtpObj = smtplib.SMTP('smtp-out.sannet.gov')
    smtpObj.sendmail(sender,receivers, message)
except Exception as e:
    logging.error('Email NOT sent!' + str(e))


logging.info('--------------------------------------------------------------')
logging.info('                  ' + str(datetime.now()))
logging.info('                Finished MoveBasemapCache.py')
logging.info('--------------------------------------------------------------')