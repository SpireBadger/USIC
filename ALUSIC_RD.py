# Project: AL to USIC data
# Create Date: 02/13/2020
# Last Updated: 02/18/2020
# Create by: Brad Craddick
# Updated by: Robert Domiano
# Purpose: To provide a clean set of the AL GIS data to send to USIC
# ArcGIS Version:   10.2
# Python Version:   2.7.5
# Input Variables: 
# Output:


# -----------------------------------------------------------------------

# For testing purposes, the script will be run in unbuffered mode
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)


# Import modules
import sys, os, arcpy, datetime, traceback, tempfile
import shutil

# Set unbuffered mode
sys.stdout = Unbuffered(sys.stdout)

# Set up Try/Except for Error Logging
try:
    # set datetime variable
    d = datetime.datetime.now()
    # open log file for holding errors
    # will also create file if not already there
    log = open("C:\\Temp\ALLogFile.txt","a")
    log.write("----------------------------" + "\n")
    log.write("----------------------------" + "\n")
    # write datetime to log
    log.write("Log: " + str(d) + "\n")
    log.write("\n")
    # set arcpy environment to allow overwriting
    arcpy.env.overwriteOutput=True

#----------------------Main Text-----------------------------------------
    # Set path variable
    cPath = r"C:\Temp"
    gdbName = "AL_USIC_2.gdb"
    isGDB = os.path.join(cPath, gdbName)
    # Test if gdb exists, if so delete. If not, create
    if arcpy.Exists(isGDB):
        print ("{} already exists and will be deleted.".format(isGDB))
        arcpy.Delete_management(isGDB)
    # Creates a new GDB
    else:
        pass
    
    print ("{} is being created.".format(isGDB))
    outWS = arcpy.CreateFileGDB_management(cPath, gdbName)
        
    # Connecting to an existing SDE doesn't seem to work unless the connection
    # is already in place.
    # This is a work around to deal with that issue and avoid needing to connect
    # ahead of time outside the script.
    sdeTempPath = tempfile.mkdtemp()
    arcpy.CreateDatabaseConnection_management(sdeTempPath, 'tempALServ.sde', \
                                              'ORACLE', 'xs-bhm-dgp-1:1521/gsp',\
                                              'DATABASE_AUTH', 'GISADMIN', \
                                              'gisadmin','SAVE_USERNAME')
    # Set the new temp connection as the usable workspace
    inputWS = arcpy.env.workspace = sdeTempPath + r"\tempALServ.sde"
    
    #Create var for mainText & path to where the new one should  be
    mainText = "mainText"
    newmainText = os.path.join(isGDB, mainText)
    
    # Copy mainText features to new gdb
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.MainText', newmainText)
    
    # Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management('mainText', 'temp_lyr')

    # Create a list of variables to save
    keepList = ['OBJECTID','SHAPE_Length','SHAPE_Area','SHAPE',\
                     'TextString', 'FontSize', 'Angle']
    delList = []
    
    # Get list of fields in temp layer
    fields = arcpy.ListFields(tempLayer)

    # Iterate through all fields in the temp feature layer
    for field in fields:
        # If the field name is not in the keep list or a required field
        # add it to the empty deletion list
        if field.name not in keepList and not field.required:
            delList.append(field.name)
            print("{} is added to the delete list.".format(field.name))
            sys.stdout.flush()
        # If the field is in the keep list, pass to the next field
        else:
            print("Keeping {}.".format(field.name))
            sys.stdout.flush()
            pass
    
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = "MainTextUSIC.shp"
    shpPath = "C:\Temp\SHP"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
#        print("{} exists and will be deleted.".format(shpPathFull))
        arcpy.Delete_management(shpPathFull)
    else:
#        print("{} not found and copy can proceed.".format(shpPathFull))
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
#    print("Shapefile created.")
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer)
    
#----------------------Regulator Stations-----------------------------------------
    # Create the regulator  variables
    newVar = "RegulatorStation"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.RegulatorStation',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')

    # Create a list of variables to save
    keepList = ['OBJECTID','INSTALLDATE','LOCATIONDESCRIPTION','ROTATIONANGLE',\
                'COMMENTS', 'MAXINLETPRESSURE', 'MAXOUTLETPRESSURE', 'SETTINGNAME']
    # Create empty deletion list
    delList = []    

    # Get list of fields in temp layer
    fields = arcpy.ListFields(tempLayer)

    # Iterate through all fields in the temp feature layer
    for field in fields:
        # If the field name is not in the keep list or a required field
        # add it to the empty deletion list
        if field.name not in keepList and not field.required:
            delList.append(field.name)
            print("{} is added to the delete list.".format(field.name))
            sys.stdout.flush()
        # If the field is in the keep list, pass to the next field
        else:
            print("Keeping {}.".format(field.name))
            sys.stdout.flush()
            pass   
        
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = "RegUSIC.shp"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
#        print("{} exists and will be deleted.".format(shpPathFull))
        arcpy.Delete_management(shpPathFull)
    else:
