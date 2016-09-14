"""-----------------------------------------------------------------------------
Name:        CopyATLASDataToLocalFGDB.py
Purpose:     This script takes data from ATLAS and brings it to a local FGDB
named 'sdw_new.gdb'
The local FGDB is consumed by the CompassGIS_StandAlone.mxd.  There is a
StandAlone.bat file that calls this script and passes the parameter to the
jobDirectory variable in order to tell the script where the FGDB should be
created.  The bat file will then call the CreateGeometricNetworks_ATLAS_schema.py
which will create the geometric networks on the data that is copied by this
script.

As it copies the Feature Classes from ATLAS, if the FC will be in a geometric
network, the script will add the ENABLED field that the geometric network needs.
It will also calculate the ENABLED field based off of the FNCTNL_CD found
in the data.
Once all of the data is downloaded, it will rename the current ?sdw.gdb? to
?sdw_old.gdb? and rename the new 'sdw_new.gdb' to ?sdw.gdb?.  This is so when the
CompassGIS_StandAlone.mxd is next opened up, it will look for the ?sdw.gdb?
that has the new data in it.

Author:      MGrue

Created:     22/08/2016
Copyright:   (c) MGrue 2016
Licence:     <your licence>
"""
#-------------------------------------------------------------------------------

import arcpy, logging, os, shutil
from datetime import datetime
arcpy.env.overwriteOutput = True


#-------------------------------------------------------------------------------
#  Variables that will change when script is moved from one computer to another

jobDirectory = arcpy.GetParameterAsText(0)

name_of_AD_connection_to_ATLAS = arcpy.GetParameterAsText(1)

#-------------------------------------------------------------------------------
#                      Set Variables that probably wont change
#                  (as long as the file structure for the StandAlone
#                       folder in the Y: Drive doesn't change)

#  Where do you want the log file to go???
fileLog = jobDirectory + '\\' + r'Maintenance\Logs\CopyATLASDataToLocalFGDB.log'

#  Which folder do you want the FGDB to go into???
currentData_file_loc = jobDirectory + '\\' + 'Data'

#  Where is the prj file you want to use to create the feature datasets???
#It should be in StatePlaneVI
prjFile = jobDirectory + '\\' + r'Maintenance\Scripts\ProjectionFile_StatePlaneVI\StatePlaneVI.prj'

#  What is your Database Connection file to atlas named???
database_connection_file = 'Database Connections' + '\\' + name_of_AD_connection_to_ATLAS

#Name and location of new FGDB
newFGDB = 'sdw_new.gdb'
newFGDB_loc = currentData_file_loc + '\\' + newFGDB

success = True

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                Set Variables that may change if we want to change the:
#                    feature datasets
#                    feature classes that will get copied
#                    feature classes that will be in a geometric network


#The order of the two below lists is important since they will both be
#controlled with an index 'i'
FGDB_fds = [          'WATER',          'RWATER',          'SEWER',          'GRID',           'SANGIS']
ATLAS_fds = ['SDW.CITY.WATER', 'SDW.CITY.RWATER', 'SDW.CITY.SEWER', 'SDW.CITY.GRID',  'SDW.CITY.SANGIS']

#Below is a list of all the feature classes that were in the original FGDB
#that I tried to get from ATLAS.
#NOTE: Any of the uncapitalized FC's are NOT in ATLAS and couldn't be coppied
#over.  If we need these layers on the StandAlone.mxd, then the City should
#put them on ATLAS.

WATER_FC = ['W_AIR_VALVE', 'W_AQUEDUCT', 'W_BACK_FLOW', 'W_BLOW_OFF', 'W_CAP',
'W_CHANNEL', 'W_DAM', 'W_DISTRIBUTION_RESERVOIR', 'W_DIVERSION_CONNECTION',
'W_FILTRATION_PLANT', 'W_FLUME', 'W_HGL', 'W_HYDRANT',
'W_HYDRANT_REMOVED_ABANDONED', 'W_METER', 'W_OUTLET_TOWER', 'W_PIPE',
'W_PITOT_TAP', 'W_PUMP', 'W_PUMP_STATION', 'W_RAW_WATER_RESERVOIR', 'W_REDUCER',
'W_REGULATING_RESERVOIR', 'W_REGULATOR_REMOVED_ABANDONED', 'W_REGULATOR_VALVE',
'W_SAMPLE_LOCATION', 'W_SERVICE', 'W_STATION', 'W_STATIONP', 'W_STBL', 'W_TANK',
'W_TUNNEL', 'W_VALVE', 'W_VALVE_REMOVED_ABANDONED', 'W_WEIR', 'W_WELL']

