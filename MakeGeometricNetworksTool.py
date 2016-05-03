import arcpy
import shutil, os
arcpy.env.overwriteOutput = True

arcpy.AddMessage('arcpy imported')

#------------------------------------------------------------------------------
#   Variables that will be parameters

originalData = arcpy.GetParameterAsText(0)
#originalData = r'C:\Users\mgrue\CompasGIS\ERDs\FinalERDs\FGDBs\Infrastructure.gdb'

newFGDB_loc = arcpy.GetParameterAsText(1)
#newFGDB_loc = r'C:\Users\mgrue\Scratch\TestGeomNet'

nameOfSewerDataset = arcpy.GetParameterAsText(2)
#nameOfSewerDataset = 'Sewer'

nameOfWaterDataset = arcpy.GetParameterAsText(3)
#nameOfWaterDataset = 'Water'

nameOfRecycledDataset = arcpy.GetParameterAsText(4)
#nameOfRecycledDataset = 'Recycled'

snapTolerance = arcpy.GetParameterAsText(5)
#snapTolerance = '3.28083333333333E-03'

preserveEnabled = arcpy.GetParameterAsText(6)
#preserveEnabled = True
if preserveEnabled == True:
    preserveEnabled = 'PRESERVE_ENABLED'
else:
    preserveEnabled = 'NO_PRESERVE_ENABLED'
#-------------------------------------------------------------------------------
#     Variables that will PROBABLY NOT change

#Set the name of the new FGDB
newFGDB_name = 'Infrastructure_GeomNet.gdb'


#Get a list of the Feature Datasets from the original data
arcpy.env.workspace = originalData
fds = arcpy.ListDatasets('', 'Feature')
fds.sort()

#Not currently using this, but could if I wanted to limit the clips
skipList = ['CathodicProtection', 'PUD_Misc']

#-------------------------------------------------------------------------------

def makeGeom(featureDataset):
    try:
        arcpy.AddMessage('Making Geom Net for: ' + featureDataset)
        #print 'Making Geom Net for: ' + featureDataset


        #    WATER GEOM NETWORK

        if featureDataset == nameOfWaterDataset:
            #Make Water Geom Network
            print 'Making ' + featureDataset + ' Geom Net'

            in_feature_dataset = featureDataset
            out_name = 'Water_Net'
            in_source_feature_classes = 'wControlValve SIMPLE_JUNCTION NO;wFitting SIMPLE_JUNCTION NO;wHydrant SIMPLE_JUNCTION NO;wMain COMPLEX_EDGE NO;wMeter SIMPLE_JUNCTION NO;wPump SIMPLE_JUNCTION NO;wService COMPLEX_EDGE NO;wSystemValve SIMPLE_JUNCTION NO'
            snap_tolerance = snapTolerance
            weights = ''
            weight_associations = ''
            z_snap_tolerance = ''
            preserve_enabled_values = preserveEnabled

            arcpy.CreateGeometricNetwork_management(in_feature_dataset, out_name,
            in_source_feature_classes, snap_tolerance, weights,
            weight_associations, z_snap_tolerance, preserve_enabled_values)

            arcpy.AddMessage('Made Water Geom Net')
            print 'Made Water Geom Net'


        #       RECYCLED GEOM NETWORK

        elif featureDataset == nameOfRecycledDataset:
            #Make Recycled Geom Network
            print 'Making ' + featureDataset + ' Geom Net'

            in_feature_dataset = featureDataset
            out_name = 'Recycled_Net'
            in_source_feature_classes = 'rControlValve SIMPLE_JUNCTION NO;rFitting SIMPLE_JUNCTION NO;rMain COMPLEX_EDGE NO;rMeter SIMPLE_JUNCTION NO;rPump SIMPLE_JUNCTION NO;rService COMPLEX_EDGE NO;rSystemValve SIMPLE_JUNCTION NO'
            snap_tolerance = snapTolerance
            weights = ''
            weight_associations = ''
            z_snap_tolerance = ''
            preserve_enabled_values = preserveEnabled

            arcpy.CreateGeometricNetwork_management(in_feature_dataset, out_name,
            in_source_feature_classes, snap_tolerance, weights,
            weight_associations, z_snap_tolerance, preserve_enabled_values)

            arcpy.AddMessage('Made Recycled Geom Net')
            print 'Made Recycled Geom Net'


        #         SEWER GEOM NETWORK

        elif featureDataset == nameOfSewerDataset:
            #Make Sewer Geom Network
            print 'Making ' + featureDataset + ' Geom Net'

            in_feature_dataset = featureDataset
            out_name = 'Sewer_Net'
            in_source_feature_classes = 'ssCleanOut SIMPLE_JUNCTION YES;ssControlValve SIMPLE_JUNCTION YES;ssFitting SIMPLE_JUNCTION YES;ssGravityMain COMPLEX_EDGE NO;ssLateral COMPLEX_EDGE NO;ssManhole SIMPLE_JUNCTION YES;ssPressurizedMain COMPLEX_EDGE NO;ssPump SIMPLE_JUNCTION YES;ssServiceConnection SIMPLE_JUNCTION NO;ssSystemValve SIMPLE_JUNCTION YES'
            snap_tolerance = snapTolerance
            weights = ''
            weight_associations = ''
            z_snap_tolerance = ''
            preserve_enabled_values = preserveEnabled

            arcpy.CreateGeometricNetwork_management(in_feature_dataset, out_name,
            in_source_feature_classes, snap_tolerance, weights,
            weight_associations, z_snap_tolerance, preserve_enabled_values)

            arcpy.AddMessage('Made Sewer Geom Net')
            print 'Made Sewer Geom Net'
    except:
        arcpy.AddMessage('FAILED to create Geom net for ' + featureDataset)
        print 'FAILED to create Geom net for ' + featureDataset


#-------------------------------------------------------------------------------

     #Build new FGDB to create the Geom Network

try:
    arcpy.AddMessage('Creating new FGDB at ' + newFGDB_loc + '\\' + newFGDB_name)
    print 'Creating new FGDB at ' + newFGDB_loc + '\\' + newFGDB_name

    src = originalData
    dest = newFGDB_loc + '\\' + newFGDB_name
    if os.path.exists(dest):
        arcpy.AddMessage(dest + '\nalready exists.  Did not create new FGDB')
        print dest + '\nalready exists.  Did not create new FGDB'
    else:
        arcpy.AddMessage('Making new FGDB from: ' + src + '\nTo: ' + dest)
        shutil.copytree(src, dest)
        arcpy.AddMessage('Finished making new FGDB')

except:
    arcpy.AddMessage('Didn\'t build the new FGDB')
    print 'Didn\'t build the new FGDB'

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
#Loop through all of the feature datasets in the edit FGDB and make a GeomNet

arcpy.env.workspace = dest
print dest
i = 0
while i < len(fds):
    fd = fds[i]
    #print fd
    if (fd in skipList):
        pass
        ##print fc.name + ' is being skipped.'
    else:
        makeGeom(fd)
    i += 1
#-------------------------------------------------------------------------------
