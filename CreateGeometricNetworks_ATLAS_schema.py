#-------------------------------------------------------------------------------
# Name:        CreateGeometricNetworks_ATLAS_schema.py
# Purpose:     This script creates Water_Net, Recycled_Net, and Sewer_Net
# networks on which ever FGDB is entered in the FGDB_loc variable.  It needs
# the Feature Data Set to be named 'WATER', 'RWATER', 'SEWER' in order to work.
# It is assumed that the data is copied over from ATLAS and not ATLAS-EDIT since
# there is different schema between the two.  See water_in_source_features for
# the 'list' of feature classes that will be in the 'Water_Net' geom network.
# Sewer geom network has an additional geoprocessing tool on it to set the flow
# direction on the sewer network.
#
# Author:      MGrue
#
# Created:     22/08/2016
# Copyright:   (c) MGrue 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy, logging
from datetime import datetime
arcpy.env.overwriteOutput = True

#-------------------------------------------------------------------------------
#  Variables that will change when script is moved from one computer to another

jobDirectory = arcpy.GetParameterAsText(0)

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#                      Set Variables that probably wont change
#                  (as long as the file structure for the StandAlone
#                       folder in the Y: Drive doesn't change)

FGDB_loc = jobDirectory + '\\' + 'Data\sdw.gdb'

#                                   Set up logger
#  Where do you want the log file to go???
fileLog = jobDirectory + '\\' + r'Maintenance\Logs\CreateGeometricNetworks_ATLAS_schema.log'

#-------------------------------------------------------------------------------
#                                 Set up logger
#If you need to debug, set the level=logging.INFO to logging.DEBUG
logging.basicConfig(filename = fileLog, level=logging.DEBUG)

#Header for the log file
logging.info('--------------------------------------------------------------' )
logging.info('                  ' + str(datetime.now()))
logging.info('                Running CreateGeometricNetworks_ATLAS_schema.py')
logging.info('--------------------------------------------------------------' )

#-------------------------------------------------------------------------------
#                 Set workspace to the FGDB to create the geom nets

arcpy.env.workspace = FGDB_loc

#-------------------------------------------------------------------------------
#     Set the variables the could change if we change the feature classes
#          that are participating in the geom net, or snapping, etc.
#     Note the odd way that ESRI makes a 'list' for the in_source_features.

#Set the water variables
wFDS = 'WATER'
water_in_source_features = ('W_AQUEDUCT COMPLEX_EDGE NO;W_CAP SIMPLE_JUNCTION NO;W_CHANNEL COMPLEX_EDGE NO;W_FLUME COMPLEX_EDGE NO;W_HYDRANT SIMPLE_JUNCTION NO;W_METER SIMPLE_JUNCTION NO;W_PIPE COMPLEX_EDGE NO;W_PUMP SIMPLE_JUNCTION NO;W_REDUCER SIMPLE_JUNCTION NO;W_REGULATOR_VALVE SIMPLE_JUNCTION NO;W_SERVICE COMPLEX_EDGE NO;W_VALVE SIMPLE_JUNCTION NO')

#Set the recycled variables
rFDS = 'RWATER'
recycled_in_source_features = ('RWTR_REGULATOR_VALVE SIMPLE_JUNCTION NO;RWTR_REDUCER SIMPLE_JUNCTION NO;RWTR_CAP SIMPLE_JUNCTION NO;RWTR_PIPE COMPLEX_EDGE NO;RWTR_METER SIMPLE_JUNCTION NO;RWTR_PUMP SIMPLE_JUNCTION NO;RWTR_SERVICE COMPLEX_EDGE NO;RWTR_VALVE SIMPLE_JUNCTION NO;')

#Set the sewer variables
sFDS = 'SEWER'
sewer_in_source_features = ('S_CLEAN_OUT SIMPLE_JUNCTION NO;S_VALVE SIMPLE_JUNCTION NO;S_PLUG SIMPLE_JUNCTION NO;S_REDUCER SIMPLE_JUNCTION NO;S_MAIN COMPLEX_EDGE NO;S_LATERAL COMPLEX_EDGE NO;S_MANHOLE SIMPLE_JUNCTION NO;S_PUMP SIMPLE_JUNCTION NO;S_METER SIMPLE_JUNCTION NO')

#Set the variables that will be used for all the geom nets this script creates
snap_tolerance = '0.01'
weights = ''
weight_associations = ''
z_snap_tolerance = ''
preserve_enabled_values = 'PRESERVE_ENABLED'

#-------------------------------------------------------------------------------
#                            Set an error flag
wasError = False

#-------------------------------------------------------------------------------
#                          START of MAIN

print 'Making Geometric Networks for: ' + FGDB_loc + '\n'
##arcpy.AddMessage('Making Geometric Networks for: ' + FGDB_loc)
logging.info('Making Goemetric Networks for: ' + FGDB_loc + '\n')

