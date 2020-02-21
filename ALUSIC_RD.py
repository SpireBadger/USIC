# Project: AL to USIC data
# Create Date: 02/13/2020
# Last Updated: 02/20/2020
# Create by: Brad Craddick
# Updated by: Robert Domiano
# Purpose: To provide a clean set of the AL GIS data to send to USIC
# ArcGIS Version:   10.2
# Python Version:   2.7.5
# -----------------------------------------------------------------------

# For testing purposes, the script will be run in unbuffered mode
# This helps print statements generate as they are produced instead of at once.
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
    # Set path variables
    cPath = r"C:\Temp"
    gdbName = "AL_USIC.gdb"
    isGDB = os.path.join(cPath, gdbName)
    # Test if gdb exists, if so delete. If not, create
    if arcpy.Exists(isGDB):
        print ("{} already exists and will be deleted.".format(isGDB))
        arcpy.Delete_management(isGDB)
    else:
        pass
    
    print ("{} is being created.".format(isGDB))
    # Create the new GDB
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
    print("Database connection created at {0} to the AL Oracle Database."\
          .format(sdeTempPath))
    print("\n")
    # Set the new temp connection as the usable workspace
    inputWS = arcpy.env.workspace = sdeTempPath + r"\tempALServ.sde"
    
    #Create var for feature class & path to where the new one should  be
    mainText = "mainText"
    newmainText = os.path.join(isGDB, mainText)
    
    # Copy input FC features to new gdb
    print("Beginning to copy to {}.".format(newmainText))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.MainText',\
                                            newmainText)
    
    # Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management('mainText', 'temp_lyr')
    print("\n Temp layer created.")

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
    print("/n")
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
        print("Deleting existing shapefile.")
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
    print("A shapefile has been copied as {}.".format(shpPathFull))
    print("/n")
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer)
    
#----------------------Regulator Stations--------------------------------------
    # Create the regulator  variables
    newVar = "RegulatorStation"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    print("Beginning to copy to {}.".format(newVarPath))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.RegulatorStation',\
                                            newVarPath)
       
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')
    
    
    # Create a list of variables to save
    keepList = ['OBJECTID','INSTALLDATE','LOCATIONDESCRIPTION','ROTATIONANGLE',\
                'COMMENTS', 'MAXINLETPRESSURE', 'MAXOUTLETPRESSURE',\
                'SUBTYPE','SETTINGNAME']
    
    ###Locate all subtypes and add them to the keepList

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
    
    # Subtypes prevent deletion of a field. This section strips subtypes from
    # all variables in dellist.
    # An Error can result if the code tries to remove subtypes from an FC and
    # finds none. That is why the if statement is used.
    subtypes = arcpy.da.ListSubtypes(tempLayer)
    sKeys = subtypes.keys()
    for keys in sKeys:
        if keys != 0:
            print("Subtype found at code {}.".format(keys))
            sys.stdout.flush()
            arcpy.RemoveSubtype_management(tempLayer,keys)
        else:
            print("No subtypes found.")
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
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
    print("A shapefile has been copied as {}.".format(shpPathFull))

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
    print("Beginning to copy to {}.".format(newVarPath))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.AbandonedMain',\
                                            newVarPath)
    
    # Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')
    print("\n Temp layer created.")

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
        
    # Subtypes prevent deletion of a field. This section strips subtypes from
    # all variables in dellist.
    # An Error can result if the code tries to remove subtypes from an FC and
    # finds none. That is why the if statement is used.
    
    # Create list of subtypes in the temporary layer
    subtypes = arcpy.da.ListSubtypes(tempLayer)
    # Store all subtype keys
    sKeys = subtypes.keys()
    # For each key in the key list, test if it is equal to zero
    for keys in sKeys:
        # If a key is found that doesn't equal keys, delete all keys
        # NOTE: If there are any subtypes, keys should give a 1 value and
        # after finding a 1, it will delete all keys. 
        if keys != 0:
            print("Subtype found at code {}.".format(keys))
            arcpy.RemoveSubtype_management(tempLayer,keys)
        else:
            print("No subtypes found.")
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
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)

    
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
    print("Beginning to copy to {}.".format(newVarPath))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.Valve',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')
    print("\n Temp layer created.")

    # Create a list of variables to save
    keepList = ['OBJECTID','SHAPE', 'INSTALLDATE', 'COMMENTS', 'HOUSEDIN', \
                'MATERIAL', 'INSULATEDINDICATOR', 'VALVEENDS', 'VALVETYPE', \
                'VALVEUSE', 'ROTATIONANGLE', 'VALVEMATERIAL', 'VALVESIZE', \
                'LABELTEXT','TURNSTOCLOSE','DATECREATED','DATEMODIFIED']
    
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
        
    # Subtypes prevent deletion of a field. This section strips subtypes from
    # all variables in dellist.
    # An Error can result if the code tries to remove subtypes from an FC and
    # finds none. That is why the if statement is used.
    subtypes = arcpy.da.ListSubtypes(tempLayer)
    sKeys = subtypes.keys()
    for keys in sKeys:
        if keys != 0:
            print("Subtype found at code {}.".format(keys))
            arcpy.RemoveSubtype_management(tempLayer,keys)
        else:
            print("No subtypes found.")
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
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
    print("A shapefile has been copied as {}.".format(shpPathFull))

    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer)   
    