RWATER_FC = ['RWTR_AIR_VALVE', 'RWTR_BACK_FLOW', 'RWTR_BLOW_OFF', 'RWTR_CAP',
'RWTR_HGL', 'RWTR_METER', 'RWTR_PIPE', 'RWTR_PUMP', 'RWTR_PUMP_STATION',
'RWTR_REDUCER', 'RWTR_REGULATOR_VALVE', 'RWTR_SAMPLE_LOCATION', 'RWTR_SERVICE',
'RWTR_STABILIZING_STRUCTURE', 'RWTR_STATION', 'RWTR_STATIONP', 'RWTR_TANK',
'RWTR_VALVE']

SEWER_FC = ['S_AIR_VALVE', 'S_BLOW_OFF', 'S_CLEAN_OUT', 'S_CYN_ACCESS_PATHS',
'S_LATERAL', 'S_LATERAL_REMOVED_ABANDONED', 'S_MAIN', 'S_MAIN_FLOWARROW',
'S_MAIN_REMOVED_ABANDONED', 'S_MANHOLE', 'S_MANHOLE_REMOVED_ABANDONED',
'S_METER', 'S_PLUG', 'S_PUMP', 'S_PUMPSTA', 'S_PUMPSTN', 'S_REDUCER',
'S_STATION', 'S_STBL', 'S_TANK', 'S_TREATMENT_PLANT', 'S_VALVE']

GRID_FC = ['FIELD_BOOK']

SANGIS_FC = ['ADDRAPN', 'AIR_RUNWAYS', 'CULTURE_POINTS_TB',
'FACILITIES_MILITARY', 'FIRE_STATION', 'HOSPITAL', 'HYD_LAKE', 'HYD_RIVERS',
'HYD_STREAMS_SG', 'INDIAN_RESERVATIONS', 'JUR_MUNICIPAL', 'JUR_VICINITY',
'LIBRARY', 'NTL_FOREST', 'PARCELS_ALL', 'PARKS_ACTIVE_USE', 'PARKS_CN',
'RAILROAD', 'REC_CENTER_CN', 'RIGHT_OF_WAY', 'RIGHT_OF_WAY_LINE', 'ROADS_ALL',
'ROADS_MAJOR', 'ROAD_TB', 'SCHOOL', 'WATER_INDEX', 'detail_inset_extent',
'easement', 'gis_fuel_line_route', 'gis_tc_conduit_route',
'gis_tc_station_location', 'gis_ws_cp_anode_bed_location',
'gis_ws_cp_rectifier_location', 'index_grid_line_extent',
'index_grid_quadrant_extent', 'ws_cathodic_site_current_recl_location',
'ws_cathodic_site_current_sewer_location',
'ws_cathodic_site_current_water_location', 'ws_cp_test_station', 'ws_cp_wire',
'ws_jumpover']

#Below is a list of all of the feature classes that will participate in the
#Geometric network.  We will want to create a field ENABLED and populate it
#based on the FNCTNL_CD field.
in_geom_net = ['RWTR_CAP', 'RWTR_METER', 'RWTR_PIPE', 'RWTR_PUMP',
'RWTR_REDUCER', 'RWTR_REGULATOR_VALVE', 'RWTR_SERVICE', 'RWTR_VALVE',
'S_CLEAN_OUT', 'S_LATERAL', 'S_MAIN', 'S_MANHOLE', 'S_METER', 'S_PLUG',
'S_PUMP', 'S_REDUCER', 'S_VALVE', 'W_AQUEDUCT', 'W_CAP', 'W_CHANNEL', 'W_FLUME',
'W_HYDRANT','W_METER', 'W_PIPE', 'W_PUMP', 'W_REDUCER', 'W_REGULATOR_VALVE',
'W_SERVICE', 'W_VALVE']

#-------------------------------------------------------------------------------
#                                   Set up logger
#If you need to debug, set the level=logging.INFO to logging.DEBUG

logging.basicConfig(filename = fileLog, level=logging.DEBUG)

