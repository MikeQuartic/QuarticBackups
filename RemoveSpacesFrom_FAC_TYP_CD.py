#-------------------------------------------------------------------------------
# Name:        RemoveSpacesFrom_FAC_TYP_CD.py
# Purpose:
#
# Author:      MGrue
#
# Created:     04/05/2016
# Copyright:   (c) MGrue 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
arcpy.env.overwriteOutput = True

#-------------------------------------------------------------------------------
#                        Variables that may change

#arcpy.env.workspace = r'C:\Users\mgrue\CompasGIS\MXD\Test\TestRelationshipClass\TestRelClass_AllSPLASH.gdb'
fgdb = r'C:\Users\mgrue\CompasGIS\MXD\WorkingMXDs\DRAWING\ProcessedTables.gdb'
origTable = fgdb + '\\' + 'DRAWING'
#newTable = fgdb + '\\' + 'DRAWING_spaces_removed'
#newTable = fgdb + '\\' + 'DRAWING_final'

#Selects the data from the City that has spaces in it
selectList = ['A  ', 'AB ', 'AD ', 'AL ', 'AW ', 'B  ', 'BD ', 'BL ', 'C  ',
'CD ', 'CL ', 'CT ', 'CW ', 'D', 'D  ', 'DD ', 'DL ', 'ED ', 'FB ', 'FD ',
'FW ', 'H  ', 'ID ', 'JL ', 'L  ', 'M  ', 'MB ', 'MD ', 'O  ', 'PM ', 'R  ',
'S  ', 'W  ', 'XD ', 'XL ', 'YD ']

#List of data that has the spaces removed
replaceList = ["A", "AB", "AD", "AL", "AW", "B", "BD", "BL", "C",
"CD", "CL", "CT", "CW", "D", "D", "DD", "DL", "ED", "FB", "FD",
"FW", "H", "ID", "JL", "L", "M", "MB", "MD", "O", "PM", "R",
"S", "W", "XD", "XL", "YD"]

#-------------------------------------------------------------------------------
#                      Variables that will not change
i = 0
#-------------------------------------------------------------------------------
#                  Remove extra spaces from DRAWG_TYP_CD field

#Make a table view that we can perform selections and calculations on
arcpy.MakeTableView_management(origTable, 'viewTable')


#Run through the select list and select the CD's that have spaces then
#run through the replace list and replace the codes with non spaces
while i<len(selectList):

    #Select the features with a space in their DRAWG_TYP_CD
    selection_type="NEW_SELECTION"
    where_clause="DRAWG_TYP_CD = '%s'" % selectList[i]

    print 'Where clause: ' + where_clause
    arcpy.AddMessage('Where clause: ' + where_clause)
    print 'Selecting ' + selectList[i]
    arcpy.AddMessage('Selecting ' + selectList[i])

    arcpy.SelectLayerByAttribute_management('viewTable', selection_type, where_clause)

    #Calculate the selected features to take out the spaces
    field = 'DRAWG_TYP_CD'
    expression = '"' + replaceList[i] + '"'

    print 'Calculating: ' + field + ' to: ' + expression + '\n'
    arcpy.AddMessage('Calculating: ' + field + ' to: ' + expression + '\n')

    arcpy.CalculateField_management('viewTable', field, expression, expression_type="PYTHON", code_block="")

    i += 1

print 'Finished successfully'
arcpy.AddMessage('Finished successfully')

