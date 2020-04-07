# Project: Spire to USIC data compilation
# Create Date: 02/13/2020
# Last Updated: 04/07/2020
# Create by: Brad Craddick & Robert Domiano
# Updated by: Robert Domiano
# Purpose: To provide a clean set of MO East, MO West, and Alabama to USIC
# ArcGIS Version:   10.3
# Python Version:   2.7.5
# For a changelog of updates, visit the github at: https://github.com/SpireBadger/USIC
# -----------------------------------------------------------------------

# Import modules
import sys, arcpy, datetime, traceback
import os
import shutil


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
   
def copyFeature(shpName, sdeConnect, keepList, inputFC, sqlQ='#'):
    """
    This function creates a shapefile based on an input
    feature class within a Spire SDE while using a list of
    field names to keep. 
    
    It optionally can take a SQL query to take only certain
    features from the original feature class.
    """
    # Set the workspace to the sdeConnect variable given. Get output is used as
    # a string to path avoids some issues.
    wsConnect = sdeConnect.getOutput(0)
    arcpy.env.workspace = wsConnect
    # Empty field mapping object created
    fmap = arcpy.FieldMappings()
    # The input FC is added to the field mappings object
    fmap.addTable(inputFC)
    # Get all fields
    fields = {f.name: f for f in arcpy.ListFields(inputFC)}
    # Clean up field map based on keep list
    for fname, fld in fields.iteritems():
       if fld.type not in ('OID', 'Geometry') and 'shape' not in fname.lower():
          if fname not in keepList:
#             print("Field name {0} is not on the Keep List and will be removed.".format(fname))
             fmap.removeFieldMap(fmap.findFieldMapIndex(fname))
    # A list of current Spire USIC Directories and areas
    paths = ['SpireAL','SpireMOEast','SpireMoWest']
    # Set the pdf pathway
    pdfN="_FieldNotePDF"   
    # Set variable to the path declared in script
    # TO CHANGE WHAT DIRECTORY THIS CREATES THE BASE FILES IN, POINT THIS 
    # VARIABLE TO DESIRED DIRECTORY.
    setPath = r"\\pdatfile01\ProdData\GIS\USIC"
    # Global variables for the folder directories are created for use outside
    # the function
    global shpPath,USICpdf
    # Determine what SDE is being used and set shpPath to point to a matching
    # directory to store shapefiles in.
    if sdeConnect == sdeAL:
        print("Connecting to the {0} SDE.".format(paths[0]))
        shpPath = os.path.join(setPath, paths[0])
        USICpdfPath = paths[1] + pdfN
        USICpdf = os.path.join(sdeTempPath, USICpdfPath)
    elif sdeConnect == sdeMOE or sdeConnect == sdeMOEPoly:
        shpPath = os.path.join(setPath, paths[1])
        print("Connecting to the {0} SDE.".format(paths[1]))
        USICpdfPath = paths[1] + pdfN
        USICpdf = os.path.join(sdeTempPath, USICpdfPath)
    elif sdeConnect == sdeMOW or sdeConnect == sdeMOWPoly:
        shpPath = os.path.join(setPath, paths[2])
        print("Connecting to the {0} SDE.".format(paths[2]))
        USICpdfPath = paths[2] + pdfN
        USICpdf = os.path.join(sdeTempPath, USICpdfPath)
    # Prior to using the directory, test to see if it exists.
    # If it does not, create a new directory based on that name. 
    if not os.path.exists(shpPath):
        os.mkdir(shpPath)
        print("No folder for shapefiles. A directory has been created at {0}.".format(shpPath))
    if not os.path.exists(USICpdf):
        os.mkdir(USICpdf)
    # Delete any existing shapefile to avoid overwrite issues
    doesEx = os.path.join(shpPath, shpName + ".shp")
    if arcpy.Exists(doesEx):
        arcpy.Delete_management(doesEx)
    # Create the new shapefile to be sent to locator company
    # newSHP is made global so it can be used in Distribution Main/Services/WO Polys
    global newSHP
    newSHP = arcpy.conversion.FeatureClassToFeatureClass(inputFC, shpPath, shpName,\
                                                sqlQ, fmap)
    print("Shapefile has been created in {0}.".format(newSHP))
    print("\n")
    # Delete inputs to prepare for next shapefile
    del shpName, keepList, inputFC, sdeConnect
    # return none
    return
                                                                                               
# Set unbuffered mode
sys.stdout = Unbuffered(sys.stdout)
try:
    # set datetime variable
    d = datetime.datetime.now()
    sdeTempPath = r"C:\TempUSIC"
    if not os.path.exists(sdeTempPath):
        os.mkdir(sdeTempPath)
        print("Temporary directory not found. A new directory has been " + \
              "created at {0}.".format(sdeTempPath))
    else:
        print("The temp USIC directory already exists at {0} and will be used.".format(sdeTempPath))    

    # open log file for holding errors
    # will also create file if not already there
    log = open("C:\TempUSIC\LogFile.txt","a")
    log.write("----------------------------" + "\n")
    log.write("----------------------------" + "\n")
    # write datetime to log
    log.write("Log: " + str(d) + "\n")
    log.write("\n")

# -----------------------Variable setup---------------------------------------

    # set arcpy environment to allow overwriting
    arcpy.env.overwriteOutput=True        
    # Set environment to transport subtype descriptions
    arcpy.env.transferDomains = True