#Header for the log file
logging.info('--------------------------------------------------------------' )
logging.info('                  ' + str(datetime.now()))
logging.info('                Running CopyATLASDataToLocalFGDB.py')
logging.info('--------------------------------------------------------------' )


#-------------------------------------------------------------------------------
# ************************ START DEFINE FUNCTIONS  ****************************
#-------------------------------------------------------------------------------
#                            Create 'sdw_new.gdb'

def createNewFGDB():
    print 'Creating FGDB: ' + '"' + newFGDB + '"' + ' at: ' + currentData_file_loc + '\n'
    logging.info('Creating FGDB: ' + '"' + newFGDB + '"' + ' at: ' + currentData_file_loc + '\n')
    arcpy.CreateFileGDB_management(currentData_file_loc, newFGDB , "CURRENT")

    #Create Feature Datasets:  RWATER, SEWER, WATER, GRID, SANGIS
    for fd in FGDB_fds:
        print 'Creating Feature Dataset: ' + fd
        logging.info('Creating Feature Dataset: ' + fd)
        out_dataset_path = newFGDB_loc
        out_name = fd
        spatial_reference = prjFile

        arcpy.CreateFeatureDataset_management(out_dataset_path, out_name, spatial_reference)

    print '\n'
    logging.info('\n')
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                Copy the features from ATLAS to the local FGDB
def copyFeatures(fc, fc_truncate):

    print 'Copying: ' + fc + ' to ' + FGDB_fds[i] + ' feature dataset.'
    logging.info('Copying: ' + fc + ' to ' + FGDB_fds[i] + ' feature dataset.')

    in_features = fc
    out_feature_class = newFGDB_loc + '\\' + FGDB_fds[i] + '\\' + fc_truncate

    arcpy.CopyFeatures_management(in_features, out_feature_class)
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                      Create the ENABLED field
def createENABLED(fc_truncate):

    print '    ' + fc_truncate + ' is in a geom network.  Creating ENABLED field.'
    logging.info('    ' + fc_truncate + ' is in a geom network.  Creating ENABLED field.')

    in_table = newFGDB_loc + '\\' + FGDB_fds[i] + '\\' + fc_truncate
    field_name = 'ENABLED'
    field_type = 'SHORT'
    field_precision = ''
    field_scale = ''
    field_length = ''
    field_alias = 'Trace Enabled'
    field_is_nullable = 'NULLABLE'
    field_is_required = 'NON_REQUIRED'
    field_domain = ''

    arcpy.AddField_management (in_table, field_name, field_type,
                         field_precision, field_scale, field_length,
                         field_alias, field_is_nullable,
                         field_is_required, field_domain)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                     Calculate the ENABLED field
def calculateENABLED(fc_truncate):

    print '    Calculating ENABLED field for: ' + fc_truncate + '\n'
    logging.info('    Calculating ENABLED field for: ' + fc_truncate + '\n')

    out_feature_class = newFGDB_loc + '\\' + FGDB_fds[i] + '\\' + fc_truncate
    in_table = out_feature_class
    field="ENABLED"
    expression="getFunctional(str(!FNCTNL_CD!))"
    expression_type="PYTHON_9.3"
    code_block="""def getFunctional(value):
        if value == 'Y':
            return 1
        else:
            return 0"""

    arcpy.CalculateField_management(in_table, field, expression, expression_type,
                                code_block)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                      Create the 'Operable' field
def createOperable(fc_truncate):

    print '    ' + fc_truncate + ' Creating Operable field.'
    logging.info('    ' + fc_truncate + ' Creating Operable field.')

    in_table = newFGDB_loc + '\\' + FGDB_fds[i] + '\\' + fc_truncate
    field_name = 'Operable'
    field_type = 'SHORT'
    field_precision = ''
    field_scale = ''
    field_length = ''
    field_alias = 'Operable'
    field_is_nullable = 'NULLABLE'
    field_is_required = 'NON_REQUIRED'
    field_domain = ''

    arcpy.AddField_management (in_table, field_name, field_type,
                         field_precision, field_scale, field_length,
                         field_alias, field_is_nullable,
                         field_is_required, field_domain)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                     Calculate the 'Operable' field