#----------------------Casing----------------------------------
  # Create the variables
    newVar = "casing"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    print("Beginning to copy to {}.".format(newVarPath))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.Casing',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')
    print("\n Temp layer created.")

    # Create a list of variables to save
    keepList = ['OBJECTID','MEASUREDLENGTH', 'CASINGCOATINDICATOR',\
                'CASINGSIZE', 'CASINGMATERIAL','LABELTEXT']
    
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
        
    # Subtypes prevent deletion of a field. This section strips subtypes from
    # all variables in dellist.
    # An Error can result if the code tries to remove subtypes from an FC and
    # finds none. That is why the if statement is used.
    subtypes = arcpy.da.ListSubtypes(tempLayer)
    sKeys = subtypes.keys()
    for keys in sKeys:
        if keys != 0:
            print("Subtype found at code {}.".format(keys))
            arcpy.RemoveSubtype_management(tempLayer,keys) 
        else:
            print("No subtypes found.")
            pass  
        
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = "casingUSIC.shp"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
    print("A shapefile has been copied as {}.".format(shpPathFull))
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer)   
#----------------------Drips---------------------------------
  # Create the variables
    newVar = "drips"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    print("Beginning to copy to {}.".format(newVarPath))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.Drip',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')
    print("\n Temp layer created.")

    # Create a list of variables to save
    keepList = ['OBJECTID','LOCATIONDESCRIPTION', 'INSTALLDATE','LABELTEXT']
    
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
        
    # Subtypes prevent deletion of a field. This section strips subtypes from
    # all variables in dellist.
    # An Error can result if the code tries to remove subtypes from an FC and
    # finds none. That is why the if statement is used.
    subtypes = arcpy.da.ListSubtypes(tempLayer)
    sKeys = subtypes.keys()
    for keys in sKeys:
        if keys != 0:
            print("Subtype found at code {}.".format(keys))
            sys.stdout.flush()
            arcpy.RemoveSubtype_management(tempLayer,keys) 
        else:
            print("No subtypes found.")
            pass  
        
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = "dripUSIC.shp"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
    print("A shapefile has been copied as {}.".format(shpPathFull))
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer)       

#----------------------Marker Balls---------------------------------
  # Create the variables
    newVar = "markBall"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    print("Beginning to copy to {}.".format(newVarPath))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.ElectronicMarker',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')
    print("\n Temp layer created.")

    # Create a list of variables to save
    keepList = ['OBJECTID','INSTALLDATE', 'DISTANCE1','DIRECTION1',\
                'LOCATION1','BUILDING1','STREET1','DISTANCE2','DIRECTION2',\
                'LOCATION2','BUILDING2','STREET2']
    
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
        
    # Subtypes prevent deletion of a field. This section strips subtypes from
    # all variables in dellist.
    # An Error can result if the code tries to remove subtypes from an FC and
    # finds none. That is why the if statement is used.
    subtypes = arcpy.da.ListSubtypes(tempLayer)
    sKeys = subtypes.keys()
    for keys in sKeys:
        if keys != 0:
            print("Subtype found at code {}.".format(keys))
            sys.stdout.flush()
            arcpy.RemoveSubtype_management(tempLayer,keys) 
    
        else:
            print("No subtypes found.")
            pass  
        
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = "markerBallUSIC.shp"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
    print("A shapefile has been copied as {}.".format(shpPathFull))
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer) 

#----------------------FirstCut Regulator---------------------------------
  # Create the variables
    newVar = "firstCutRegulator"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    print("Beginning to copy to {}.".format(newVarPath))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.FirstCutRegulator',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')
    print("\n Temp layer created.")

    # Create a list of variables to save
    keepList = ['OBJECTID','LOCATIONDESCRIPTION','ROTATIONANGLE','INSTALLDATE']
    
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
        
    # Subtypes prevent deletion of a field. This section strips subtypes from
    # all variables in dellist.
    # An Error can result if the code tries to remove subtypes from an FC and
    # finds none. That is why the if statement is used.
    subtypes = arcpy.da.ListSubtypes(tempLayer)
    sKeys = subtypes.keys()
    for keys in sKeys:
        if keys != 0:
            print("Subtype found at code {}.".format(keys))
            sys.stdout.flush()
            arcpy.RemoveSubtype_management(tempLayer,keys)
        else:
            print("No subtypes found.")
            pass  
        
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = "firstCutRegUSIC.shp"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
    print("A shapefile has been copied as {}.".format(shpPathFull))
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer) 

