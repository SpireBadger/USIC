# Project: AL to USIC data
# Create Date: 02/13/2020
# Last Updated: 03/03/2020
# Created by: Brad Craddick & Robert Domiano
# Updated by: Robert Domiano
# Purpose: To provide a clean set of the AL GIS data to send to USIC
# ArcGIS Version:   10.2
# Python Version:   2.7.5
# -----------------------------------------------------------------------
# Project: Spire to USIC data compilation
# Create Date: 02/13/2020
# Last Updated: 03/02/2020
# Create by: Brad Craddick & Robert Domiano
# Updated by: Robert Domiano
# Purpose: To provide a clean set of MO East, MO West, and Alabama to USIC
# ArcGIS Version:   10.3
# Python Version:   2.7.5

##Note: Wo Poly's from MO East not added, look into
# -----------------------------------------------------------------------

# Import modules
import sys, arcpy, datetime, traceback
import os


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
   
def copyFeature(shpName, sdeConnect, keepList, inputFC):
    wsConnect = sdeConnect.getOutput(0)
    arcpy.env.workspace = wsConnect
    fmap = arcpy.FieldMappings()
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
    # Set variable to the path declared in script
    setPath = r"\\pdatfile01\ProdData\GIS\USIC"
    # Determine what SDE is being used and set shpPath to point to a matching
    # directory to store shapefiles in.
    if sdeConnect == sdeAL:
        print("Connecting to the {0} SDE.".format(paths[0]))
        shpPath = os.path.join(setPath, paths[0])
#    elif sdeConnect == sdeMOE:
#        shpPath = os.path.join(setPath, paths[1])
#        print("Connecting to the {0} SDE.".format(paths[1]))
    # Prior to using the directory, test to see if it exists.
    # If it does not, create a new directory based on that name.
    if not os.path.exists(shpPath):
        os.mkdir(shpPath)
        print("No folder for shapefiles. A directory has been created at {0}.".format(shpPath))
#    elif sdeConnect == sdeMOW:
#        shpPath = os.path.join(setPath, paths[2])
    print("Creating the shapefile now.")
    arcpy.conversion.FeatureClassToFeatureClass(inputFC, shpPath, shpName, '#', fmap)
    print("Shapefile {0} has been created in {1}.".format(shpName, shpPath))
    print("\n")
    del shpName, keepList, inputFC, sdeConnect
                                                                                               
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
    # open log file for holding errors
    # will also create file if not already there
    log = open("C:\TempUSIC\LogFile.txt","w")
    log.write("----------------------------" + "\n")
    log.write("----------------------------" + "\n")
    # write datetime to log
    log.write("Log: " + str(d) + "\n")
    log.write("\n")
    # set arcpy environment to allow overwriting
    arcpy.env.overwriteOutput=True

#--------------------Create SDE Connections------------------------------------
    # Connecting to an existing SDE doesn't seem to work unless the connection
    # is already in place.
    # This is a work around to deal with that issue and avoid needing to connect
    # ahead of time outside the script.
    
#    sdeMOE = arcpy.CreateDatabaseConnection_management(sdeTempPath, 'tempMOEServ.sde', \
#                                              'ORACLE', 'stl-pgisdb-20:1526/PGISE',\
#                                              'DATABASE_AUTH', 'IMAPVIEW', \
#                                              'ue2Y6vwm','SAVE_USERNAME')
#    print("Database connection created at {0} to the Mo East Oracle Database."\
#          .format(sdeTempPath))
    
       # Create the MO West SDE Connection
#    sdeMOW = arcpy.CreateDatabaseConnection_management(sdeTempPath, 'tempMOEServ.sde', \
#                                              'ORACLE', 'stl-pgisdb-22.lac1.biz:1521/PGISM',\
#                                              'DATABASE_AUTH', 'IMAPVIEW', \
#                                              'ue2Y6vwm','SAVE_USERNAME')
#    print("Database connection created at {0} to the MO West Oracle Database."\
#          .format(sdeTempPath))
#    print("\n")     
    sdeAL = arcpy.CreateDatabaseConnection_management(sdeTempPath,'tempALServ.sde',\
                                                      'ORACLE',\
                                                      'xs-bhm-dgp-1.energen.com:1521/gsp',\
                                                      'DATABASE_AUTH', 'GISADMIN',\
                                                      'gisadmin','SAVE_USERNAME')
    print("Database connection created at {0} to the Alabama Database."\
          .format(sdeTempPath))
#----------------------------AL Setup------------------------------------------
#---------Dimension Text-------------------------------------------------------
    shpName = "mainText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.MainText'
    keepList = ['TextString', 'FontSize', 'Angle']