def calculateOperable(fc_truncate):

    print '    Calculating Operable field for: ' + fc_truncate + '\n'
    logging.info('    Calculating Operable field for: ' + fc_truncate + '\n')

    in_table = newFGDB_loc + '\\' + FGDB_fds[i] + '\\' + fc_truncate
    field="Operable"
    expression="getFunctional(str(!FNCTNL_CD!))"
    expression_type="PYTHON_9.3"
    code_block="""def getFunctional(value):
        if value == 'Y':
            return 1
        else:
            return 0"""

    arcpy.CalculateField_management(in_table, field, expression, expression_type,
                                code_block)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#       Check to see if 'sdw_old.gdb' currently exists and delete it if it does
#            so that we can rename the current 'sdw.gdb' to 'sdw_old.gdb'
def delete_existing_sdw_old(currentData_file_loc):

    currentFileName = currentData_file_loc + '\\' + 'sdw_old.gdb'
    print 'Checking to see if FGDB sdw_old.gdb currently exists...'
    logging.info('Checking to see if FGDB sdw_old.gdb currently exists...')

    if os.path.exists(currentFileName):
        print 'sdw_old.gdb currently exists, deleting sdw_old.gdb'
        logging.info('sdw_old.gdb currently exists, deleting sdw_old.gdb')

        #Process
        shutil.rmtree(currentFileName)

    else:
        print 'sdw_old.gdb does NOT exist, no need to delete.'
        logging.info('sdw_old.gdb does NOT exist, no need to delete.')

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#Rename the current 'sdw.gdb' that the StandAlone mxd is using to 'sdw_old.gdb'
#to act as a BACKUP FGDB.
def rename_current_sdw(currentData_file_loc):

    currentFileName = currentData_file_loc + '\\' + 'sdw.gdb'
    newFileName = currentData_file_loc + '\\' + 'sdw_old.gdb'

    if os.path.exists(currentFileName):

        print 'Renaming: ' + currentFileName + ' to: ' + newFileName
        logging.info('Renaming: ' + currentFileName + ' to: ' + newFileName)

        os.rename(currentFileName, newFileName)
    else:
        print 'WARNING!!!'
        logging.warning('WARNING!!!')
        print currentFileName + """ Does not exist.  Cannot rename current FGDB.
        This may not be an error IF there was no sdw.gdb when the
        script was started"""
        loggin.warning(currentFileName + 'Does not exist.  Cannot rename current FGDB.')
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#Rename the new 'sdw_new.gdb' that the StandAlone mxd is using to 'sdw.gdb'
#to act as the ACTIVE FGDB.
def rename_new_FGDB(currentData_file_loc):

    currentFileName = currentData_file_loc + '\\' + 'sdw_new.gdb'
    newFileName = currentData_file_loc + '\\' + 'sdw.gdb'

    if os.path.exists(currentFileName):

        print 'Renaming: ' + currentFileName + ' to: ' + newFileName
        logging.info('Renaming: ' + currentFileName + ' to: ' + newFileName)

        os.rename(currentFileName, newFileName)
    else:
        print 'ERROR!!!'
        logging.error('ERROR!!!')
        print currentFileName + 'Does not exist.  Cannot rename new FGDB.'
        logging.error(currentFileName + 'Does not exist.  Cannot rename new FGDB.')

#-------------------------------------------------------------------------------
# *************************** END DEFINE FUNCTIONS  ****************************
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# *************************** BEGIN MAIN  *******************************
#-------------------------------------------------------------------------------