#        print("{} not found and copy can proceed.".format(shpPathFull))
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
#    print("Shapefile created.")
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
#    print("Shapefile created.")
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer)
    
#----------------------Abandoned Main-----------------------------------------
    # Create the regulator  variables
    newVar = "AbandonedMain"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.AbandonedMain',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')

    # Create a list of variables to save
    keepList = ['OBJECTID','MEASUREDLENGTH', 'CASTIRONTYPE', 'COATINGTYPE', \
                'NOMINALPIPESIZE', 'MATERIAL','DATEABANDONED', 'LABELTEXT']
    
    # Create empty deletion list
    delList = []    

    # Get list of fields in temp layer
    fields = arcpy.ListFields(tempLayer)

    # Iterate through all fields in the temp feature layer
    for field in fields:
        # If the field name is not in the keep list or a required field
        # add it to the empty deletion list
        if field.name not in keepList and not field.required:
            delList.append(field.name)
            print("{} is added to the delete list.".format(field.name))
            sys.stdout.flush()
        # If the field is in the keep list, pass to the next field
        else:
            print("Keeping {}.".format(field.name))
            sys.stdout.flush()
            pass   
        
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = "abandonMainUSIC.shp"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
#        print("{} exists and will be deleted.".format(shpPathFull))
        arcpy.Delete_management(shpPathFull)
    else:
#        print("{} not found and copy can proceed.".format(shpPathFull))
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
#    print("Shapefile created.")
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
#    print("Shapefile created.")
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer)
    
#----------------------Valves-----------------------------------------
  # Create the variables
    newVar = "Valves"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.Valve',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')

    # Create a list of variables to save
    keepList = ['OBJECTID','SHAPE', 'INSTALLDATE', 'COMMENTS', 'HOUSEDIN', \
                'MATERIAL', 'INSULATEDINDICATOR', 'VALVEENDS', 'VALVETYPE', \
                'VALVEUSE', 'ROTATIONANGLE', 'VALVEMATERIAL', 'VALVESIZE', \
                'LABELTEXT']
    
    # Create empty deletion list
    delList = []    

    # Get list of fields in temp layer
    fields = arcpy.ListFields(tempLayer)

    # Iterate through all fields in the temp feature layer
    for field in fields:
        # If the field name is not in the keep list or a required field
        # add it to the empty deletion list
        if field.name not in keepList and not field.required:
            delList.append(field.name)
            print("{} is added to the delete list.".format(field.name))
            sys.stdout.flush()
        # If the field is in the keep list, pass to the next field
        else:
            print("Keeping {}.".format(field.name))
            sys.stdout.flush()
            pass   
        
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = "valveUSIC.shp"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
#        print("{} exists and will be deleted.".format(shpPathFull))
        arcpy.Delete_management(shpPathFull)
    else:
#        print("{} not found and copy can proceed.".format(shpPathFull))
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
#    print("Shapefile created.")
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
#    print("Shapefile created.")
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer)   
       
    # When done, remove the temp path containing the connection files
    shutil.rmtree(sdeTempPath)
    
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" \
            + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"    
    log.write("" + pymsg + "\n")
    log.write("" + msgs + "")
    print(msgs)
    log.close()
   