#    copyFeature(shpName,sdeAL,keepList,inputFC)
#
#---------Distribution Main-------------------------------------------------------
    shpName = "main"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.Main'
    keepList = ['INSTALLDATE','MEASUREDLENGTH','LENGTHSOURCE','COATINGTYPE',\
                'NOMINALPIPESIZE','PIPEGRADE','PRESSURECODE',\
                'MATERIALCODE','LABELTEXT','TRANSMISSION_FLAG',\
                'LOCATIONDESCRIPTION','PLASTICTYPE','PROJECTYEAR',\
                'MANUFACTURER','LENGTHMX']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
#---------Regulator Station----------------------------------------------------
    shpName = "RegulatorStation"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.RegulatorStation'
    keepList = ['INSTALLDATE','LOCATIONDESCRIPTION','ROTATIONANGLE',\
                'COMMENTS', 'MAXINLETPRESSURE', 'MAXOUTLETPRESSURE',\
                'SUBTYPE','SETTINGNAME']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
#---------Abandoned Main----------------------------------------------------
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
    shpName = "MarkerBall"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.ElectronicMarker'
    keepList = ['INSTALLDATE', 'DISTANCE1','DIRECTION1',\
                'LOCATION1','BUILDING1','STREET1','DISTANCE2','DIRECTION2',\
                'LOCATION2','BUILDING2','STREET2']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
#---------First Cut Regulator----------------------------------------------------
    shpName = "FcRegulator"
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
    shpName = "stopperFitting"
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
    shpName = "cpRectifier"
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
    shpName = "cpAnode"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.CPAnode'
    keepList = ['DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','LEADCOLOR','PROTECTIONDIRECTION',\
                'BOXTYPE','LOCATIONDESCRIPTION']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------CP Test Point-------------------------------------- -------      
    shpName = "cpTestPoint"
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
    shpName = "miscText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Landbase\GISADMIN.MiscellaneousText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Project Boundary------------------------- ----------- 
    shpName = "projBoundary"
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
    
##------------------------Retired Main Text------------------------- ----------
    shpName = "retMainText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.RetiredMainText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Retired Service Text------------------------- -------
    shpName = "retSvcText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.RetiredServiceText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Regulator Station Text------------------------- -----
    shpName = "regStationText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.RegulatorStationText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Stopper Fitting Text------------------------- -------
    shpName = "stopFittingText"
    inputFC = sdeAL.getOutput(0) + '\GISADMIN.Gas\GISADMIN.StopperFittingText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeAL,keepList,inputFC)
    
##------------------------Main Authorization Number Text-----------------------
    shpName = "mainAuthorNumText"
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
    