#----------------------Fittings---------------------------------
  # Create the variables
    newVar = "fittings"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    print("Beginning to copy to {}.".format(newVarPath))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.Fitting',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')
    print("\n Temp layer created.")

    # Create a list of variables to save
    keepList = ['OBJECTID','FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT','FITTINGSIZECODE'\
                'LOCATIONDESCRIPTION']
    
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
        
    # Subtypes prevent deletion of a field. This section strips subtypes from
    # all variables in dellist.
    # An Error can result if the code tries to remove subtypes from an FC and
    # finds none. That is why the if statement is used.
    subtypes = arcpy.da.ListSubtypes(tempLayer)
    sKeys = subtypes.keys()
    for keys in sKeys:
        if keys != 0:
            print("Subtype found at code {}.".format(keys))
            sys.stdout.flush()
            arcpy.RemoveSubtype_management(tempLayer,keys)
        else:
            print("No subtypes found.")
            pass  
        
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = newVar + "USIC.shp"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
    print("A shapefile has been copied as {}.".format(shpPathFull))
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer) 
#------------------------Distribution Main-------------------------------
  # Create the variables
    newVar = "fdistMain"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    print("Beginning to copy to {}.".format(newVarPath))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.Main',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')
    print("\n Temp layer created.")

    # Create a list of variables to save
    keepList = ['INSTALLDATE','MEASUREDLENGTH','LENGTHSOURCE','COATINGTYPE',\
                'MATERIAL','NOMINALPIPESIZE','PIPEGRADE','PRESSURECODE',\
                'MATERIALCODE','LABELTEXT','TRANSMISSION_FLAG',\
                'LOCATIONDESCRIPTION','PLASTICTYPE','PROJECTYEAR',\
                'MANUFACTURER','LENGTHMX']
    
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
        
    # Subtypes prevent deletion of a field. This section strips subtypes from
    # all variables in dellist.
    # An Error can result if the code tries to remove subtypes from an FC and
    # finds none. That is why the if statement is used.
    subtypes = arcpy.da.ListSubtypes(tempLayer)
    sKeys = subtypes.keys()
    for keys in sKeys:
        if keys != 0:
            print("Subtype found at code {}.".format(keys))
            sys.stdout.flush()
            arcpy.RemoveSubtype_management(tempLayer,keys) 
        
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = newVar + "USIC.shp"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
    print("A shapefile has been copied as {}.".format(shpPathFull))
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer) 

#------------------------Service-------------------------------
  # Create the variables
    newVar = "service"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    print("Beginning to copy to {}.".format(newVarPath))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.Service',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')
    print("\n Temp layer created.")

    # Create a list of variables to save
    keepList = ['INSTALLDATE','MEASUREDLENGTH','LENGTHSOURCE','COATINGTYPE',\
                'PIPETYPE','NOMINALPIPESIZE','PIPEGRADE','PRESSURECODE',\
                'MATERIALCODE','LABELTEXT','TRANSMISSION_FLAG',\
                'LOCATIONDESCRIPTION','HIGHDENSITYPLASTIC','PROJECTYEAR',\
                'PROJECTNUMBER','SERVICETYPE','MANUFACTURER','LENGTH604',\
                'STREETADDRESS','MAINMATERIAL']
    
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
        
    # Subtypes prevent deletion of a field. This section strips subtypes from
    # all variables in dellist.
    # An Error can result if the code tries to remove subtypes from an FC and
    # finds none. That is why the if statement is used.
    subtypes = arcpy.da.ListSubtypes(tempLayer)
    sKeys = subtypes.keys()
    for keys in sKeys:
        if keys != 0:
            print("Subtype found at code {}.".format(keys))
            sys.stdout.flush()
            arcpy.RemoveSubtype_management(tempLayer,keys)
        else:
            print("No subtypes found.")
            pass  
        
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = newVar + "USIC.shp"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
    print("A shapefile has been copied as {}.".format(shpPathFull))
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer)

