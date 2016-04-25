################################################################################
#Author: Mike Grue
#Date: 4/25/16
#The below script is intended to be used inside of a MXD.  You should copy and
#paste everything below the ####'s in order to create .lyr files.
#You can add layer names to:
#'skipList' if you don't want those layers created.  This is
#currently being used for all the basemap layers.
#You can also change:
#'dfName' if the dataframe name is different
#You can also change:
#'locToSaveLyrFiles' to the location where you want to save the layer files to
################################################################################

import arcpy
arcpy.env.overwriteOutput = True

#-------------------------------------------------------------------------------
                         #Variables that may change
skipList = ['Basemap', 'Points Of Interest', 'Library', 'Hospital',
'Fire Station', 'School', 'Rec Center (County)',
'Points Of Interest Names (Thomas Bros)', 'Addresses', 'Roads',
'Road Names (Major)', 'Road Names (All)', 'Road Centerline (and Block Ranges)',
'Road Thomas Brothers', 'Railroads', 'Rivers', 'Streams', 'Airport Runways',
'Lakes', 'Military Facilities', 'Indian Reservations', 'RightOfWay (Line)',
'Parks (Active Use)', 'Parks (County)', 'National Forest', 'Parcels (Outline)',
'Parcels (Shading)', 'City Boundary (Shading)', 'City Boundary',
'Vicinity Shading', 'Aerial 2014', 'Layers', 'SDW.CITY.FIELD_BOOK',
'SDW.CITY.GRID_PAGE_TB', 'SDW.CITY.GRID_TILE_TB']

dfName = 'Layers'

locToSaveLyrFiles = r"C:\Users\mgrue\CompasGIS\MXD\Test\LayerFiles\TestLayerFiles"

#-------------------------------------------------------------------------------
                          #Script that probably won't change

mxd = arcpy.mapping.MapDocument("CURRENT")

df = arcpy.mapping.ListDataFrames(mxd, dfName)[0]

lyrs = arcpy.mapping.ListLayers(mxd, '', df)

for lyr in lyrs:
    if lyr.name in skipList:
        pass
    else:
        if lyr.isFeatureLayer:
            print lyr.name
            arcpy.SaveToLayerFile_management(lyr.longName,
            locToSaveLyrFiles + '\\' + lyr.name,
            'ABSOLUTE', 'CURRENT')