#############################   MISSOURI EAST    ############################### 
#
##------------------------MoNat Dimension Text--------------------- ----------- 
#    shpName = "MOE_moNatDimText"
#    inputFC = sdeMOE.getOutput(0) + '\LGC_LAND.Landbase\LGC_LAND.MoNatDimText'
#    keepList = ['SYMBOLROTATION','DIMENSION','COUNTY']
#    copyFeature(shpName,sdeMOE,keepList,inputFC)
#    
###------------------------Marker Ball--------------------- ----------- 
#    shpName = "MOE_MarkerBall"
#    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.LocationIndicator'
#    keepList = ['COMMENTS','DISTANCE1','DIRECTION1','LOCATION1',\
#                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
#                'BUILDING2','STREET2','LOCATION3','INSTALL_DATE','INSTALLED_ON',\
#                'OWNER','MARKERTYPE', 'SUBTYPECD','FULLTEXT']
#    copyFeature(shpName,sdeMOE,keepList,inputFC)
#    
###------------------------MoNat Dimension Line--------------------- ----------- 
#    shpName = "MOE_MONat_DimLine"
#    inputFC = sdeMOE.getOutput(0) + '\LGC_LAND.Landbase\LGC_LAND.MoNatDimLine'
#    keepList = ['OWNER']
#    copyFeature(shpName,sdeMOE,keepList,inputFC)
#
###------------------------Distribution Main Dimension--------------------- ----------- 
#    shpName = "MOE_DimLine"
#    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.DistributionMainDimension'
#    keepList = ['LOCATION','SYMBOLROTATION','DISTANCE','COVER']
#    copyFeature(shpName,sdeMOE,keepList,inputFC)     
#    
###------------------------Service Points--------------------------- ----------- 
#    shpName = "MOE_svcPoints"
#    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.ServicePoint'
#    keepList = ['CUSTOMERTYPE','SERVICEMXLOCATION','SERVICESTATUS','DISCLOCATION',\
#                'STREETADDRESS','METERLOCATIONDESC','METERLOCATION','MXSTATUS']
#    copyFeature(shpName,sdeMOE,keepList,inputFC)
#
###------------------------Test Points--------------------------- ----------- 
#    shpName = "MOE_testPoint"
#    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.CPTestPoint'
#    keepList = ['COMMENTS','DISTANCE1','DIRECTION1','LOCATION1',\
#                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
#                'BUILDING2','STREET2','LEADCOLOR','LEADDIRECTION','BOXTYPE',\
#                'STATIONTYPE','LOCATIONDESCRIPTION','SYMBOLROTATION','SUBTYPECD',\
#                'OPERATINGPRESSURE','LOCATION1MX','LOCATION2MX','ADDITIONALINFO',\
#                'CPSIZE','HOUSENUM','STREETNAME']
#    copyFeature(shpName,sdeMOE,keepList,inputFC)     
#    
###------------------------Ctrl Fittings--------------------------- ----------- 
#    shpName = "MOE_controllableFittings"
#    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.ControllableFitting'
#    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
#                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
#                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
#                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
#                'BUILDING2','STREET2','SUBTYPECD','COVER','SYMBOLROTATION']
#    copyFeature(shpName,sdeMOE,keepList,inputFC)  
#
###------------------------nON-Ctrl Fittings--------------------------- ----------- 
#    shpName = "MOE_NoncontrollableFittings"
#    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.NonControllableFitting'
#    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
#                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
#                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
#                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
#                'BUILDING2','STREET2','SUBTYPECD','COVER','SYMBOLROTATION']
#    copyFeature(shpName,sdeMOE,keepList,inputFC)
#    
###------------------------abandoned Services--------------------------- ----------- 
#    shpName = "MOE_abandonServices"
#    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.AbandonedGasService'
#    keepList = ['SUBTYPECD','NOMINALDIAMETER','MATERIAL','FIELDBOOKPATH',\
#                'MXSTREETADDRESS','MXTEELOCATION','MXCURBBOXLOCATION',\
#                'MXCURBDESCRIPTION','MXSERVICELOCATION','MXRISERLOCATION',\
#                'MXRISERDESCRIPTION','MXMAINLOCATION','MXMAINSIZE','MXMAINMATERIAL',\
#                'DATECREATED','DATEMODIFIED','OPERATINGPRESSURE','STREETNUMBER',\
#                'STREETNAME','STREETSUFFIX','ONE_HUNDRED_FOOT_DISPLAY','REASON']
#    copyFeature(shpName,sdeMOE,keepList,inputFC)
#    
###------------------------Valves--------------------------- ----------- 
#    shpName = "MOE_Valves"
#    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.GasValve'
#    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
#                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
#                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
#                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
#                'BUILDING2','STREET2','SUBTYPECD','COVER','SYMBOLROTATION'\
#                'DIRECTION1MX','DIRECTION2MX','MXLOCATION','COVER','SUBTYPECD','COMMENTS',\
#                'MATERIAL','MATERIALMX','VALVEDIAMETER','VALVETYPE','VALVEUSE',\
#                'CLOCKWISETOCLOSE','NORMALPOSITION','NONESSENTIAL','NUMBEROFTURNS',\
#                'VALVENUMBER','VALVELOCATION1','VALVELOCATION2','VALVELOCATION3',\
#                'FITTINGNUMBER']
#    copyFeature(shpName,sdeMOE,keepList,inputFC)
#
###------------------------Wo Polygons--------------------------- -----------
#    # wo POLYGONS WILL NEED THEIR OWN SDE CONNECTION
##    shpName = "MOE_WOPoly"
##    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.GasValve'
##    keepList = ['STATUS','MXWONUM','WORKTYPE','DESCRIPTION','ZLAC_SUBWORKTYPE',\
##                'ACTFINISH']
##    copyFeature(shpName,sdeMOE,keepList,inputFC)      
#    
###------------------------Drips--------------------------- ----------- 
#    shpName = "MOE_Drip"
#    inputFC = sdeMOE.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.Drip'
#    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
#                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
#                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
#                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
#                'BUILDING2','STREET2','SUBTYPECD','COVER','SYMBOLROTATION'\
#                'DIRECTION1MX','DIRECTION2MX','MXLOCATION','COVER','SUBTYPECD','COMMENTS',\
#                'MATERIAL','DRIPTYPE','CONNECTYPE','OFFSET']
#    copyFeature(shpName,sdeMOE,keepList,inputFC)
#    
#    
#    
#    
#
#    
    #Clean up the temp SDE connection
    print("\n")
    arcpy.env.workspace = ""
    arcpy.ClearWorkspaceCache_management(sdeAL)
    os.remove(sdeAL.getOutput(0))
#    os.remove(sdeMOE.getOutput(0))
    # close out the log file
    print("Closing the log file.")
    log.close() 
   
except:
#    arcpy.Delete_management(sdeAL)
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" \
            + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"    
    log.write("" + pymsg + "\n")
    log.write("" + msgs + "")
    print(msgs)
    log.close() 
