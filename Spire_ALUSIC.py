# Project: AL to USIC data
# Create Date: 02/13/2020
# Last Updated: 03/02/2020
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
# -----------------------------------------------------------------------

# Import modules
import sys, arcpy, datetime, traceback
# import os


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
    print("\n")
    print("Connected to {0} for {1}.".format(sdeConnect,shpName))
    print("\n")
    fmap = arcpy.FieldMappings()
    fmap.addTable(inputFC)
    # Get all fields
    fields = {f.name: f for f in arcpy.ListFields(inputFC)}
    # Clean up field map based on keep list
    for fname, fld in fields.iteritems():
       if fld.type not in ('OID', 'Geometry') and 'shape' not in fname.lower():
          if fname not in keepList:
             print("Field name {0} is not on the Keep List and will be removed.".format(fname))
             fmap.removeFieldMap(fmap.findFieldMapIndex(fname))
    # Set shapefile path name
    shpPath = r'C:\TempUSIC\SpireAL'
    print("Creating the shapefile now.")
    arcpy.conversion.FeatureClassToFeatureClass(inputFC, shpPath, shpName, '#', fmap)
    print("Shapefile {0} has been created in {1}.".format(shpName, shpPath))
    print("\n")
                                                                                               
# Set unbuffered mode
sys.stdout = Unbuffered(sys.stdout)
try:
    # set datetime variable
    d = datetime.datetime.now()
    # open log file for holding errors
    # will also create file if not already there
    log = open("C:\TempUSIC\ALLogFile.txt","a")
    log.write("----------------------------" + "\n")
    log.write("----------------------------" + "\n")
    # write datetime to log
    log.write("Log: " + str(d) + "\n")
    log.write("\n")
    # set arcpy environment to allow overwriting
    arcpy.env.overwriteOutput=True

#--------------------Create SDE Connections------------------------------------
    sdeTempPath = r"C:\TempUSIC"
    # Connecting to an existing SDE doesn't seem to work unless the connection
    # is already in place.
    # This is a work around to deal with that issue and avoid needing to connect
    # ahead of time outside the script.
    
##    if arcpy.Exists("C:\TempUSIC\tempALServ.sde"):
##        arcpy.Delete_management("C:\TempUSIC\tempALServ.sde") stl-pgisdb-22.lac1.biz:1521/PGISM

    sdeMOE = arcpy.CreateDatabaseConnection_management(sdeTempPath, 'tempMOEServ.sde', \
                                              'ORACLE', 'stl-pgisdb-20:1526/PGISE',\
                                              'DATABASE_AUTH', 'IMAPVIEW', \
                                              'ue2Y6vwm','SAVE_USERNAME')
    print("Database connection created at {0} to the Mo East Oracle Database."\
          .format(sdeTempPath))
    print("\n")
    
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
#----------------------------AL Setup----------------------------------------
    
   # Set path variables
    cPath = r"C:\TempUSIC"
    sdeConnect = sdeAL 

#---------Dimension Text-------------------------------------------------------
    shpName = "mainText"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.MainText'
    keepList = ['TextString', 'FontSize', 'Angle']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    del shpName, keepList, inputFC

#---------Distribution Main-------------------------------------------------------
    shpName = "main"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.Main'
    keepList = ['INSTALLDATE','MEASUREDLENGTH','LENGTHSOURCE','COATINGTYPE',\
                'NOMINALPIPESIZE','PIPEGRADE','PRESSURECODE',\
                'MATERIALCODE','LABELTEXT','TRANSMISSION_FLAG',\
                'LOCATIONDESCRIPTION','PLASTICTYPE','PROJECTYEAR',\
                'MANUFACTURER','LENGTHMX']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
#---------Regulator Station----------------------------------------------------
    shpName = "RegulatorStation"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.RegulatorStation'
    keepList = ['INSTALLDATE','LOCATIONDESCRIPTION','ROTATIONANGLE',\
                'COMMENTS', 'MAXINLETPRESSURE', 'MAXOUTLETPRESSURE',\
                'SUBTYPE','SETTINGNAME']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
#---------Abandoned Main----------------------------------------------------
    shpName = "AbandonedMain"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.AbandonedMain'
    keepList = ['MEASUREDLENGTH', 'COATINGTYPE', \
                'NOMINALPIPESIZE', 'MATERIAL','DATEABANDONED', 'LABELTEXT']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