#--------------------Create SDE Connections------------------------------------
    # Connecting to an existing SDE doesn't seem to work unless the connection
    # is already in place.
    # This is a work around to deal with that issue and avoid needing to connect
    # ahead of time outside the script.
    
    sdeMOE = arcpy.CreateDatabaseConnection_management(sdeTempPath, 'tempMOEServ.sde', \
                                              'ORACLE', 'stl-pgisdb-20:1526/PGISE',\
                                              'DATABASE_AUTH', 'IMAPVIEW', \
                                              'ue2Y6vwm','SAVE_USERNAME')
    print("Database connection created at {0} to the Mo East Oracle Database."\
          .format(sdeTempPath))
    
       # Create the MO West SDE Connection
    sdeMOW = arcpy.CreateDatabaseConnection_management(sdeTempPath, 'tempMOWServ.sde', \
                                              'ORACLE', 'stl-pgisdb-21.lac1.biz:1521/PGISM',\
                                              'DATABASE_AUTH', 'IMAPVIEW', \
                                              'ue2Y6vwm','SAVE_USERNAME')
    print("Database connection created at {0} to the MO West Oracle Database."\
          .format(sdeTempPath))   
    sdeAL = arcpy.CreateDatabaseConnection_management(sdeTempPath,'tempALServ.sde',\
                                                      'ORACLE',\
                                                      'xs-bhm-dgp-1.energen.com:1521/gsp',\
                                                      'DATABASE_AUTH', 'GISADMIN',\
                                                      'gisadmin','SAVE_USERNAME')
    print("Database connection created at {0} to the Alabama Database."\
          .format(sdeTempPath))
    
    #Mo East WO Polygons are stored in a different SDE than gas facilities.
    # This SDE connection sets that up.
    sdeMOEPoly = arcpy.CreateDatabaseConnection_management(sdeTempPath, 'tempMOE_Poly.sde', \
                                              'ORACLE', 'pgisdb02:1523/pgis3',\
                                              'DATABASE_AUTH', 'mxviewer', \
                                              'mxviewer','SAVE_USERNAME')
    print("Database connection created at {0} to the Mo East WO Poly Database."\
          .format(sdeTempPath))

    sdeMOWPoly = arcpy.CreateDatabaseConnection_management(sdeTempPath, 'tempMOW_Poly.sde', \
                                              'ORACLE', 'pgisdb02.lac1.biz:1523/pgis3',\
                                              'DATABASE_AUTH', 'mxviewer', \
                                              'mxviewer','SAVE_USERNAME')
    print("Database connection created at {0} to the Mo West WO Poly Database."\
          .format(sdeTempPath))
    print("\n")    
    
#----------------------------AL Setup----------------------------------------
#---------Dimension Text-------------------------------------------------------
    # Only this first shapefile will be commented, all others follow the same format unless otherwise
    # noted in comments
      # Set the shapefile name
    shpName = "mainText"
     # Set variable to a path of where the input Feature class is located.
     # getOutput is used to force sdeAL path to be a string.
     # sdeAL is used in case the sdeTempPath is changed to limit number of changes needed in the script.
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.MainText'
   # Create a list of all field names to be kept.     
    keepList = ['TextString', 'FontSize', 'Angle']
   # Run the copyFeature function to create the shapefile.     
    copyFeature(shpName,sdeAL,keepList,inputFC)

#---------Distribution Main-------------------------------------------------------
    shpName = "main"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.Main'
    keepList = ['INSTALLDATE','MEASUREDLENGTH','LENGTHSOURCE','COATINGTYPE',\
                'NOMINALPIPESIZE','PIPEGRADE','PRESSURECODE',\
                'MATERIALCODE','LABELTEXT','TRANSMISSION_FLAG',\
                'LOCATIONDESCRIPTION','PLASTICTYPE','PROJECTYEAR',\
                'MANUFACTURER','LENGTHMX']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##---------Regulator Station----------------------------------------------------
    shpName = "RegulatorStation"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.RegulatorStation'
    keepList = ['INSTALLDATE','LOCATIONDESCRIPTION','ROTATIONANGLE',\
                'COMMENTS', 'MAXINLETPRESSURE', 'MAXOUTLETPRESSURE',\
                'SUBTYPE','SETTINGNAME']
    copyFeature(shpName,sdeAL,keepList,inputFC)
#    
##---------Abandoned Main----------------------------------------------------
    shpName = "AbandonedMain"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.AbandonedMain'
    keepList = ['MEASUREDLENGTH', 'COATINGTYPE', \
                'NOMINALPIPESIZE', 'MATERIAL','DATEABANDONED', 'LABELTEXT']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
#---------Valves----------------------------------------------------
    shpName = "Valves"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.Valve'
    keepList = ['INSTALLDATE', 'COMMENTS', 'HOUSEDIN', \
                'MATERIAL', 'INSULATEDINDICATOR', 'VALVEENDS', 'VALVETYPE', \
                'VALVEUSE', 'ROTATIONANGLE', 'VALVEMATERIAL', 'VALVESIZE', \
                'LABELTEXT','TURNSTOCLOSE','DATECREATED','DATEMODIFIED'\
                'LOCATIONDESCRIPTION']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
#---------Casing----------------------------------------------------
    shpName = "Casing"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.Casing'
    keepList = ['MEASUREDLENGTH', 'CASINGCOATINDICATOR',\
                'CASINGSIZE', 'CASINGMATERIAL','LABELTEXT']
    copyFeature(shpName,sdeAL,keepList,inputFC)
#---------Drips----------------------------------------------------
    shpName = "Drips"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.Drip'
    keepList = ['LOCATIONDESCRIPTION', 'INSTALLDATE','LABELTEXT']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
#---------Marker Ball----------------------------------------------------
    shpName = "ElectronicMarker"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.ElectronicMarker'
    keepList = ['INSTALLDATE', 'DISTANCE1','DIRECTION1',\
                'LOCATION1','BUILDING1','STREET1','DISTANCE2','DIRECTION2',\
                'LOCATION2','BUILDING2','STREET2']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
