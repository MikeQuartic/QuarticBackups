#-------------------------------------------------------------------------------
# Name:        Add_Num_CD_To_DRAWING_Tables.py
# Purpose:     Adds field "Num_CD" to the two tables in the workspace then
#               Concatenates the fields [DRAWG_NUM] and [DRAWG_TYP_CD] into
#               the newly created field.
#
# Author:      MGrue
#
# Created:     06/05/2016
# Copyright:   (c) MGrue 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import arcpy

arcpy.env.workspace = r'C:/Users/mgrue/CompasGIS/MXD/WorkingMXDs/DRAWING/ProcessedTables.gdb'
table1 = 'DRAWING'
table2 = 'DRAWING_FACILITY'
#-------------------------------------------------------------------------------
#        Set variables that will remain the for both AddField processes
field_name="Num_CD"
field_type="TEXT"
field_precision=""
field_scale=""
field_length="25"
field_alias="Drawing Num - Type"
field_is_nullable="NULLABLE"
field_is_required="NON_REQUIRED"
field_domain=""

#        Set variables that will remain the same for both Concatenate processes
field="Num_CD"
expression="!DRAWG_NUM! + ' - ' + !DRAWG_TYP_CD!"
expression_type="PYTHON"
code_block=""
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                           Add field to FIRST table
try:
    #Set the first table to have the field added to:
    in_table = table1
    print 'Adding field to: ' + in_table
    arcpy.AddField_management(in_table, field_name, field_type, field_precision,
    field_scale, field_length, field_alias, field_is_nullable, field_is_required,
    field_domain)

    print 'Added field to: ' + in_table
except Exception as e:
    print 'ERROR with adding field to the FIRST table'
    print str(e)

#-------------------------------------------------------------------------------
#                      Concatenate the newly created field
try:
    #Now make a table view to concatenate into the new field
    arcpy.MakeTableView_management(table1, 'table1_view')

    #Concatenate the Num_CD field with [DRAWG_NUM] and the newly changed [DRAWG_TYP_CD]
    print 'Concatenating: ' + table1
    arcpy.AddMessage('Concatenating: ' + table1)
    arcpy.CalculateField_management('table1_view', field, expression,
    expression_type, code_block)

    print 'Finished concatenating: ' + table1
    arcpy.AddMessage('Finished concatenating: ' + table1)

except Exception as e:
    print 'ERROR with concatenating Num_CD for the FIRST table'
    arcpy.AddMessage('ERROR with concatenating Num_CD for the FIRST table')
    print str(e)
    arcpy.AddMessage(str(e))
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#                           Add field to SECOND table
#Set the second table to have the field added to:
try:
    in_table = table2
    print 'Adding field to: ' + in_table
    arcpy.AddField_management(in_table, field_name, field_type, field_precision,
    field_scale, field_length, field_alias, field_is_nullable, field_is_required,
    field_domain)

    print 'Added field to: ' + in_table
except Exception as e:
    print 'ERROR with adding field to the FIRST table'
    print str(e)

#-------------------------------------------------------------------------------
#                      Concatenate the newly created field
try:
    #Now make a table view to concatenate into the new field
    arcpy.MakeTableView_management(table2, 'table2_view')

    #Concatenate the Num_CD field with [DRAWG_NUM] and the newly changed [DRAWG_TYP_CD]
    print 'Concatenating: ' + table2
    arcpy.AddMessage('Concatenating: ' + table2)
    arcpy.CalculateField_management('table2_view', field, expression,
    expression_type, code_block)

    print 'Finished concatenating: ' + table2
    arcpy.AddMessage('Finished concatenating: ' + table2)

except Exception as e:
    print 'ERROR with concatenating Num_CD for the FIRST table'
    arcpy.AddMessage('ERROR with concatenating Num_CD for the FIRST table')
    print str(e)
    arcpy.AddMessage(str(e))

print 'FINISHED running Add_Num_CD_To_DRAWING_Tables.py'
arcpy.AddMessage('FINISHED running Add_Num_CD_To_DRAWING_Tables.py')