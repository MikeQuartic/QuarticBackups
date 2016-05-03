#This script makes a relationship class for every feature class that is in
#a FGDB defined in the arcpy.env.workspace

#TODO: when we use this script to create rel classes on our LGIM data
#      we will need to change the origin_primary_key to "FACILITYID"


import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.workspace = arcpy.GetParameterAsText(0)
#arcpy.env.workspace = r'C:\Users\mgrue\CompasGIS\MXD\Test\TestRelationshipClass\TestRelClass_AllSPLASH.gdb'

#The LGIM FC's that are in skipList do not have DRAWINGS associated with them
#No need to create a relationship class for them

#Below is the skipList for LGIM FC's
"""
skipList = ['ssStructure', 'wPressureZone', 'rPressureZone', 'wStructure',
'rStructure', 'pudDetailInset', 'pudEasement', 'pudIndexGrid',
'pudIndexGridQuad', 'pudFiber', 'pudFuelLine', 'pudJumpOver', 'wBreakLeak',
'wOperationalArea', 'rOperationalArea']
"""

#Below is the skipList for the SPLASH FC's.
#TODO: This should be commented out and the LGIM skipList above should be made
#available once we migrate to working with LGIM data.
skipList = ['delivery_area', 'detail_inset', 'easement_splash',
'emergency_service_area', 'flow_arrow', 'hgl', 'index_grid', 'index_grid_line',
'index_grid_quadrant', 'reimbursement_agreement', 'ws_jump_over']

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def CreateRelationshipClass(FeatureClass, fd):
    #---------------------------------------------------------------------------
    #                      Create the relationship class
    try:
        arcpy.AddMessage( 'Creating the relationship class for: ' + FeatureClass)
        origin_table = FeatureClass
        destination_table = 'DRAWING'
        out_relationship_class = origin_table + '_To_DRAWING'
        relationship_type = 'SIMPLE'
        forward_label = 'From ' + origin_table + ' To DRAWING'
        backward_label = 'From DRAWING To ' + origin_table
        message_direction = 'NONE'
        cardinality = 'MANY_TO_MANY'
        attributed = 'ATTRIBUTED'

        #TODO: when we use this script to create rel classes on our LGIM data
        #we will need to change the origin_primary_key to "FACILITYID"
        ##origin_primary_key = 'FACILITYID'
        origin_primary_key = 'FAC_SEQ_NUM'
        origin_foreign_key = 'FAC_SEQ_NUM'
        destination_primary_key = 'Num_CD'
        destination_foreign_key = 'Num_CD'


        arcpy.CreateRelationshipClass_management(origin_table, destination_table,
        out_relationship_class, relationship_type, forward_label, backward_label,
        message_direction, cardinality, attributed, origin_primary_key,
        origin_foreign_key, destination_primary_key, destination_foreign_key)

        arcpy.AddMessage( 'Created relationship class: ' + out_relationship_class)

    except Exception as e:
        arcpy.AddMessage( 'ERROR creating the relationship class')
        arcpy.AddMessage( str(e))

    #---------------------------------------------------------------------------
    #               Create the schema from DRAWING_FACILITY
    #               for the newly created relationship class
    try:
        arcpy.AddMessage( ('Starting to Create the schema for the newly created relationship class: '
        + out_relationship_class))
        #TODO:
        #Loop through every FC that currently exists in the City's DRAWING_FACILITY
        #table and create the same schema

        #variables that do not change from added field to added field
        in_table = out_relationship_class
        field_precision = 0
        field_scale = 0
        field_is_nullable = 'NULLABLE'
        field_is_required = 'NON_REQUIRED'
        field_domain = ''
        i = 0

        while (i < 12):
            #variables that will change from each added field
            addedFieldName = ['FAC_TYP_CD', 'DRAWG_NUM', 'DRAWG_SHEET_NUM', 'DRAWG_TYP_CD',
            'PRIM_DRAWG_IND', 'LAST_ATTR_UPDT_DT', 'LAST_ATTR_UPDT_ID', 'LOCK__ID',
            'FACILITY_KEY', 'LAST_BATCH_UPDT_ID', 'LAST_BATCH_UPDT_DT', 'PHASE__ID']

            addedFieldType = ['String', 'String', 'SmallInteger', 'String', 'String',
            'Date', 'String', 'String', 'String', 'String', 'Date', 'Integer']

            addedFieldLength = [50, 50, 2, 50, 50, 8, 50, 50, 50, 50, 8, 4]

            field_name = addedFieldName[i]
            field_type = addedFieldType[i]
            field_length = addedFieldLength[i]
            field_alias = field_name

            arcpy.AddField_management (in_table, field_name, field_type, field_precision,
            field_scale, field_length, field_alias, field_is_nullable,
            field_is_required, field_domain)

            arcpy.AddMessage( '    Made field: ' + field_name)

            i += 1

        arcpy.AddMessage( 'Finished creating the schema for the relationship class: ' + out_relationship_class)

    except Exception as e:
        arcpy.AddMessage( 'ERROR creating the schema for the relationship class: ' + out_relationship_class)
        arcpy.AddMessage( str(e))
    #---------------------------------------------------------------------------
    #                      Append the data from DRAWING_FACILITY
    #                     to the newly created relationship class
    try:
        arcpy.AddMessage( 'Appending the data from DRAWING_FACILITY to the newly created relationship class')
        inputs = 'DRAWING_FACILITY'
        target = out_relationship_class
        schema_type = 'TEST'

        arcpy.Append_management(inputs, target, schema_type)
        arcpy.AddMessage( 'Finished appending data')
        arcpy.AddMessage( '\nFINISHED making a relationship class for Feature Class: ' + FeatureClass)

    except Exception as e:
        arcpy.AddMessage( 'ERROR appending the data from DRAWING_FACILITY to the relationship class: ' + out_relationship_class)

    arcpy.AddMessage( '----------------------------------------------------------------\n\n')

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------



#Loop through all fc's in FGDB and create a relationship class for it
fds = arcpy.ListDatasets('', 'Feature')
for fd in fds:
    arcpy.AddMessage( 'Feature dataset: ' + fd)
    fcs = arcpy.ListFeatureClasses('', '', fd)
    for fc in fcs:
        if fc in skipList:
            #We don't want to create a Rel Class if a FC is in skipList
            arcpy.AddMessage( 'NOT making a rel class for: ' + fc)
        else:
            arcpy.AddMessage( 'Passing ' + fc + ' into CreateRelationshipClass')
            CreateRelationshipClass(fc, fd)