try:
    #Create the new FGDB
    createNewFGDB()

    #   Copy the features from Atlas to the appropriate location on the local FGDB
    i = 0
    #Cycle through all of the feature datasets on Atlas
    while i < len(FGDB_fds):
        print 'Changing workspace to : ' + ATLAS_fds[i] + ' on ATLAS \n\n'
        logging.info('Changing workspace to : ' + ATLAS_fds[i] + ' on ATLAS \n\n')

        try:
            arcpy.env.workspace = database_connection_file + '\\' + ATLAS_fds[i]
            fcs = arcpy.ListFeatureClasses()

        except Exception as e:
            print 'Setting workspace failed.  Is the connection file correct?'
            logging.info('Setting workspace failed.  Is the connection file correct?')
            print str(e)
            logging.info(str(e))
            success = False

        #Sort the list of feature classes.  'Pass' the sort function if the list
        #only contains one item and is not sortable.
        try:
            fcs.sort()
        except:
            pass

        #For each Feature Class (fc) in the ATLAS feature datasets we defined in our
        #ATLAS_fds list: copy the features, create the ENABLED field, and then
        #calculate the enabled field based off the 'FNCTNL_CD' field.
        for fc in fcs:
            #Strip out the 'SDW.CITY.' prefix from the feature class name
            fc_truncate = fc[9:]
            #If the feature class name is in one of the lists above, then copy
            #the feature class over to the local FGDB
            if ((fc_truncate in RWATER_FC) or (fc_truncate in SANGIS_FC) or
                (fc_truncate in SEWER_FC) or (fc_truncate in WATER_FC) or
                 fc_truncate in GRID_FC):

                try:
                    copyFeatures(fc, fc_truncate)

                except Exception as e:
                    print 'copyFeatures function failed'
                    logging.info('copyFeatures function failed')
                    print str(e)
                    logging.info(str(e))
                    success = False

                #If fc = will be in a geometric network, then add the ENABLED field
                #that the geom net uses to keep track of if a feature should be
                #traced or not
                if(fc_truncate in in_geom_net):
                    #Create the ENABLED field
                    try:
                        createENABLED(fc_truncate)

                    except Exception as e:
                        print 'createENABLED function failed'
                        logging.info('createENABLED function failed')
                        print str(e)
                        logging.info(str(e))
                        success = False

                    #Calculate ENABLED field
                    try:
                        calculateENABLED(fc_truncate)

                    except Exception as e:
                        print 'calculateENABLED function failed'
                        logging.info('calculateENABLED function failed')
                        print str(e)
                        logging.info(str(e))
                        success = False

                else:
                    print ''
                    logging.info('')

                if (fc_truncate == 'W_VALVE'):
                     #Create the Operable field needed for the secondary trace tool
                     #for the 'W_VALVE' feature class
                    try:
                        createOperable(fc_truncate)

                    except Exception as e:
                        print 'createOperable function failed'
                        logging.info('createOperable function failed')
                        print str(e)
                        logging.info(str(e))
                        success = False

                    #Calculate Operable field
                    try:
                        calculateOperable(fc_truncate)

                    except Exception as e:
                        print 'calculateOperable function failed'
                        logging.info('calculateOperable function failed')
                        print str(e)
                        logging.info(str(e))
                        success = False

            else:
                pass
        print '\n'
        logging.info('\n')
        #increase the index to go to the next feature dataset in ATLAS
        i+=1
    #---------------------------------------------------------------------------
    #Now that there is a local FGDB we want to rename both the current 'sdw.gdb'
    #and the 'sdw_new.gdb'

    #First delete the existing 'sdw_old.gdb' if it exists
    try:
        delete_existing_sdw_old(currentData_file_loc)

    except Exception as e:
        print 'delete_existing_sdw_old function failed.'
        logging.info('delete_existing_sdw_old function failed')
        print str(e)
        logging.info(str(e))
        success = False

    #Rename the current 'sdw.gdb' to 'sdw_old.gdb'
    try:
        rename_current_sdw(currentData_file_loc)

    except Exception as e:
        print 'rename_current_sdw function failed.  Is there a schema lock?'
        logging.info('rename_current_sdw function failed Is there a schema lock?')
        print str(e)
        logging.info(str(e))
        success = False

    #Rename the 'sdw_new.gdb' to 'sdw.gdb'
    try:
        rename_new_FGDB(currentData_file_loc)

    except Exception as e:
        print 'rename_new_FGDB function failed.  Is there a schema lock?'
        logging.info('rename_new_FGDB function failed.  Is there a schema lock?')
        print str(e)
        logging.info(str(e))
        success = False

except Exception as e:
    print 'There was an error in the MAIN'
    logging.info('There was an error in the MAIN')
    print str(e)
    logging.error(str(e))
    success = False
    #-------------------------------------------------------------------------------
    # *************************** END MAIN  *********************************
    #-------------------------------------------------------------------------------

if success == True:
    print 'SUCCESSFULLY FINISHED'
    logging.info('SUCCESSFULLY FINISHED')
else:
    print """ERROR!!!  There was an error with the script.
    Please check log for info"""
    logging.error('ERROR!!!  There was an error with the script.  Please see above for info')

print 'Done running CopyATLASDataToLocalFGDB.py'
logging.info('--------------------------------------------------------------')
logging.info('                  ' + str(datetime.now()))
logging.info('                   Finished running script')
logging.info('--------------------------------------------------------------\n')