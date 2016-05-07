#-------------------------------------------------------------------------------
# Name:        Prepare_DRAWING_Tables_ToBeLoaded.py
# Purpose:      This script prepares the two DRAWING tables to be loaded with
#               the Simple Data Loader in ArcCatalog
#
# Author:      MGrue
#
# Created:     06/05/2016
# Copyright:   (c) MGrue 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#Prepare Processed tables to be loaded into the LGIM container tables

import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r'C:/Users/mgrue/CompasGIS/MXD/WorkingMXDs/DRAWING/ProcessedTables.gdb'
table1 = 'DRAWING'
table2 = 'DRAWING_FACILITY'

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                                   TABLE1
#                   Make a new text field: COUNCILDISTRICT
try:
    in_table = table1
    field_name="COUNCILDISTRICT"
    field_type="TEXT"
    field_precision=""
    field_scale=""
    field_length="3"
    field_alias="Council District"
    field_is_nullable="NULLABLE"
    field_is_required="NON_REQUIRED"
    field_domain=""

    print 'Adding field: ' + field_name + ' to table: ' + in_table
    arcpy.AddMessage('Adding field: ' + field_name + ' to table: ' + in_table)

    arcpy.AddField_management(in_table, field_name, field_type, field_precision,
    field_scale, field_length, field_alias, field_is_nullable, field_is_required,
    field_domain)

    print 'Finished adding field'
    arcpy.AddMessage('Finished adding field')
    #-------------------------------------------------------------------------------
    #        Load data to new COUNCILDISTRICT field from COUNCIL_DISTRICT_NUM
    #                       then delete COUNCIL_DISTRICT_NUM

    #Now make a table view to calculate into the new field
    arcpy.MakeTableView_management(table1, 'table1_view')

    in_table='table1_view'
    field="COUNCILDISTRICT"
    expression="!COUNCIL_DISTRICT_NUM!"
    expression_type="PYTHON"
    code_block=""

    print 'Importing data into field: ' + field + ' from: ' + expression
    arcpy.AddMessage('Importing data into field: ' + field + ' from: ' + expression)

    arcpy.CalculateField_management(in_table, field, expression, expression_type,
    code_block)

    print 'Finished Importing data'
    arcpy.AddMessage('Finished Importing data')
    """
    #Delete COUNCIL_DISTRICT_NUM
    in_table = table1
    drop_field="COUNCIL_DISTRICT_NUM"

    print 'Deleting: ' + drop_field + ' from ' + in_table
    arcpy.AddMessage('Deleting: ' + drop_field + ' from ' + in_table)

    arcpy.DeleteField_management(in_table, drop_field)

    print 'Deleted field'
    arcpy.AddMessage('Deleted field')
    """
    #-------------------------------------------------------------------------------
    ##                   Make a new text field: FLD_BK_PAGE_NUM
    in_table = table1
    field_name="FLD_BK_PAGE_NUM"
    field_type="TEXT"
    field_precision=""
    field_scale=""
    field_length="7"
    field_alias="Field Book Page Number"
    field_is_nullable="NULLABLE"
    field_is_required="NON_REQUIRED"
    field_domain=""

    print 'Adding field: ' + field_name + ' to table: ' + in_table
    arcpy.AddMessage('Adding field: ' + field_name + ' to table: ' + in_table)

    arcpy.AddField_management(in_table, field_name, field_type, field_precision,
    field_scale, field_length, field_alias, field_is_nullable, field_is_required,
    field_domain)

    print 'Finished adding field'
    arcpy.AddMessage('Finished adding field')
    #-------------------------------------------------------------------------------
    #        Load data to new FLD_BK_PAGE_NUM field from FLD_BK_PG_NUM
    #                        then delete FLD_BK_PG_NUM

    #Now make a table view to calculate into the new field
    arcpy.MakeTableView_management(table1, 'table1_view')

    in_table='table1_view'
    field="FLD_BK_PAGE_NUM"
    expression="!FLD_BK_PG_NUM!"
    expression_type="PYTHON"
    code_block=""

    print 'Importing data into field: ' + field + ' from: ' + expression
    arcpy.AddMessage('Importing data into field: ' + field + ' from: ' + expression)

    arcpy.CalculateField_management(in_table, field, expression, expression_type,
    code_block)

    print 'Finished Importing data'
    arcpy.AddMessage('Finished Importing data')
    """
    #Delete FLD_BK_PG_NUM
    in_table = table1
    drop_field="FLD_BK_PG_NUM"

    print 'Deleting: ' + drop_field + ' from ' + in_table
    arcpy.AddMessage('Deleting: ' + drop_field + ' from ' + in_table)

    arcpy.DeleteField_management(in_table, drop_field)

    print 'Deleted field'
    arcpy.AddMessage('Deleted field')
    """
    #-------------------------------------------------------------------------------
    #                        Delete LAST_BATCH_UPDT_DT (as TEXT field)
    #                       There is no data in this field so it is OK

    in_table = table1
    drop_field="LAST_BATCH_UPDT_DT"

    print 'Deleting: ' + drop_field + ' from ' + in_table
    arcpy.AddMessage('Deleting: ' + drop_field + ' from ' + in_table)

    arcpy.DeleteField_management(in_table, drop_field)

    print 'Deleted field'
    arcpy.AddMessage('Deleted field')

    #-------------------------------------------------------------------------------
    #                        Recreate LAST_BATCH_UPDT_DT (as Date field)
    in_table = table1
    field_name="LAST_BATCH_UPDT_DT"
    field_type="DATE"
    field_precision=""
    field_scale=""
    field_length=""
    field_alias="Last Batch Update Date"
    field_is_nullable="NULLABLE"
    field_is_required="NON_REQUIRED"
    field_domain=""

    print 'Adding field: ' + field_name + ' to table: ' + in_table
    arcpy.AddMessage('Adding field: ' + field_name + ' to table: ' + in_table)

    arcpy.AddField_management(in_table, field_name, field_type, field_precision,
    field_scale, field_length, field_alias, field_is_nullable, field_is_required,
    field_domain)

    print 'Finished adding field'
    arcpy.AddMessage('Finished adding field')