#Get a list of the feature data sets
fds = arcpy.ListDatasets('', 'Feature')

try:
    #Loop through the water, recycled, and sewer feature datasets
    for fd in fds:

#-------------------------------------------------------------------------------
        #Make Water Geom Network
        if (fd == wFDS):

            print 'Making ' + wFDS + ' Geom Net'
            ##arcpy.AddMessage('Making Geom Net for: ' + wFDS)
            logging.info('Making Geom Net for: ' + wFDS)

            in_feature_dataset = wFDS
            out_name = wFDS + '_Net'
            in_source_feature_classes = water_in_source_features


            arcpy.CreateGeometricNetwork_management(in_feature_dataset, out_name,
            in_source_feature_classes, snap_tolerance, weights,
            weight_associations, z_snap_tolerance, preserve_enabled_values)


            ##arcpy.AddMessage('Made Geom Net for: ' + wFDS)
            print 'Made Geom Net for: ' + wFDS
            ##logging.info('Made Geom Net for: ' + wFDS)


#-------------------------------------------------------------------------------
        #Make Recycled Geom Network
        elif (fd == rFDS):

            print 'Making ' + rFDS + ' Geom Net'
            ##arcpy.AddMessage('Making Geom Net for: ' + rFDS)
            logging.info('Making Geom Net for: ' + rFDS)

            in_feature_dataset = rFDS
            out_name = rFDS + '_Net'
            in_source_feature_classes = recycled_in_source_features


            arcpy.CreateGeometricNetwork_management(in_feature_dataset, out_name,
            in_source_feature_classes, snap_tolerance, weights,
            weight_associations, z_snap_tolerance, preserve_enabled_values)


            ##arcpy.AddMessage('Made Geom Net for: ' + rFDS)
            print 'Made Geom Net for: ' + rFDS
            ##logging.info('Made Geom Net for: ' + rFDS)

#-------------------------------------------------------------------------------
        #Make Sewer Geom Network
        elif (fd == sFDS):

            print 'Making ' + sFDS + ' Geom Net'
            ##arcpy.AddMessage('Making Geom Net for: ' + sFDS)
            logging.info('Making Geom Net for: ' + sFDS)

            in_feature_dataset = sFDS
            out_name = sFDS + '_Net'
            in_source_feature_classes = sewer_in_source_features
            arcpy.CreateGeometricNetwork_management(in_feature_dataset, out_name,
            in_source_feature_classes, snap_tolerance, weights,
            weight_associations, z_snap_tolerance, preserve_enabled_values)


            ##arcpy.AddMessage('Made Geom Net for: ' + sFDS)
            print 'Made Geom Net for: ' + sFDS
            ##logging.info('Made Geom Net for: ' + sFDS)

        #Set flow direction for the Sewer Geometric Network
            in_geometric_network= FGDB_loc + r'\SEWER\SEWER_Net'
            flow_option="WITH_DIGITIZED_DIRECTION"

            ##arcpy.AddMessage('Setting Flow Direction for: ' + in_geometric_network)
            print 'Setting Flow Direction for: ' + in_geometric_network
            logging.info('Setting Flow Direction for: ' + in_geometric_network)

            arcpy.SetFlowDirection_management(in_geometric_network, flow_option)

            ##arcpy.AddMessage('Finished Setting Flow Direction for: ' + in_geometric_network)
            print 'Finished Setting Flow Direction for: ' + in_geometric_network
            ##logging.info('Finished Setting Flow Direction for: ' + in_geometric_network)
#-------------------------------------------------------------------------------
        #Feature Dataset is not Water, Recycled, or Sewer
        else:
            print fd + ' Feature Dataset will not have a geometric network created for it'
            ##arcpy.AddMessage(fd + ' Feature Dataset will not have a geometric network created for it')
            logging.info(fd + ' Feature Dataset will not have a geometric network created for it')

#-------------------------------------------------------------------------------

except Exception as e:
    wasError = True
    print str(e)
    ##arcpy.AddMessage(str(e))
    logging.info(str(e))

#-------------------------------------------------------------------------------

if (wasError == False):
    print '\nCreateGeomNetwork_ProductionSchema.py has FINISHED SUCCESSFULLY'
    ##arcpy.AddMessage('CreateGeomNetwork_ProductionSchema.py has FINISHED SUCCESSFULLY')
    logging.info('\nCreateGeomNetwork_ProductionSchema.py has FINISHED SUCCESSFULLY')

else:
    print '\nCreateGeomNetwork_ProductionSchema.py has finished with ERRORS'
    ##arcpy.AddMessage('CreateGeomNetwork_ProductionSchema.py has inished with ERRORS')
    logging.error('\nCreateGeomNetwork_ProductionSchema.py has finished with ERRORS')

logging.info('--------------------------------------------------------------')
logging.info('                  ' + str(datetime.now()))
logging.info('                   Finished running script')
logging.info('--------------------------------------------------------------\n')