#------------------------Stopper Fitting-------------------------------
  # Create the variables
    newVar = "service"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    print("Beginning to copy to {}.".format(newVarPath))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.StopperFitting',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')
    print("\n Temp layer created.")

    # Create a list of variables to save
    keepList = ['INSTALLDATE','LABELTEXT','LOCATIONDESCRIPTION','PRESENTPOSITION']
    
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
        
    # Subtypes prevent deletion of a field. This section strips subtypes from
    # all variables in dellist.
    # An Error can result if the code tries to remove subtypes from an FC and
    # finds none. That is why the if statement is used.
    subtypes = arcpy.da.ListSubtypes(tempLayer)
    sKeys = subtypes.keys()
    for keys in sKeys:
        if keys != 0:
            print("Subtype found at code {}.".format(keys))
            sys.stdout.flush()
            arcpy.RemoveSubtype_management(tempLayer,keys)
        else:
            print("No subtypes found.")
            pass  
        
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = newVar + "USIC.shp"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
    print("A shapefile has been copied as {}.".format(shpPathFull))
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer)
    
#------------------------Premise-------------------------------    
  # Create the variables
    newVar = "premise"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    print("Beginning to copy to {}.".format(newVarPath))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Historical\GISADMIN.Premise',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')
    print("\n Temp layer created.")

    # Create a list of variables to save
    keepList = ['INSTALLIONDATE','PIPENAME','LOCATIONDESCRIPTION',\
                'PIPEID','MANUFACTURER']
    
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
        
    # Subtypes prevent deletion of a field. This section strips subtypes from
    # all variables in dellist.
    # An Error can result if the code tries to remove subtypes from an FC and
    # finds none. That is why the if statement is used.
    subtypes = arcpy.da.ListSubtypes(tempLayer)
    sKeys = subtypes.keys()
    for keys in sKeys:
        if keys != 0:
            print("Subtype found at code {}.".format(keys))
            sys.stdout.flush()
            arcpy.RemoveSubtype_management(tempLayer,keys)
        else:
            print("No subtypes found.")
            pass  
        
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = newVar + "USIC.shp"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
    print("A shapefile has been copied as {}.".format(shpPathFull))
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer)    

#------------------------CP Rectifier-------------------------------
  # Create the variables
    newVar = "cpRectifier"
    newVarPath = os.path.join(isGDB, newVar)
    # Change workspace  back to the tempSDE
    arcpy.env.workspace = inputWS
    
    # Copy features to new gdb
    print("Beginning to copy to {}.".format(newVarPath))
    Textvar = arcpy.CopyFeatures_management('GISADMIN.Gas\GISADMIN.CPRectifier',\
                                            newVarPath)
    
# Use a temporary feature layer to edit annotation
    arcpy.env.workspace = isGDB
    tempLayer = arcpy.MakeFeatureLayer_management(newVar, 'temp_lyr')
    print("\n Temp layer created.")

    # Create a list of variables to save
    keepList = ['LOCATIONDESCRIPTION','RECTIFIERNAME','RECTIFIERTYPE',\
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
        
    # Subtypes prevent deletion of a field. This section strips subtypes from
    # all variables in dellist.
    # An Error can result if the code tries to remove subtypes from an FC and
    # finds none. That is why the if statement is used.
    subtypes = arcpy.da.ListSubtypes(tempLayer)
    sKeys = subtypes.keys()
    for keys in sKeys:
        if keys != 0:
            print("Subtype found at code {}.".format(keys))
            sys.stdout.flush()
            arcpy.RemoveSubtype_management(tempLayer,keys)
        else:
            print("No subtypes found.")
            pass  
        
    # Delete all features in deletion list
    arcpy.DeleteField_management(tempLayer, delList)
    
    # Set the new shapefile path variables
    shp = newVar + "USIC.shp"
    # Instead of using a full path, partials are used in case the pieces are
    # used seperately further in.
    shpPathFull = os.path.join(shpPath, shp)
    
    # If the shapefile already exists, delete it
    if arcpy.Exists(shpPathFull):
        arcpy.Delete_management(shpPathFull)
    else:
        pass
    
    # Copy the temp layer to a new shapefile.
    arcpy.CopyFeatures_management(tempLayer, shpPathFull)
    print("A shapefile has been copied as {}.".format(shpPathFull))
    
    # Delete variables that will get re-used in the next section
    del keepList, delList, shp, shpPathFull
    # Delete the temporary layer
    arcpy.Delete_management(tempLayer) 
    
    


    # When done, remove the temp path containing the connection files
    shutil.rmtree(sdeTempPath)
except:
    shutil.rmtree(sdeTempPath)
    print("Deleting temp SDE.")
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" \
            + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"    
    log.write("" + pymsg + "\n")
    log.write("" + msgs + "")
    print(msgs)
    log.close()