except Exception as e:
    print 'ERROR with process for: ' + table1
    arcpy.AddMessage('ERROR with process for: ' + table1)
    print str(e)
    arcpy.AddMessage(str(e))
#-------------------------------------------------------------------------------
#                          Change PRIM_DRAWG_IND to have the values
#                            that will match our YesNoDomain
try:
    arcpy.MakeTableView_management(table2, 'viewTable2')

    #Select 'Y'
    selection_type="NEW_SELECTION"
    where_clause="PRIM_DRAWG_IND = 'Y'"
    print 'Selecting: ' + where_clause
    arcpy.SelectLayerByAttribute_management('viewTable2', selection_type, where_clause)

    #Calculate to "Yes"
    field = 'PRIM_DRAWG_IND'
    expression = '"' + 'Yes' + '"'
    print 'Calculating expression: ' + expression
    arcpy.CalculateField_management('viewTable2', field, expression, expression_type="PYTHON", code_block="")

    #Select 'N'
    selection_type="NEW_SELECTION"
    where_clause="PRIM_DRAWG_IND = 'N'"
    print 'Selecting: ' + where_clause
    arcpy.SelectLayerByAttribute_management('viewTable2', selection_type, where_clause)

    #Calculate to "No"
    field = 'PRIM_DRAWG_IND'
    expression =  '"' + 'No' + '"'
    print 'Calculating expression: ' + expression
    arcpy.CalculateField_management('viewTable2', field, expression, expression_type="PYTHON", code_block="")

    print 'FINISHED'
except Exception as e:
    print 'ERROR with process for: ' + table2
    arcpy.AddMessage('ERROR with process for: ' + table2)
    print str(e)
    arcpy.AddMessage(str(e))