#---------Valves----------------------------------------------------
    shpName = "Valves"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.Valve'
    keepList = ['INSTALLDATE', 'COMMENTS', 'HOUSEDIN', \
                'MATERIAL', 'INSULATEDINDICATOR', 'VALVEENDS', 'VALVETYPE', \
                'VALVEUSE', 'ROTATIONANGLE', 'VALVEMATERIAL', 'VALVESIZE', \
                'LABELTEXT','TURNSTOCLOSE','DATECREATED','DATEMODIFIED'\
                'LOCATIONDESCRIPTION']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
#---------Casing----------------------------------------------------
    shpName = "Casing"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.Casing'
    keepList = ['MEASUREDLENGTH', 'CASINGCOATINDICATOR',\
                'CASINGSIZE', 'CASINGMATERIAL','LABELTEXT']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
#---------Casing----------------------------------------------------
    shpName = "Drips"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.Drip'
    keepList = ['LOCATIONDESCRIPTION', 'INSTALLDATE','LABELTEXT']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
#---------Marker Ball----------------------------------------------------
    shpName = "MarkerBall"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.ElectronicMarker'
    keepList = ['INSTALLDATE', 'DISTANCE1','DIRECTION1',\
                'LOCATION1','BUILDING1','STREET1','DISTANCE2','DIRECTION2',\
                'LOCATION2','BUILDING2','STREET2']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
#---------Marker Ball----------------------------------------------------
    shpName = "FcRegulator"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.FirstCutRegulator'
    keepList = ['LOCATIONDESCRIPTION','ROTATIONANGLE','INSTALLDATE']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
#---------Fittings----------------------------------------------------
    shpName = "Fittings"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.Fitting'
    keepList = ['FITTINGSIZE','INSULATEDINDICATOR','MATERIAL',\
                'FITTINGTYPE','ROTATIONANGLE','LABELTEXT',\
                'LOCATIONDESCRIPTION','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
#---------Fittings----------------------------------------------------
    shpName = "Services"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.Service'
    keepList = ['INSTALLDATE','MEASUREDLENGTH','LENGTHSOURCE','COATINGTYPE',\
                'PIPETYPE','NOMINALPIPESIZE','PIPEGRADE','PRESSURECODE',\
                'MATERIALCODE','LABELTEXT','TRANSMISSION_FLAG',\
                'LOCATIONDESCRIPTION','HIGHDENSITYPLASTIC','PROJECTYEAR',\
                'PROJECTNUMBER','SERVICETYPE','MANUFACTURER','LENGTH604',\
                'STREETADDRESS','MAINMATERIAL']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
#---------Stopper Fitting----------------------------------------------------
    shpName = "stopperFitting"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.StopperFitting'
    keepList = ['INSTALLDATE','LABELTEXT','LOCATIONDESCRIPTION','PRESENTPOSITION']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
#---------Premises----------------------------------------------------
    shpName = "Premise"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Historical\GISADMIN.Premise'
    keepList = ['INSTALLIONDATE','PIPENAME','LOCATIONDESCRIPTION',\
                'PIPEID','MANUFACTURER']
    copyFeature(shpName,sdeConnect,keepList,inputFC)

#---------CP Rectifier----------------------------------------------------
    shpName = "cpRectifier"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.CPRectifier'
    keepList = ['LOCATIONDESCRIPTION','RECTIFIERNAME','RECTIFIERTYPE',\
                'LABELTEXT']
    copyFeature(shpName,sdeConnect,keepList,inputFC) 

##------------------------Abandon Services--------------------------------------     
    shpName = "abandonService"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.AbandonedService'
    keepList = ['NOMINALSIZE','MATERIALCODE','DATEABANDONED','LABELTEXT',\
                'RETIREMENTPROJECTNUMBER']
    copyFeature(shpName,sdeConnect,keepList,inputFC)

##------------------------CP Anode-------------------------------------- -------      
    shpName = "cpAnode"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.CPAnode'
    keepList = ['DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','LEADCOLOR','PROTECTIONDIRECTION',\
                'BOXTYPE','LOCATIONDESCRIPTION']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
##------------------------CP Test Point-------------------------------------- -------      
    shpName = "cpTestPoint"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.CPTestPoint'
    keepList = ['COMMENTS','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','LEADCOLOR','LEADDIRECTION','BOXTYPE',\
                'STATIONTYPE','LOCATIONDESCRIPTION']
    copyFeature(shpName,sdeConnect,keepList,inputFC)

##------------------------Service Text--------------------------------- -------   
    shpName = "serviceText"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.ServiceText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeConnect,keepList,inputFC) 
    
##------------------------Misc Text--------------------------------- ----------- 
    shpName = "miscText"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Landbase\GISADMIN.MiscellaneousText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
##------------------------Project Boundary------------------------- ----------- 
    shpName = "projBoundary"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.ProjectData\GISADMIN.ProjectBoundary'
    keepList = ['DESCRIPTION','STATUS','PROJECTNUMBER']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