#---------First Cut Regulator----------------------------------------------------
    shpName = "FirstCutRegulator"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.FirstCutRegulator'
    keepList = ['LOCATIONDESCRIPTION','ROTATIONANGLE','INSTALLDATE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
#---------Fittings----------------------------------------------------
    shpName = "Fittings"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.Fitting'
    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
#---------Services----------------------------------------------------
    shpName = "Services"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.Service'
    keepList = ['INSTALLDATE','MEASUREDLENGTH','LENGTHSOURCE','COATINGTYPE',\
                'PIPETYPE','NOMINALPIPESIZE','PIPEGRADE','PRESSURECODE',\
                'MATERIALCODE','LABELTEXT','TRANSMISSION_FLAG',\
                'LOCATIONDESCRIPTION','HIGHDENSITYPLASTIC','PROJECTYEAR',\
                'PROJECTNUMBER','SERVICETYPE','MANUFACTURER','LENGTH604',\
                'STREETADDRESS','MAINMATERIAL']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
#---------Stopper Fitting----------------------------------------------------
    shpName = "StopperFitting"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.StopperFitting'
    keepList = ['INSTALLDATE','LABELTEXT','LOCATIONDESCRIPTION','PRESENTPOSITION']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
#---------Premises----------------------------------------------------
    shpName = "Premise"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Historical\GISADMIN.Premise'
    keepList = ['INSTALLIONDATE','PIPENAME','LOCATIONDESCRIPTION',\
                'PIPEID','MANUFACTURER']
    copyFeature(shpName,sdeAL,keepList,inputFC)

#---------CP Rectifier----------------------------------------------------
    shpName = "CPRectifier"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.CPRectifier'
    keepList = ['LOCATIONDESCRIPTION','RECTIFIERNAME','RECTIFIERTYPE',\
                'LABELTEXT']
    copyFeature(shpName,sdeAL,keepList,inputFC) 

##------------------------Abandon Services--------------------------------------     
    shpName = "abandonService"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.AbandonedService'
    keepList = ['NOMINALSIZE','MATERIALCODE','DATEABANDONED','LABELTEXT',\
                'RETIREMENTPROJECTNUMBER']
    copyFeature(shpName,sdeAL,keepList,inputFC)

##------------------------CP Anode-------------------------------------- -------      
    shpName = "CPAnode"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.CPAnode'
    keepList = ['DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','LEADCOLOR','PROTECTIONDIRECTION',\
                'BOXTYPE','LOCATIONDESCRIPTION']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------CP Test Point-------------------------------------- -------      
    shpName = "CPTestPoint"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.CPTestPoint'
    keepList = ['COMMENTS','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','LEADCOLOR','LEADDIRECTION','BOXTYPE',\
                'STATIONTYPE','LOCATIONDESCRIPTION']
    copyFeature(shpName,sdeAL,keepList,inputFC)

##------------------------Service Text--------------------------------- -------   
    shpName = "serviceText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.ServiceText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC) 
    
##------------------------Misc Text--------------------------------- ----------- 
    shpName = "MiscellaneousText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Landbase\GISADMIN.MiscellaneousText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Project Boundary------------------------- ----------- 
    shpName = "ProjectBoundary"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.ProjectData\GISADMIN.ProjectBoundary'
    keepList = ['DESCRIPTION','STATUS','PROJECTNUMBER']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Casing Text------------------------- ----------- 
    shpName = "casingText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.CasingText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC) 
    
##------------------------Valve Text------------------------- ----------- 
    shpName = "valveText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.ValveText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Fitting Text------------------------- ----------- 
    shpName = "fittingText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.FittingText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Retired Main Text------------------------- ----------- 
    shpName = "RetiredMainText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.RetiredMainText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Retired Service Text------------------------- ----------- 
    shpName = "RetiredServiceText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.RetiredServiceText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Regulator Station Text------------------------- ----------- 
    shpName = "regStationText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.RegulatorStationText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
###------------------------Leader Lines------------------------- -----
    shpName = "LeaderLines"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Landbase\GISADMIN.LeaderLine'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
###------------------------Leader Lines------------------------- -----
    shpName = "HookLeader"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Landbase\GISADMIN.HookLeader'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Stopper Fitting Text------------------------- ----------- 
    shpName = "stopperFittingText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.StopperFittingText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)

##------------------------Location Description Text------------------------- -------
    shpName = "LocationMeasurement"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Landbase\GISADMIN.locationMeasurement'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)

##------------------------Station Plus Text------------------------- -------
    shpName = "StationPlus"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Landbase\GISADMIN.StationPlus'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)

##------------------------Detail Annotation Text------------------------- -------
    shpName = "DetailAnnotation"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Landbase\GISADMIN.DetailAnnotation'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Notes Text------------------------- -------
    shpName = "Notes"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Landbase\GISADMIN.Notes'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Main Authorization Number Text-----------------------
    shpName = "mainAuthorizationNumberText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.MainAuthorizationNumberText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)    
    
##------------------------Gas Lamp------------------------- ----------- 
    shpName = "gasLamp"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.GasLamp'
    keepList = ['SYMBOLROTATION','STREET_NUMBER','STREET_NAME','STREET_SUFFIX']
    copyFeature(shpName,sdeAL,keepList,inputFC)

##------------------------Customer------------------------- ----------- 
    shpName = "customer"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.CCSData\GISADMIN.Customer'
    keepList = ['METERLOCATION','ADDRESS']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##############################   MISSOURI EAST    ############################### 
##
###------------------------MoNat Dimension Text--------------------- ----------- 
    shpName = "DimMoNatTextUSICMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_LAND.Landbase\LGC_LAND.MoNatDimText'
    keepList = ['SYMBOLROTATION','DIMENSION','COUNTY']
    copyFeature(shpName,sdeMOE,keepList,inputFC)
    
##------------------------Marker Ball--------------------- ----------- 
    shpName = "MarkerBallUSICMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.LocationIndicator'
    keepList = ['COMMENTS','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','LOCATION3','INSTALL_DATE','INSTALLED_ON',\
                'OWNER','MARKERTYPE', 'SUBTYPECD','FULLTEXT']
    copyFeature(shpName,sdeMOE,keepList,inputFC)
    
##------------------------MoNat Dimension Line--------------------- ----------- 
    shpName = "DimLineMoNatUSICMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_LAND.Landbase\LGC_LAND.MoNatDimLine'
    keepList = ['OWNER']
    copyFeature(shpName,sdeMOE,keepList,inputFC)

##------------------------Distribution Main Dimension--------------------- ----------- 
    shpName = "DistributionMainDimUSICMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.DistributionMainDimension'
    keepList = ['LOCATION','SYMBOLROTATION','DISTANCE','COVER']
    copyFeature(shpName,sdeMOE,keepList,inputFC)     
    
##------------------------Service Points--------------------------- ----------- 
    shpName = "ServicePointUSICMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.ServicePoint'
    keepList = ['CUSTOMERTYPE','SERVICEMXLOCATION','SERVICESTATUS','DISCLOCATION',\
                'STREETADDRESS','METERLOCATIONDESC','METERLOCATION','MXSTATUS']
    copyFeature(shpName,sdeMOE,keepList,inputFC)

##------------------------Test Points--------------------------- ----------- 
    shpName = "AnodeUSICMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.CPTestPoint'
    keepList = ['COMMENTS','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','LEADCOLOR','LEADDIRECTION','BOXTYPE',\
                'STATIONTYPE','LOCATIONDESCRIPTION','SYMBOLROTATION','SUBTYPECD',\
                'OPERATINGPRESSURE','LOCATION1MX','LOCATION2MX','ADDITIONALINFO',\
                'CPSIZE','HOUSENUM','STREETNAME']
    copyFeature(shpName,sdeMOE,keepList,inputFC)     
    
##------------------------Ctrl Fittings--------------------------- ----------- 
    shpName = "ControllableFittingUSICMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.ControllableFitting'
    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','SUBTYPECD','COVER','SYMBOLROTATION']
    copyFeature(shpName,sdeMOE,keepList,inputFC)  

##------------------------nON-Ctrl Fittings--------------------------- ----------- 
    shpName = "NonControllableFittingMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.NonControllableFitting'
    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','SUBTYPECD','COVER','SYMBOLROTATION']
    copyFeature(shpName,sdeMOE,keepList,inputFC)
    
##------------------------abandoned Services--------------------------- ----------- 
    shpName = "AbandonedGasServiceUSICMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.AbandonedGasService'
    keepList = ['SUBTYPECD','NOMINALDIAMETER','MATERIAL','FIELDBOOKPATH',\
                'MXSTREETADDRESS','MXTEELOCATION','MXCURBBOXLOCATION',\
                'MXCURBDESCRIPTION','MXSERVICELOCATION','MXRISERLOCATION',\
                'MXRISERDESCRIPTION','MXMAINLOCATION','MXMAINSIZE','MXMAINMATERIAL',\
                'DATECREATED','DATEMODIFIED','OPERATINGPRESSURE','STREETNUMBER',\
                'STREETNAME','STREETSUFFIX','ONE_HUNDRED_FOOT_DISPLAY','REASON']
    copyFeature(shpName,sdeMOE,keepList,inputFC)
    
##------------------------Valves--------------------------- ----------- 
    shpName = "GasValveMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.GasValve'
    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','SUBTYPECD','COVER','SYMBOLROTATION'\
                'DIRECTION1MX','DIRECTION2MX','MXLOCATION','COVER','SUBTYPECD','COMMENTS',\
                'MATERIAL','MATERIALMX','VALVEDIAMETER','VALVETYPE','VALVEUSE',\
                'CLOCKWISETOCLOSE','NORMALPOSITION','NONESSENTIAL','NUMBEROFTURNS',\
                'VALVENUMBER','VALVELOCATION1','VALVELOCATION2','VALVELOCATION3',\
                'FITTINGNUMBER']
    copyFeature(shpName,sdeMOE,keepList,inputFC)
    
##------------------------Drips--------------------------- ----------- 
    shpName = "DripMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.Drip'
    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','SUBTYPECD','COVER','SYMBOLROTATION'\
                'DIRECTION1MX','DIRECTION2MX','MXLOCATION','COVER','SUBTYPECD','COMMENTS',\
                'MATERIAL','DRIPTYPE','CONNECTYPE','OFFSET']
    copyFeature(shpName,sdeMOE,keepList,inputFC)
    
###------------------------Distribution Main----------------------- -----------
    ## Distribution main is unique and requires more manipulation to produce. 
    shpName = "DistributionMainUSICMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.DistributionMain'
    keepList = ['MXLOCATION','NOMINALDIAMETER','JOINTTRENCH','DATEINSTALLED',\
                'LENGTHMX','MATERIALMX','MATERIAL','FIELDBOOKPATH',\
                'OPERATINGPRESSURE','COATINGTYPE','RELAYEDSIZE','RELAYEDMATERIAL']
    # Distribution main that belongs to Spire is the only main we want for the 
    # final SHP. This sql expression helps to secure that.
    sqlQ=r"NOT OWNER in ( 'Southern Star', 'MRT') AND NOT OWNER IS NULL"
    copyFeature(shpName, sdeMOE, keepList, inputFC, sqlQ)
    
    # Set the workspace to the shapefile folder 
    arcpy.env.workspace = shpPath
    # Add a new field for FieldNote to the newly created shapefile
    arcpy.AddField_management(newSHP,"FieldNote","TEXT","#","#","200","#",\
                              "NULLABLE","NON_REQUIRED","#")
    print("New field created for FieldNote.")
    # Iterate through the newly created field and FIELDBOOKP                          
    with arcpy.da.UpdateCursor(newSHP, ['FIELDBOOKP', 'FieldNote']) as cursor:
        for row in cursor:
            # This sets any blank or null fieldbookpaths to none
            if row[0] == " " or row[0] is None:
#                print("Row being updated from blank to None.")
                none = "None"
                row[0] = none
                cursor.updateRow(row)
            if row[0].rfind('\\') > 0:
                # Find the exact location of last \\
                slashes=row[0].rfind('\\')
                # Add one to the location of the start, to keep everything after the first \
                slashIndx= slashes+1
                # Count the total length of string
                charCount=len(row[0])
                # 
                ok=row[0][slashIndx:charCount]
                # Strip out everything before the last \ and store the remainder in a variable
                ok2 = ok.strip()
                row[1] = ok2
                cursor.updateRow(row)
            if row[0].rfind('/') > 0:
                thats=row[0].rfind('/')
                that1= thats+1
                theother=len(row[0])
                ok=row[0][that1:theother]
                ok2=ok.strip()
                these=row[0].replace(str(that1),'')
                row[1] = ok2
                cursor.updateRow(row)
    # Clean up the cursor object                        
    del cursor
###-----------------------------Create Main PDF Folder-------------------------
    # Copy pdfs of field books modified in the last 14 days.
    # Set current date variable
    CUR_DATE = datetime.date.today().strftime('%Y-%m-%d')
    # set date variable 14 days back from current d ate
    d = datetime.date.today() - datetime.timedelta(days=14)
    # Set a sql query using dates
    query='"DATEINSTAL" <= date '+"'"+CUR_DATE+"' AND "+'"DATEINSTAL" >= date '+"'"+str(d)+"'"

#   Set the workspace to the new pdf folder.
    arcpy.env.workspace = USICpdf
    
    # Create a list of any existing pdfs. If present, delete them.
    for csv_file in (arcpy.ListFiles("*.pdf") or []):
        print("Deleting existing PDFs.")
        os.remove(USICpdf+"\\"+csv_file)

    # Create a search cursor for the feature layer
    # for each row in the cursor based on the time query
    with arcpy.da.SearchCursor(newSHP, ['FIELDBOOKP', 'DATEINSTAL'], query) as cursor:
        print("Searching for PDFs.")
        for row in cursor:
            print row[0]
#            print row[1]
            if row[0] <> 'None' and arcpy.Exists(row[0]):
                shutil.copy2(row[0], USICpdf)
            else:
                print("Row is blank.")
    del cursor
    # Delete the fieldbook path as its no longer needed
    arcpy.DeleteField_management(newSHP,"FIELDBOOKP")
    
#------------------------Services----------------------- ---------------------
    shpName = "ServiceUSICMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.Service'
    keepList = ['OWNER','DATECREATED','MXSTATUS','STREETADDRESS','SERVICETYPE',\
                'BRANCHTYPE','SERVICENUMBER','FIELDBOOKPATH','TEELOCATION',\
                'TEEDESCRIPTION','CURBBOXLOCATION','SERVICELOCATION',\
                'RISERLOCATION','RISERDESCRIPTION','MAINLOCATION','MAINDEPTH',\
                'MAINSIZE','MAINMATERIAL','EFV','SUBTYPECD','MXLOCATION']
    sqlQ=r"(NOT FIELDBOOKPATH IS null AND NOT FIELDBOOKPATH = 'NO FIELDBOOK' ) OR( OWNER = 'MoNat')"
    copyFeature(shpName, sdeMOE, keepList, inputFC, sqlQ)
    
    arcpy.env.workspace = shpPath
    arcpy.AddField_management(newSHP,"FieldNote","TEXT","#","#","200","#",\
                              "NULLABLE","NON_REQUIRED","#")
    print("New field created for FieldNote.")                          
    with arcpy.da.UpdateCursor(newSHP, ['FIELDBOOKP', 'FieldNote']) as cursor:
        for row in cursor:
            if row[0] == " " or row[0] is None:
#                print("Row being updated from blank to None.")
                none = "None"
                row[0] = none
                cursor.updateRow(row)
            if row[0].rfind('\\') > 0:
                # Find the exact location of last \\
                slashes=row[0].rfind('\\')
                # Add one to the location of the start, to keep everything after the first \
                slashIndx= slashes+1
                # Count the total length of string
                charCount=len(row[0])
                # 
                ok=row[0][slashIndx:charCount]
                # Strip out everything before the last \ and store the remainder in a variable
                ok2 = ok.strip()
                row[1] = ok2
                cursor.updateRow(row)
            if row[0].rfind('/') > 0:
                thats=row[0].rfind('/')
                that1= thats+1
                theother=len(row[0])
                ok=row[0][that1:theother]
                ok2=ok.strip()
                these=row[0].replace(str(that1),'')
                row[1] = ok2
                cursor.updateRow(row)                        
    del cursor
###-----------------------------Create Service PDFs-------------------------
    # Copy pdfs of field books modified in the last 14 days.
    # Set current date variable
    CUR_DATE = datetime.date.today().strftime('%Y-%m-%d')
    # set date variable 14 days back from current d ate
    d = datetime.date.today() - datetime.timedelta(days=14)
    # Set a sql query using dates
    query='"DATECREATE" <= date '+"'"+CUR_DATE+"' AND "+'"DATECREATE" >= date '+"'"+str(d)+"'"

#   Set the workspace to the new pdf folder.
    arcpy.env.workspace = USICpdf
            
    # Create a search cursor for the feature layer
    # for each row in the cursor based on the time query
    with arcpy.da.SearchCursor(newSHP, ['FIELDBOOKP', 'DATECREATE'], query) as cursor:
        print("Searching for PDFs.")
        for row in cursor:
            print row[0]
#            print row[1]
            if row[0] != 'NO FIELDBOOK' and arcpy.Exists(row[0]):
                print("Creating a pdf for {0}.".format(row[0]))
                shutil.copy2(row[0], USICpdf)
            elif row[0].find(r'\\gisappser2\images') > 0 and row[0] != 'NO FIELDBOOK'and row[0] != r'\\gisappser2\images\Laclede Gas\pdf\pdf 2B checked\Laclede\1643-75.pdf':
                print("PDF found in images.")
                shutil.copy2(row[0], USICpdf)                
            else:
                print("Row for {0} is blank or the PDF cannot be found.".format(row[0]))
    del row, cursor
    arcpy.DeleteField_management(newSHP,"FIELDBOOKP")
###-----------------------------Abandoned Main-------------------------    
    shpName = "AbandonedGasPipeUSICMoEast"
    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.AbandonedGasPipe'
    keepList = ['OWNER','DATECREATED','DATEMODIFIED','RETIREDATE','REASON',\
                'FIELDBOOKPATH','MATERIALMX','NOMINALDIAMETER','MATERIAL',\
                'WORKREQUESTID','OPERATINGPRESSURE','JOINTTRENCH','DATEINSTALLED',\
                'COATINGTYPE','MAINTYPE','COUNTY']
    copyFeature(shpName, sdeMOE, keepList, inputFC)
    
    arcpy.env.workspace = shpPath
    arcpy.AddField_management(newSHP,"FieldNote","TEXT","#","#","200","#",\
                              "NULLABLE","NON_REQUIRED","#")
    print("New field created for FieldNote.")                          
    with arcpy.da.UpdateCursor(newSHP, ['FIELDBOOKP', 'FieldNote']) as cursor:
        for row in cursor:
            if row[0] == " " or row[0] is None:
#                print("Row being updated from blank to None.")
                none = "None"
                row[0] = none
                cursor.updateRow(row)
            if row[0].rfind('\\') > 0:
                # Find the exact location of last \\
                slashes=row[0].rfind('\\')
                # Add one to the location of the start, to keep everything after the first \
                slashIndx= slashes+1
                # Count the total length of string
                charCount=len(row[0])
                # 
                ok=row[0][slashIndx:charCount]
                # Strip out everything before the last \ and store the remainder in a variable
                ok2 = ok.strip()
                row[1] = ok2
                cursor.updateRow(row)
            if row[0].rfind('/') > 0:
                thats=row[0].rfind('/')
                that1= thats+1
                theother=len(row[0])
                ok=row[0][that1:theother]
                ok2=ok.strip()
                these=row[0].replace(str(that1),'')
                row[1] = ok2
                cursor.updateRow(row)                        
    del cursor
##------------------------Wo Polygons--------------------------- -----------
    shpName = "WorkOrderUSIC"
    inputFC = sdeMOEPoly.getOutput(0) + '\MXSPAT.WOPoly'
    keepList = ['STATUS','MXWONUM','WORKTYPE','DESCRIPTION','ZLAC_SUBWORKTYPE',\
                'ACTFINISH']
    sqlQ = r"STATUS in ( 'RJCTDFCOMP', 'FCOMP', 'GISREVW', 'WFFILE','CONTRCOMP', 'INPRG', 'LSNC','DISPATCH','ENROUTE','ASBUILTWAPPR','RJCTDASBUILTCOMP','CONTINST','RJCTDASBILTWAPPR','RJCTDWASBUILT','WASBUILT')"
    copyFeature(shpName, sdeMOEPoly, keepList, inputFC, sqlQ)
#    arcpy.env.workspace = shpPath
#    projSHP = shpName + "Proj.shp"
#    print("Projecting {0} to {1}.".format(newSHP, projSHP))
#    arcpy.Project_management(newSHP,projSHP,\
#                             "PROJCS['NAD_1983_StatePlane_Missouri_West_FIPS_2403_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',2788708.333333333],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-94.5],PARAMETER['Scale_Factor',0.9999411764705882],PARAMETER['Latitude_Of_Origin',36.16666666666666],UNIT['Foot_US',0.3048006096012192]]",\
#                             "'WGS_1984_Major_Auxiliary_Sphere_To_WGS_1984 + WGS_1984_(ITRF00)_To_NAD_1983'",\
#                             "PROJCS['WGS_1984_Web_Mercator',GEOGCS['GCS_WGS_1984_Major_Auxiliary_Sphere',DATUM['D_WGS_1984_Major_Auxiliary_Sphere',SPHEROID['WGS_1984_Major_Auxiliary_Sphere',6378137.0,0.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],UNIT['Meter',1.0]]")
#    print("Deleting the wrongly projected {0} shapefile.".format(newSHP))
#    arcpy.Delete_management(newSHP)
############################   MISSOURI WEST    ###############################      
#------------------------Marker Ball--------------------- ----------- 
    shpName = "MarkerBallUSIC"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.LocationIndicator'
    keepList = ['COMMENTS','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','LOCATION3','INSTALL_DATE','INSTALLED_ON',\
                'OWNER','MARKERTYPE', 'SUBTYPECD','FULLTEXT']
    copyFeature(shpName,sdeMOW,keepList,inputFC)
##------------------------Drips--------------------------- ----------- 
    shpName = "Drip"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.Drip'
    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','SUBTYPECD','COVER','SYMBOLROTATION'\
                'DIRECTION1MX','DIRECTION2MX','MXLOCATION','COVER','SUBTYPECD','COMMENTS',\
                'MATERIAL','DRIPTYPE','CONNECTYPE','OFFSET']
    copyFeature(shpName,sdeMOW,keepList,inputFC)
    
##------------------------Distribution Main Dimension-------------------------
    shpName = "DistributionMainDimUSIC"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.DistributionMainDimension'
    keepList = ['LOCATION','SYMBOLROTATION','DISTANCE','COVER']
    copyFeature(shpName,sdeMOW,keepList,inputFC)        
 
##------------------------Service Points--------------------------- ----------- 
    shpName = "ServicePointUSIC"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.ServicePoint'
    keepList = ['CUSTOMERTYPE','SERVICEMXLOCATION','SERVICESTATUS','DISCLOCATION',\
                'STREETADDRESS','METERLOCATIONDESC','METERLOCATION','MXSTATUS'\
                ,'SERVICEPOINTTYPE','DIVISION','TOWN','SECTOR']   
    copyFeature(shpName,sdeMOW,keepList,inputFC)

    # Add a field for location length stored as a LONG
    
    arcpy.AddField_management(newSHP, "LOC", "LONG")
    expression = "getClass(!SERVICEMXL!)"
    codeBlock = """def getClass(SERVICEMXL):
        if 'MGEMAIN' in SERVICEMXL or len(SERVICEMXL) > 9 or SERVICEMXL == ' ':
            return 0
        else:
            return int(SERVICEMXL)"""     
    arcpy.CalculateField_management(newSHP, "LOC",expression, "PYTHON_9.3", codeBlock)

####------------------------Test Point-------------------------------------- -   
    shpName = "AnodeUSIC"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.CPTestPoint'
    keepList = ['DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','LEADCOLOR','PROTECTIONDIRECTION',\
                'BOXTYPE','LOCATIONDESCRIPTION','CPSIZE','SYMBOLDIRECTION',\
                'HOUSENUM','SUBTYPECD','STREETNAME','STATIONTYPE','PROTECTING',\
                'OPERATINGPRESSURE','REASON','LOCATION1MX','LOCATION2MX',\
                'ADDITIONALINFO','DIVISION','TOWN','SECTOR']
    copyFeature(shpName,sdeMOW,keepList,inputFC)   
    
####------------------------Rectifier-------------------------------------- --    
    shpName = "RectifierUSIC"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.CPRectifier'
    keepList = ['SUBTYPECD','DIVISION','TOWN','SECTOR','COMMENTS','FACILITYID',\
                'SYMBOLROTATION']
    copyFeature(shpName,sdeMOW,keepList,inputFC)
####------------------------ga fITTINGlINE------------------------------------   
    shpName = "GAFittingLineUSIC"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.GA_FittingLine'
    keepList = ['DETAIL','FID_LEGACY']
    copyFeature(shpName,sdeMOW,keepList,inputFC)
####------------------------GA Fitting Text-----------------------------------   
    shpName = "GAFittingTextUSIC"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.GA_FittingText'
    keepList = ['SUBTYPECD','DIVISION','TOWN','SECTOR','COMMENTS','FACILITYID',\
                'SYMBOLROTATION']
    copyFeature(shpName,sdeMOW,keepList,inputFC)
####------------------------Controllable Fittings-----------------------------     
    shpName = "ControllableFittingUSIC"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.ControllableFitting'
    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','SUBTYPECD','COVER','SYMBOLROTATION',\
                'DIVISION','TOWN','SECTOR']
    copyFeature(shpName,sdeMOW,keepList,inputFC)
####------------------------Non-Controllable Fittings-----------------------------    
    shpName = "NonControllableFittingUSIC"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.NonControllableFitting'
    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','SUBTYPECD','COVER','SYMBOLROTATION',\
                'DIVISION','TOWN','SECTOR','COVER','COMMENTS','STYLE']
    copyFeature(shpName,sdeMOW,keepList,inputFC)
    
##------------------------Wo Polygons--------------------------- -----------
    shpName = "WorkOrderUSIC"
    inputFC = sdeMOWPoly.getOutput(0) + '\MXSPAT.WOPoly'
    keepList = ['STATUS','MXWONUM','WORKTYPE','DESCRIPTION','ZLAC_SUBWORKTYPE',\
                'ACTFINISH']
    sqlQ = "STATUS in ( 'RJCTDFCOMP', 'FCOMP', 'GISREVW','WFFILE','CONTRCOMP', 'INPRG', 'LSNC','DISPATCH','ENROUTE','ASBUILTWAPPR','RJCTDASBUILTCOMP','CONTINST','RJCTDASBILTWAPPR','RJCTDWASBUILT','WASBUILT')"
    copyFeature(shpName, sdeMOWPoly, keepList, inputFC, sqlQ)
#    arcpy.env.workspace = shpPath
#    projSHP = shpName + "Proj.shp"
#    print("Projecting {0} to {1}.".format(newSHP, projSHP))
#    arcpy.Project_management(newSHP,projSHP,\
#                             "PROJCS['NAD_1983_StatePlane_Missouri_West_FIPS_2403_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',2788708.333333333],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-94.5],PARAMETER['Scale_Factor',0.9999411764705882],PARAMETER['Latitude_Of_Origin',36.16666666666666],UNIT['Foot_US',0.3048006096012192]]",\
#                             "'WGS_1984_Major_Auxiliary_Sphere_To_WGS_1984 + WGS_1984_(ITRF00)_To_NAD_1983'",\
#                             "PROJCS['WGS_1984_Web_Mercator',GEOGCS['GCS_WGS_1984_Major_Auxiliary_Sphere',DATUM['D_WGS_1984_Major_Auxiliary_Sphere',SPHEROID['WGS_1984_Major_Auxiliary_Sphere',6378137.0,0.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],UNIT['Meter',1.0]]")
#    print("Deleting the wrongly projected {0} shapefile.".format(newSHP))
#    arcpy.Delete_management(newSHP)
##------------------------Map Grid--------------------------- -----------    
    shpName = "MapGrid"
    inputFC = sdeMOW.getOutput(0) + '\LGC_LAND.Landbase\LGC_LAND.MapGrid'
    keepList = ['MAPID100','COUNTY','DISTRICT','DIVISION','TOWN','SECTOR']
    copyFeature(shpName,sdeMOW,keepList,inputFC)
##------------------------Valves----------------------------------------------- 
    shpName = "GasValve"
    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.GasValve'
    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','SUBTYPECD','COVER','SYMBOLROTATION'\
                'DIRECTION1MX','DIRECTION2MX','MXLOCATION','COVER','SUBTYPECD','COMMENTS',\
                'MATERIAL','MATERIALMX','VALVEDIAMETER','VALVETYPE','VALVEUSE',\
                'CLOCKWISETOCLOSE','NORMALPOSITION','NONESSENTIAL','NUMBEROFTURNS',\
                'VALVENUMBER','VALVELOCATION1','VALVELOCATION2','VALVELOCATION3',\
                'FITTINGNUMBER','TOWN','DIVISION','SECTOR']
    copyFeature(shpName,sdeMOW,keepList,inputFC)  
    
###-----------------------------Abandoned Main---------------------------------    
    shpName = "AbandonedGasPipeUSIC"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.AbandonedGasPipe'
    keepList = ['OWNER','DATECREATED','DATEMODIFIED','RETIREDATE','REASON',\
                'FIELDBOOKPATH','MATERIALMX','NOMINALDIAMETER','MATERIAL',\
                'WORKREQUESTID','OPERATINGPRESSURE','JOINTTRENCH','DATEINSTALLED',\
                'COATINGTYPE','MAINTYPE','COUNTY', 'DIVISION','TOWN','SECTOR']
    copyFeature(shpName, sdeMOW, keepList, inputFC)
    
    arcpy.env.workspace = shpPath
    arcpy.AddField_management(newSHP,"FieldNote","TEXT","#","#","200","#",\
                              "NULLABLE","NON_REQUIRED","#")
    print("New field created for FieldNote.")                          
    with arcpy.da.UpdateCursor(newSHP, ['FIELDBOOKP', 'FieldNote']) as cursor:
        for row in cursor:
            if row[0] == " " or row[0] is None:
#                print("Row being updated from blank to None.")
                none = "None"
                row[0] = none
                cursor.updateRow(row)
        del row, cursor
  
##------------------------abandoned Services--------------------------- ----------- 
    shpName = "AbandonedGasServiceUSIC"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.AbandonedGasService'
    keepList = ['SUBTYPECD','NOMINALDIAMETER','MATERIAL','FIELDBOOKPATH',\
                'MXSTREETADDRESS','MXTEELOCATION','MXCURBBOXLOCATION',\
                'MXCURBDESCRIPTION','MXSERVICELOCATION','MXRISERLOCATION',\
                'MXRISERDESCRIPTION','MXMAINLOCATION','MXMAINSIZE','MXMAINMATERIAL',\
                'DATECREATED','DATEMODIFIED','OPERATINGPRESSURE','STREETNUMBER',\
                'STREETNAME','STREETSUFFIX','ONE_HUNDRED_FOOT_DISPLAY','REASON'\
                'DIVISION','TOWN','SECTOR']
    copyFeature(shpName,sdeMOW,keepList,inputFC)
    
##------------------------Services---------------------------------------------
    shpName = "ServiceUSIC"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.Service'
    keepList = ['OWNER','DATECREATED','MXSTATUS','STREETADDRESS','SERVICETYPE',\
                'BRANCHTYPE','SERVICENUMBER','FIELDBOOKPATH','TEELOCATION',\
                'TEEDESCRIPTION','CURBBOXLOCATION','SERVICELOCATION',\
                'RISERLOCATION','RISERDESCRIPTION','MAINLOCATION','MAINDEPTH',\
                'MAINSIZE','MAINMATERIAL','EFV','SUBTYPECD','MXLOCATION',\
                'DIVISION','TOWN','SECTOR']
    sqlQ=("NOT FIELDBOOKPATH = 'NO FIELDBOOK'  OR OWNER = 'MoNat'")
    copyFeature(shpName, sdeMOW, keepList, inputFC, sqlQ)
    
    arcpy.env.workspace = shpPath
    arcpy.AddField_management(newSHP,"FieldNote","TEXT","#","#","200","#",\
                              "NULLABLE","NON_REQUIRED","#")
    print("New field created for FieldNote.")                          
    with arcpy.da.UpdateCursor(newSHP, ['FIELDBOOKP', 'FieldNote']) as cursor:
        for row in cursor:
            if row[0] == " " or row[0] is None:
#                print("Row being updated from blank to None.")
                none = "None"
                row[0] = none
                cursor.updateRow(row)
            if row[0].rfind('\\') > 0:
                # Find the exact location of last \\
                slashes=row[0].rfind('\\')
                # Add one to the location of the start, to keep everything after the first \
                slashIndx= slashes+1
                # Count the total length of string
                charCount=len(row[0])
                # 
                ok=row[0][slashIndx:charCount]
                # Strip out everything before the last \ and store the remainder in a variable
                ok2 = ok.strip()
                row[1] = ok2
                cursor.updateRow(row)
            if row[0].rfind('/') > 0:
                thats=row[0].rfind('/')
                that1= thats+1
                theother=len(row[0])
                ok=row[0][that1:theother]
                ok2=ok.strip()
                these=row[0].replace(str(that1),'')
                row[1] = ok2
                cursor.updateRow(row)                        
    del cursor

###-----------------------------Create Service PDFs-------------------------
    # Copy pdfs of field books modified in the last 14 days.
    # Set current date variable
    CUR_DATE = datetime.date.today().strftime('%Y-%m-%d')
    # set date variable 14 days back from current d ate
    d = datetime.date.today() - datetime.timedelta(days=14)
    # Set a sql query using dates
    query='"DATECREATE" <= date '+"'"+CUR_DATE+"' AND "+'"DATECREATE" >= date '+"'"+str(d)+"'"

#   Set the workspace to the new pdf folder.
    arcpy.env.workspace = USICpdf
    
    # Create a list of any existing pdfs. If present, delete them.
    for csv_file in (arcpy.ListFiles("*.pdf") or []):
        print("Deleting existing PDFs.")
        os.remove(USICpdf+"\\"+csv_file)
        
    # Create a search cursor for the feature layer
    # for each row in the cursor based on the time query
    with arcpy.da.SearchCursor(newSHP, ['FIELDBOOKP', 'DATECREATE'], query) as cursor:
        print("Searching for PDFs.")
        for row in cursor:
            print row[0]
#            print row[1]
            if row[0] != 'None' and arcpy.Exists(row[0]):
                print("Creating a pdf for {0}.".format(row[0]))
                shutil.copy2(row[0], USICpdf)          
            else:
                print("Row for {0} is blank or the PDF cannot be found.".format(row[0]))
    del row, cursor
    arcpy.DeleteField_management(newSHP,"FIELDBOOKP")
   
##------------------------Distribution Main----------------------- ---------------------
    shpName = "DistributionMainUSIC"
    inputFC = sdeMOW.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.DistributionMain'
    keepList = ['MXLOCATION','NOMINALDIAMETER','JOINTTRENCH','DATEINSTALLED',\
                'LENGTHMX','MATERIALMX','MATERIAL','FIELDBOOKPATH',\
                'OPERATINGPRESSURE','COATINGTYPE','RELAYEDSIZE','RELAYEDMATERIAL',\
                'MAOP','MOP','DIVISION','TOWN','SECTOR','WORKORDERNUMBER']
    sqlQ=("NOT DATEINSTALLED IS NULL AND NOT MXLOCATION = 'GMN001422772'" )
    copyFeature(shpName, sdeMOW, keepList, inputFC, sqlQ)
    
    arcpy.env.workspace = shpPath
    arcpy.AddField_management(newSHP,"FieldNote","TEXT","#","#","200","#",\
                              "NULLABLE","NON_REQUIRED","#")
    print("New field created for FieldNote.")                          
    with arcpy.da.UpdateCursor(newSHP, ['FIELDBOOKP', 'FieldNote', 'DATEINSTAL',\
                                        'WORKORDERN']) as cursor:
        for row in cursor:
            if row[0].strip() == "" or row[0] is None:
#                print("Row being updated from blank to None.")
                none = "None"
                row[0] = none
                cursor.updateRow(row)
            if row[0].rfind('\\') > 0:
                # Find the exact location of last \\
                slashes=row[0].rfind('\\')
                # Add one to the location of the start, to keep everything after the first \
                slashIndx= slashes+1
                # Count the total length of string
                charCount=len(row[0])
                # 
                ok=row[0][slashIndx:charCount]
                # Strip out everything before the last \ and store the remainder in a variable
                ok2 = ok.strip()
                row[1] = ok2
                cursor.updateRow(row)
            if row[0].rfind('/') > 0:
                thats=row[0].rfind('/')
                that1= thats+1
                theother=len(row[0])
                ok=row[0][that1:theother]
                ok2=ok.strip()
                these=row[0].replace(str(that1),'')
                row[1] = ok2
                cursor.updateRow(row)                        
    del cursor

###-----------------------------Create Distribution Main PDFs-------------------------
    # Copy pdfs of field books modified in the last 14 days.
    # Set current date variable
    CUR_DATE = datetime.date.today().strftime('%Y-%m-%d')
    # set date variable 14 days back from current d ate
    d = datetime.date.today() - datetime.timedelta(days=14)
    # Set a sql query using dates
    query='"DATEINSTAL" <= date '+"'"+CUR_DATE+"' AND "+'"DATEINSTAL" >= date '+"'"+str(d)+"'"

#   Set the workspace to the new pdf folder.
    arcpy.env.workspace = USICpdf
            
    # Create a search cursor for the feature layer
    # for each row in the cursor based on the time query
    with arcpy.da.SearchCursor(newSHP, ['FIELDBOOKP'], query) as cursor:
        print("Searching for PDFs.")
        for row in cursor:
            print row[0]
            if row[0] != 'None' and arcpy.Exists(row[0]):
                print("Creating a pdf for {0}.".format(row[0]))
                shutil.copy2(row[0], USICpdf)              
            else:
                print("PDF does not exist.")
    del row, cursor 
    arcpy.DeleteField_management(newSHP,"FIELDBOOKP")
    
    #Clean up the temp SDE connection
    arcpy.env.workspace = ""
    print("Removing temporary SDE Connection Files.")
    os.remove(sdeAL.getOutput(0))
    os.remove(sdeMOE.getOutput(0))
    os.remove(sdeMOW.getOutput(0))
    os.remove(sdeMOEPoly.getOutput(0))
    os.remove(sdeMOWPoly.getOutput(0))
#    # close out the log file
    print("Closing the log file.")
    log.close() 
   
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