"""
#-------------------------------------------------------------------------------
#                                   TABLE2
#                   Make a new text field: Rel_FACILITYID
try:
    in_table = table2
    field_name="Rel_FACILITYID"
    field_type="LONG"
    field_precision=""
    field_scale=""
    field_length="20"
    field_alias="Rel Facility Id"
    field_is_nullable="NULLABLE"
    field_is_required="NON_REQUIRED"
    field_domain=""

    print 'Adding field: ' + field_name + ' to table: ' + in_table
    arcpy.AddMessage('Adding field: ' + field_name + ' to table: ' + in_table)

    arcpy.AddField_management(in_table, field_name, field_type, field_precision,
    field_scale, field_length, field_alias, field_is_nullable, field_is_required,
    field_domain)

    print 'Finished adding field'
    arcpy.AddMessage('Finished adding field')
    #-------------------------------------------------------------------------------
    #        Load data to new Rel_FACILITYID field from FAC_SEQ_NUM
    #                       then delete FAC_SEQ_NUM

    #Now make a table view to calculate into the new field
    arcpy.MakeTableView_management(table2, 'table2_view')

    in_table='table2_view'
    field="Rel_FACILITYID"
    expression="!FAC_SEQ_NUM!"
    expression_type="PYTHON"
    code_block=""

    print 'Importing data into field: ' + field + ' from: ' + expression
    arcpy.AddMessage('Importing data into field: ' + field + ' from: ' + expression)

    arcpy.CalculateField_management(in_table, field, expression, expression_type,
    code_block)

    print 'Finished Importing data'
    arcpy.AddMessage('Finished Importing data')

    #-----------------------------------------
    #Delete FAC_SEQ_NUM
    in_table = table1
    drop_field="FAC_SEQ_NUM"

    print 'Deleting: ' + drop_field + ' from ' + in_table
    arcpy.AddMessage('Deleting: ' + drop_field + ' from ' + in_table)

    arcpy.DeleteField_management(in_table, drop_field)

    print 'Deleted field'
    arcpy.AddMessage('Deleted field')

    #-------------------------------------------------------------------------------
    #                   Make a new text field: Rel_FAC_TYP_CD
    in_table = table2
    field_name="Rel_FAC_TYP_CD"
    field_type="TEXT"
    field_precision=""
    field_scale=""
    field_length="4"
    field_alias="Rel Facility Id"
    field_is_nullable="NULLABLE"
    field_is_required="NON_REQUIRED"
    field_domain=""

    print 'Adding field: ' + field_name + ' to table: ' + in_table
    arcpy.AddMessage('Adding field: ' + field_name + ' to table: ' + in_table)

    arcpy.AddField_management(in_table, field_name, field_type, field_precision,
    field_scale, field_length, field_alias, field_is_nullable, field_is_required,
    field_domain)

    print 'Finished adding field'
    arcpy.AddMessage('Finished adding field')
    #-------------------------------------------------------------------------------
    #        Load data to new Rel_FAC_TYP_CD field from FAC_TYP_CD
    #                       then delete FAC_TYP_CD

    #Now make a table view to calculate into the new field
    arcpy.MakeTableView_management(table2, 'table2_view')

    in_table='table2_view'
    field="Rel_FACILITYID"
    expression="!FAC_TYP_CD!"
    expression_type="PYTHON"
    code_block=""

    print 'Importing data into field: ' + field + ' from: ' + expression
    arcpy.AddMessage('Importing data into field: ' + field + ' from: ' + expression)

    arcpy.CalculateField_management(in_table, field, expression, expression_type,
    code_block)

    print 'Finished Importing data'
    arcpy.AddMessage('Finished Importing data')

    #Delete FAC_TYP_CD
    in_table = table1
    drop_field="FAC_TYP_CD"

    print 'Deleting: ' + drop_field + ' from ' + in_table
    arcpy.AddMessage('Deleting: ' + drop_field + ' from ' + in_table)

    arcpy.DeleteField_management(in_table, drop_field)

    print 'Deleted field'
    arcpy.AddMessage('Deleted field')

except Exception as e:
    print 'ERROR with process for: ' + table2
    arcpy.AddMessage('ERROR with process for: ' + table2)
    print str(e)
    arcpy.AddMessage(str(e))"""