##------------------------Valve Text------------------------- ----------- 
    shpName = "casingText"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.CasingText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeConnect,keepList,inputFC) 
    
##------------------------Valve Text------------------------- ----------- 
    shpName = "valveText"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.ValveText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
##------------------------Fitting Text------------------------- ----------- 
    shpName = "fittingText"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.FittingText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
##------------------------Retired Main Text------------------------- ----------- 
    shpName = "retMainText"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.RetiredMainText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
##------------------------Retired Main Text------------------------- ----------- 
    shpName = "retSvcText"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.RetiredServiceText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
##------------------------Regulator Station Text------------------------- ----------- 
    shpName = "regStationText"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.RegulatorStationText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
##------------------------Stopper Fitting Text------------------------- ----------- 
    shpName = "stopFittingText"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.StopperFittingText'
    keepList = ['TEXTSTRING','FONTSIZE','ANGLE']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
##------------------------Stopper Fitting Text------------------------- ----------- 
    shpName = "gasLamp"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.Gas\GISADMIN.GasLamp'
    keepList = ['SYMBOLROTATION','STREET_NUMBER','STREET_NAME','STREET_SUFFIX']
    copyFeature(shpName,sdeConnect,keepList,inputFC)

##------------------------Customer------------------------- ----------- 
    shpName = "customer"
    inputFC = sdeConnect.getOutput(0) + '\GISADMIN.CCSData\GISADMIN.Customer'
    keepList = ['METERLOCATION','ADDRESS']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
############################   MISSOURI EAST    ############################### 
    sdeConnect = sdeMOE

##------------------------MoNat Dimension Text--------------------- ----------- 
    shpName = "MOE_moNatDimText"
    inputFC = sdeConnect.getOutput(0) + '\LGC_LAND.Landbase\LGC_LAND.MoNatDimText'
    keepList = ['SYMBOLROTATION','DIMENSION','COUNTY']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
##------------------------Marker Ball--------------------- ----------- 
    shpName = "MOE_MarkerBall"
    inputFC = sdeConnect.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.LocationIndicator'
    keepList = ['COMMENTS','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','LOCATION3','INSTALL_DATE','INSTALLED_ON',\
                'OWNER','MARKERTYPE', 'SUBTYPECD','FULLTEXT']
    copyFeature(shpName,sdeConnect,keepList,inputFC)
    
##------------------------MoNat Dimension Line--------------------- ----------- 
    shpName = "MOE_MONat_DimLine"
    inputFC = sdeConnect.getOutput(0) + '\LGC_LAND.Landbase\LGC_LAND.MoNatDimLine'
    keepList = ['OWNER']
    copyFeature(shpName,sdeConnect,keepList,inputFC)

##------------------------Distribution Main Dimension--------------------- ----------- 
    shpName = "MOE_DimLine"
    inputFC = sdeConnect.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.DistributionMainDimension'
    keepList = ['LOCATION','SYMBOLROTATION','DISTANCE','COVER']
    copyFeature(shpName,sdeConnect,keepList,inputFC)     
    
##------------------------Service Points--------------------------- ----------- 
    shpName = "MOE_svcPoints"
    inputFC = sdeConnect.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.ServicePoint'
    keepList = ['CUSTOMERTYPE','SERVICEMXLOCATION','SERVICESTATUS','DISCLOCATION',\
                'STREETADDRESS','METERLOCATIONDESC','METERLOCATION','MXSTATUS']
    copyFeature(shpName,sdeConnect,keepList,inputFC)

##------------------------Test Points--------------------------- ----------- 
    shpName = "MOE_testPoint"
    inputFC = sdeConnect.getOutput(0) + '\LGC_GAS.GasFacilities\LGC_GAS.CPTestPoint'
    keepList = ['COMMENTS','DISTANCE1','DIRECTION1','LOCATION1',\
                'BUILDING1','STREET1','DISTANCE2','DIRECTION2','LOCATION2',\
                'BUILDING2','STREET2','LEADCOLOR','LEADDIRECTION','BOXTYPE',\
                'STATIONTYPE','LOCATIONDESCRIPTION','SYMBOLROTATION','SUBTYPECD',\
                'OPERATINGPRESSURE','LOCATION1MX','LOCATION2MX','ADDITIONALINFO',\
                'CPSIZE','HOUSENUM','STREETNAME']
    copyFeature(shpName,sdeConnect,keepList,inputFC)     
    
    
    #Clean up the temp SDE connection
#    arcpy.Delete_management(sdeAL)     
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