#    ######--Regulator Station USIC---
#    Dist=r"\\parcser02\GisServerManager\Data\AL.sde\GISADMIN.Gas\GISADMIN.RegulatorStation"
#    Dists=r"C:\temp\NO_GIS_SP_2.gdb\DimDimInterim"
#    USIC=r"\\pdatfile01\ProdData\GIS\USIC\SpireAL"
#    USICpdf=r"\\pdatfile01\ProdData\GIS\USIC\SpireAL"
#    if arcpy.Exists(Dists):
#        arcpy.Delete_management(Dists)
#    arcpy.CopyFeatures_management(Dist,Dists)
#    arcpy.MakeFeatureLayer_management (Dists, 'Distsss')
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    for field in fields:
#        if field.name == 'OBJECTID':
#            print 'keeping '+field.name
#        elif field.name == 'SHAPE_Length':
#            print 'keeping '+field.name
#        elif field.name == 'SHAPE.AREA':
#            print 'keeping '+field.name
#        elif field.name == 'SHAPE':
#            print 'keeping '+field.name
#        elif field.name == 'INSTALLDATE':
#            print 'keeping '+field.name
#        elif field.name == 'LOCATIONDESCRIPTION':
#            print 'keeping '+field.name
#        elif field.name == 'ROTATIONANGLE':
#            print 'keeping '+field.name
#        elif field.name == 'COMMENTS':
#            print 'keeping '+field.name
#        elif field.name == 'MAXINLETPRESSURE':
#            print 'keeping '+field.name
#        elif field.name == 'MAXOUTLETPRESSURE':
#            print 'keeping '+field.name
#        elif field.name == 'SETTINGNAME':
#            print 'keeping '+field.name
#        elif field.name == 'MAXOUTLETPRESSURE':
#            print 'keeping '+field.name
#        else :
#            print 'deleting '+field.name
#            fieldNameList.append(field.name)
#    print fieldNameList
#    arcpy.DeleteField_management ("Distsss", fieldNameList)
#    if arcpy.Exists(USIC+"\\"+"RegulatorStationUSIC.shp"):
#        arcpy.Delete_management(USIC+"\\"+"RegulatorStationUSIC.shp")
#    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"RegulatorStationUSIC.shp")
#    ##########--AbandonedMain USIC---##
#    Dist=r"\\parcser02\GisServerManager\Data\AL.sde\GISADMIN.Gas\GISADMIN.AbandonedMain"
#    Dists=r"C:\temp\NO_GIS_SP_2.gdb\LocIndInterim"
#    arcpy.CopyFeatures_management(Dist,Dists)
#    arcpy.MakeFeatureLayer_management (Dists, 'Distsss')
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    for field in fields:
#        if field.name == 'OBJECTID':
#            print 'keeping '+field.name
#        elif field.name == 'SHAPE':
#            print 'keeping '+field.name
#        elif field.name == 'MEASUREDLENGTH':
#            print 'keeping '+field.name
#        elif field.name == 'CASTIRONTYPE':
#            print 'keeping '+field.name
#        elif field.name == 'COATINGTYPE':
#            print 'keeping '+field.name
#        elif field.name == 'NOMINALPIPESIZE':
#            print 'keeping '+field.name
#        elif field.name == 'MATERIAL':
#            print 'keeping '+field.name
#        elif field.name == 'DATEABANDONED':
#            print 'keeping '+field.name        
#        else :
#            print 'deleting '+field.name
#            fieldNameList.append(field.name)
#    print fieldNameList
#    arcpy.DeleteField_management ("Distsss", fieldNameList)
#    if arcpy.Exists(USIC+"\\"+"AbandonedMainUSIC.shp"):
#        arcpy.Delete_management(USIC+"\\"+"AbandonedMainUSIC.shp")
#    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"AbandonedMainUSIC.shp")
#        ##########--GasValveUSIC---##
#    Dist=r"\\parcser02\GisServerManager\Data\AL.sde\GISADMIN.Gas\GISADMIN.Valve"
#    Dists=r"C:\temp\NO_GIS_SP_2.gdb\LocIndInterim"
#    arcpy.CopyFeatures_management(Dist,Dists)
#    arcpy.MakeFeatureLayer_management (Dists, 'Distsss')
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    for field in fields:
#        if field.name == 'OBJECTID':
#            print 'keeping '+field.name
#        elif field.name == 'SHAPE':
#            print 'keeping '+field.name
#        elif field.name == 'INSTALLDATE':
#            print 'keeping '+field.name
#        elif field.name == 'LOCATIONDESCRIPTION':
#            print 'keeping '+field.name
#        elif field.name == 'COMMENTS':
#            print 'keeping '+field.name
#        elif field.name == 'HOUSEDIN':
#            print 'keeping '+field.name
#        elif field.name == 'MATERIAL':
#            print 'keeping '+field.name
#        elif field.name == 'INSULATEDINDICATOR':
#            print 'keeping '+field.name
#        elif field.name == 'VALVEENDS':
#            print 'keeping '+field.name
#        elif field.name == 'VALVETYPE':
#            print 'keeping '+field.name
#        elif field.name == 'VALVEUSE':
#            print 'keeping '+field.name
#        elif field.name == 'ROTATIONANGLE':
#            print 'keeping '+field.name
#        elif field.name == 'VALVEMATERIAL':
#            print 'keeping '+field.name
#        elif field.name == 'VALVESIZE':
#            print 'keeping '+field.name
#        elif field.name == 'LABELTEXT':
#            print 'keeping '+field.name
#        elif field.name == 'VALVESIZE':
#            print 'keeping '+field.name
#        else :
#            print 'deleting '+field.name
#            fieldNameList.append(field.name)
#    print fieldNameList
#    arcpy.DeleteField_management ("Distsss", fieldNameList)
#    if arcpy.Exists(USIC+"\\"+"ValveUSIC.shp"):
#        arcpy.Delete_management(USIC+"\\"+"ValveUSIC.shp")
#    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"ValveUSIC.shp")  
#        ##########--Casing USIC---##
#    Dist=r"\\parcser02\GisServerManager\Data\AL.sde\GISADMIN.Gas\GISADMIN.Casing"
#    Dists=r"C:\temp\NO_GIS_SP_2.gdb\LocIndInterim"
#    arcpy.CopyFeatures_management(Dist,Dists)
#    arcpy.MakeFeatureLayer_management (Dists, 'Distsss')
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    for field in fields:
#        if field.name == 'OBJECTID':
#            print 'keeping '+field.name
#        elif field.name == 'SHAPE':
#            print 'keeping '+field.name
#        elif field.name == 'MEASUREDLENGTH':
#            print 'keeping '+field.name
#        elif field.name == 'CASINGCOATINDICATOR':
#            print 'keeping '+field.name
#        elif field.name == 'CASINGSIZE':
#            print 'keeping '+field.name
#        elif field.name == 'CASINGMATERIAL':
#            print 'keeping '+field.name
#        elif field.name == 'LABELTEXT':
#            print 'keeping '+field.name
#        else :
#            print 'deleting '+field.name
#            fieldNameList.append(field.name)
#    print fieldNameList
#    arcpy.DeleteField_management ("Distsss", fieldNameList)
#    if arcpy.Exists(USIC+"\\"+"CasingUSIC.shp"):
#        arcpy.Delete_management(USIC+"\\"+"CasingUSIC.shp")
#    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"CasingUSIC.shp")
#        ##########--Drip USIC---##
#    Dist=r"\\parcser02\GisServerManager\Data\AL.sde\GISADMIN.Gas\GISADMIN.Drip"
#    Dists=r"C:\temp\NO_GIS_SP_2.gdb\LocIndInterim"
#    arcpy.CopyFeatures_management(Dist,Dists)
#    arcpy.MakeFeatureLayer_management (Dists, 'Distsss')
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    for field in fields:
#        if field.name == 'OBJECTID':
#            print 'keeping '+field.name
#        elif field.name == 'SHAPE':
#            print 'keeping '+field.name
#        elif field.name == 'LOCATIONDESCRIPTION':
#            print 'keeping '+field.name
#        elif field.name == 'INSTALLDATE':
#            print 'keeping '+field.name
#        elif field.name == 'LABELTEXT':
#            print 'keeping '+field.name
#        else :
#            print 'deleting '+field.name
#            fieldNameList.append(field.name)
#    print fieldNameList
#    arcpy.DeleteField_management ("Distsss", fieldNameList)
#    if arcpy.Exists(USIC+"\\"+"DripUSIC.shp"):
#        arcpy.Delete_management(USIC+"\\"+"DripUSIC.shp")
#    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"DripUSIC.shp")
#            ##########--MarkerBallUSIC ---##
#    Dist=r"\\parcser02\GisServerManager\Data\AL.sde\GISADMIN.Gas\GISADMIN.ElectronicMarker"
#    Dists=r"C:\temp\NO_GIS_SP_2.gdb\LocIndInterim"
#    arcpy.CopyFeatures_management(Dist,Dists)
#    arcpy.MakeFeatureLayer_management (Dists, 'Distsss')
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    for field in fields:
#        if field.name == 'OBJECTID':
#            print 'keeping '+field.name
#        elif field.name == 'SHAPE':
#            print 'keeping '+field.name
#        elif field.name == 'INSTALLDATE':
#            print 'keeping '+field.name
#        elif field.name == 'DISTANCE1':
#            print 'keeping '+field.name
#        elif field.name == 'DIRECTION1':
#            print 'keeping '+field.name
#        elif field.name == 'LOCATION1':
#            print 'keeping '+field.name
#        elif field.name == 'BUILDING1':
#            print 'keeping '+field.name
#        elif field.name == 'STREET1':
#            print 'keeping '+field.name
#        elif field.name == 'DISTANCE2':
#            print 'keeping '+field.name
#        elif field.name == 'DIRECTION2':
#            print 'keeping '+field.name
#        elif field.name == 'LOCATION2':
#            print 'keeping '+field.name
#        elif field.name == 'BUILDING2':
#            print 'keeping '+field.name
#        elif field.name == 'STREET2':
#            print 'keeping '+field.name
#        else :
#            print 'deleting '+field.name
#            fieldNameList.append(field.name)
#    print fieldNameList
#    arcpy.DeleteField_management ("Distsss", fieldNameList)
#    if arcpy.Exists(USIC+"\\"+"MarkerBallUSIC.shp"):
#        arcpy.Delete_management(USIC+"\\"+"MarkerBallUSIC.shp")
#    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"MarkerBallUSIC.shp")
#            ##########--FirstCutRegulator USIC---##
#    Dist=r"\\parcser02\GisServerManager\Data\AL.sde\GISADMIN.Gas\GISADMIN.FirstCutRegulator"
#    Dists=r"C:\temp\NO_GIS_SP_2.gdb\LocIndInterim"
#    arcpy.CopyFeatures_management(Dist,Dists)
#    arcpy.MakeFeatureLayer_management (Dists, 'Distsss')
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    for field in fields:
#        if field.name == 'OBJECTID':
#            print 'keeping '+field.name
#        elif field.name == 'SHAPE':
#            print 'keeping '+field.name
#        elif field.name == 'LOCATIONDESCRIPTION':
#            print 'keeping '+field.name
#        elif field.name == 'ROTATIONANGLE':
#            print 'keeping '+field.name
#        elif field.name == 'INSTALLDATE':
#            print 'keeping '+field.name
#        else :
#            print 'deleting '+field.name
#            fieldNameList.append(field.name)
#    print fieldNameList
#    arcpy.DeleteField_management ("Distsss", fieldNameList)
#    if arcpy.Exists(USIC+"\\"+"FirstCutRegulatorUSIC.shp"):
#        arcpy.Delete_management(USIC+"\\"+"FirstCutRegulatorUSIC.shp")
#    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"FirstCutRegulatorUSIC.shp")
#                ##########--Fitting USIC ---##
#    Dist=r"\\parcser02\GisServerManager\Data\AL.sde\GISADMIN.Gas\GISADMIN.Fitting"
#    Dists=r"C:\temp\NO_GIS_SP_2.gdb\LocIndInterim"
#    arcpy.CopyFeatures_management(Dist,Dists)
#    arcpy.MakeFeatureLayer_management (Dists, 'Distsss')
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    fieldNameList = []
#    fields = arcpy.ListFields("Distsss")
#    for field in fields:
#        if field.name == 'OBJECTID':
#            print 'keeping '+field.name
#        elif field.name == 'SHAPE':
#            print 'keeping '+field.name
#        elif field.name == 'FITTINGSIZE':
#            print 'keeping '+field.name
#        elif field.name == 'INSULATEDINDICATOR':
#            print 'keeping '+field.name
#        elif field.name == 'MATERIAL':
#            print 'keeping '+field.name
#        elif field.name == 'FITTINGTYPE':
#            print 'keeping '+field.name
#        elif field.name == 'ROTATIONANGLE':
#            print 'keeping '+field.name
#        elif field.name == 'LABELTEXT':
#            print 'keeping '+field.name
#        else :
#            print 'deleting '+field.name
#            fieldNameList.append(field.name)
#    print fieldNameList
#    arcpy.DeleteField_management ("Distsss", fieldNameList)
#    if arcpy.Exists(USIC+"\\"+"FittingUSIC.shp"):
#        arcpy.Delete_management(USIC+"\\"+"FittingUSIC.shp")
#    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"FittingUSIC.shp")
#
#    
#
## End code, delete below ish but leave Except clauses and del variables if present
#except:
#    tb = sys.exc_info()[2]
#    tbinfo = traceback.format_tb(tb)[0]
#    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
#    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"    
#    log.write("" + pymsg + "\n")
#    log.write("" + msgs + "")
#    print(msgs)
#    log.close()
