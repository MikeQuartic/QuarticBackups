echo Change the JOBDIR to point to your StandAlone folder.  You also may need to set the 'ATLAS_Connection' variable if your AD connection to atlas is named something different than 'ad@atlas.sde'.

set JOBDIR=C:\Users\YOUR_NAME_HERE\CompassGIS\StandAlone

set ATLAS_Connection=ad@atlas.sde




set log=%JOBDIR%\Maintenance\Logs\StandAlone.log

echo ------------------------------------------------------->>%log%
echo ---[START CopyATLASDataToLocalFGDB.py %date% %time%]--->>%log%
echo ------------------------------------------------------->>%log%

echo Starting to copy ATLAS data to local FGDB >>%log%
Start /wait %JOBDIR%\Maintenance\Scripts\CopyATLASDataToLocalFGDB.py %JOBDIR% %ATLAS_Connection%

timeout /T 5

echo -------------------------------------------------------------------->>%log%
echo ---[START CreateGeometricNetworks_ATLAS_schema.py %date% %time%]--- >>%log%
echo -------------------------------------------------------------------->>%log%

echo Starting to create Geometric Networks >>%log%
Start /wait %JOBDIR%\Maintenance\Scripts\CreateGeometricNetworks_ATLAS_schema.py %JOBDIR%
