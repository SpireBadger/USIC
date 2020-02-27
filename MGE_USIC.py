import arcpy, re, os, csv,sys, string, calendar, traceback
from arcpy import env
try:
    d = datetime.datetime.now()
    log = open("C:\\Temp\MGE.txt","a")
    log.write("----------------------------" + "\n")
    log.write("----------------------------" + "\n")
    log.write("Log: " + str(d) + "\n")
    log.write("\n")
    arcpy.env.overwriteOutput=True
    ########--Marker Ball USIC---##
    Dist=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.LocationIndicator"
    Dists=r"C:\temp\NO_GIS_SP_2.gdb\LocIndInterim"
    USIC=r"\\pdatfile01\ProdData\GIS\USIC\MoWest"
    USICpdf=r"\\pdatfile01\ProdData\GIS\USIC\MoWest"
    arcpy.CopyFeatures_management(Dist,Dists)
    arcpy.MakeFeatureLayer_management (Dists, 'Distsss')
    fieldNameList = []
    fields = arcpy.ListFields("Distsss")
    fieldNameList = []
    fields = arcpy.ListFields("Distsss")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'DISTANCE1':
            print 'COVER '+field.name
        elif field.name == 'DIRECTION1':
            print 'COVER '+field.name
        elif field.name == 'LOCATION1':
            print 'DISTANCE '+field.name
        elif field.name == 'BUILDING1':
            print 'keeping '+field.name
        elif field.name == 'STREET1':
            print 'keeping '+field.name
        elif field.name == 'DISTANCE2':
            print 'keeping '+field.name
        elif field.name == 'DIRECTION2':
            print 'keeping '+field.name
        elif field.name == 'LOCATION2':
            print 'keeping '+field.name
        elif field.name == 'BUILDING2':
            print 'keeping '+field.name
        elif field.name == 'LOCATION3':
            print 'keeping '+field.name
        elif field.name == 'INSTALLED_ON':
            print 'keeping '+field.name
        elif field.name == 'INSTALL_DATE':
            print 'keeping '+field.name
        elif field.name == 'COMMENTS':
            print 'keeping '+field.name
        elif field.name == 'STREET2':
            print 'keeping '+field.name
        elif field.name == 'OWNER':
            print 'keeping '+field.name
        elif field.name == 'MARKERTYPE':
            print 'keeping '+field.name
        elif field.name == 'SUBTYPECD':
            print 'keeping '+field.name
        elif field.name == 'FULLTEXT':
            print 'keeping '+field.name
        
        else :
            print 'deleting '+field.name
            fieldNameList.append(field.name)
    print fieldNameList
    arcpy.DeleteField_management ("Distsss", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"MarkerBallUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"MarkerBallUSIC.shp")
    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"MarkerBallUSIC.shp")
    ####------Drip-----######
    Drips=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.Drip"
    Drips2r=r"C:\temp\NO_GIS_SP_2.gdb\DripInt2"
    arcpy.CopyFeatures_management (Drips, Drips2r)
    arcpy.MakeFeatureLayer_management (Drips2r, 'Drips2r2')
    fieldNameList = []
    fields = arcpy.ListFields("Drips2r2")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Area':
            print 'keeping '+field.name
        elif field.name == 'OFFSET':
            print 'keeping '+field.name
        elif field.name == 'DRIPTYPE':
            print 'keeping '+field.name
        elif field.name == 'CONNECTTYPE':
            print 'keeping '+field.name
        elif field.name == 'DISTANCE1':
            print 'keeping '+field.name
        elif field.name == 'DIRECTION1MX':
            print 'keeping '+field.name
        elif field.name == 'STREET1':
            print 'keeping '+field.name
        elif field.name == 'DISTANCE2':
            print 'keeping '+field.name
        elif field.name == 'DIRECTION2MX':
            print 'keeping '+field.name
        elif field.name == 'STREET2':
            print 'keeping '+field.name
        elif field.name == 'MXLOCATION':
            print 'keeping '+field.name
        elif field.name == 'COVER':
            print 'keeping '+field.name
        elif field.name == 'SUBTYPECD':
            print 'keeping '+field.name
        else :
            print 'deleteing '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("Drips2r2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"Drip.shp"):
        arcpy.Delete_management(USIC+"\\"+"Drip.shp")
    arcpy.CopyFeatures_management ('Drips2r2', USIC+"\\"+"Drip.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"Drip.shp")
    if arcpy.Exists(Drips2r):
        arcpy.Delete_management(Drips2r)
    ##########--Distribution Main Dimension USIC---
    Dist=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.DistributionMainDimension"
    Dists=r"C:\temp\NO_GIS_SP_2.gdb\DistDimInterim"
    arcpy.CopyFeatures_management(Dist,Dists)
    arcpy.MakeFeatureLayer_management (Dists, 'Distsss')
    fieldNameList = []
    fields = arcpy.ListFields("Distsss")
    fieldNameList = []
    fields = arcpy.ListFields("Distsss")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'COVER':
            print 'COVER '+field.name
        elif field.name == 'SHAPE':
            print 'COVER '+field.name
        elif field.name == 'DISTANCE':
            print 'DISTANCE '+field.name
        elif field.name == 'LOCATION':
            print 'keeping '+field.name
        elif field.name == 'SYMBOLROTATION':
            print 'keeping '+field.name
        
        else :
            print 'deleting '+field.name
            fieldNameList.append(field.name)
    print fieldNameList
    arcpy.DeleteField_management ("Distsss", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"DistributionMainDimUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"DistributionMainDimUSIC.shp")
    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"DistributionMainDimUSIC.shp")
    ####--Service Point--#########
    SP=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.ServicePoint"
    SPs=r"C:\temp\NO_GIS_SP_2.gdb\SPInterim"
    arcpy.CopyFeatures_management(SP,SPs)
    arcpy.MakeFeatureLayer_management (SPs, 'SPss')
    arcpy.AddField_management ('SPss', "Len", "LONG")
    fieldNameList = []
    fields = arcpy.ListFields("SPss")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'MXSTATUS':
            print 'keeping '+field.name
        elif field.name == 'METERLOCATION':
            print 'keeping '+field.name
        elif field.name == 'METERLOCATIONDESC':
            print 'keeping '+field.name
        elif field.name == 'STREETADDRESS':
            print 'keeping '+field.name
        elif field.name == 'SERVICEPOINTTYPE':
            print 'keeping '+field.name
        elif field.name == 'DISCLOCATION':
            print 'keeping '+field.name
        elif field.name == 'SERVICESTATUS':
            print 'keeping '+field.name
        elif field.name == 'CUSTOMERTYPE':
            print 'keeping '+field.name
        elif field.name == 'DIVISION':
            print 'keeping '+field.name
        elif field.name == 'TOWN':
            print 'keeping '+field.name
        elif field.name == 'SECTOR':
            print 'keeping '+field.name
        elif field.name == 'Len':
            print 'keeping '+field.name
        elif field.name == 'SERVICEMXLOCATION':
            print 'keeping '+field.name
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("SPss", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"ServicePointUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"ServicePointUSIC.shp")
    arcpy.CopyFeatures_management ('SPss', USIC+"\\"+"ServicePointUSIC.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"ServicePointUSIC.shp")
    arcpy.MakeFeatureLayer_management (USIC+"\\"+"ServicePointUSIC.shp", 'SPs3')
    arcpy.CalculateField_management("SPs3", "Len", "len( !SERVICEMXL!)", "PYTHON_9.3", "")
    query=r'NOT '+'"Len"'+" >9 AND NOT"+'"SERVICEMXL" in ('+"' ','MGEMAIN')"
    arcpy.SelectLayerByAttribute_management ('SPs3','NEW_SELECTION', query)
    arcpy.AddField_management ('SPs3', "LOC", "LONG")
    arcpy.CalculateField_management ('SPs3', 'LOC', '!SERVICEMXL!','PYTHON')
    arcpy.SelectLayerByAttribute_management ('SPs3','CLEAR_SELECTION')
    arcpy.DeleteField_management ('SPs3', 'Len')
    if arcpy.Exists(SPs):
        arcpy.Delete_management(SPs)
    ######--Test Points
    TP=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.CPTestPoint"
    if arcpy.Exists(USIC+"\\"+"AnodeUSIC"):
        arcpy.Delete_management(USIC+"\\"+"AnodeUSIC.shp")
    anode=r"C:\temp\NO_GIS_SP_2.gdb\AnodeInt"
    arcpy.CopyFeatures_management (TP, anode)
    arcpy.MakeFeatureLayer_management (anode, 'anode2')
    fieldNameList = []
    fields = arcpy.ListFields("anode2")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'CPSIZE':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'SYMBOLROTATION':
            print 'keeping '+field.name
        elif field.name == 'SUBTYPECD':
            print 'keeping '+field.name
        elif field.name == 'HOUSENUM':
            print 'keeping '+field.name
        elif field.name == 'STREETNAME':
            print 'keeping '+field.name
        elif field.name == 'STATIONTYPE':
            print 'keeping '+field.name    
        elif field.name == 'OPERATINGPRESSURE':
            print 'keeping '+field.name
        elif field.name == 'PROTECTING':
            print 'keeping '+field.name
        elif field.name == 'DISTANCE1':
            print 'keeping '+field.name
        elif field.name == 'STREET1':
            print 'keeping '+field.name
        elif field.name == 'REASON':
            print 'keeping '+field.name 
        elif field.name == 'LOCATION1MX':
            print 'keeping '+field.name
        elif field.name == 'DISTANCE2':
            print 'keeping '+field.name
        elif field.name == 'STREET2':
            print 'keeping '+field.name
        elif field.name == 'LOCATION2MX':
            print 'keeping '+field.name
        elif field.name == 'LEADCOLOR':
            print 'keeping '+field.name
        elif field.name == 'LEADDIRECTION':
            print 'keeping '+field.name
        elif field.name == 'ADDITIONALINFO':
            print 'keeping '+field.name
        elif field.name == 'BOXTYPE':
            print 'keeping '+field.name
        elif field.name == 'DIVISION':
            print 'keeping '+field.name
        elif field.name == 'TOWN':
            print 'keeping '+field.name
        elif field.name == 'SECTOR':
            print 'keeping '+field.name
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("anode2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"AnodeUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"AnodeUSIC.shp")
    arcpy.CopyFeatures_management("anode2",USIC+"\\"+"AnodeUSIC.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"AnodeUSIC.shp")
    if arcpy.Exists(anode):
        arcpy.Delete_management(anode)
    ###--Rectifier
    Rectifier=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.CPRectifier"
    if arcpy.Exists(USIC+"\\"+"RectifierUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"RectifierUSIC.shp")
    CRs=r"C:\temp\NO_GIS_SP_2.gdb\CRInt"
    arcpy.CopyFeatures_management (Rectifier, CRs)
    arcpy.MakeFeatureLayer_management (CRs, 'CRs2')
    fieldNameList = []
    fields = arcpy.ListFields("CRs2")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'SUBTYPECD':
            print 'keeping '+field.name
        elif field.name == 'DIVISION':
            print 'keeping '+field.name
        elif field.name == 'TOWN':
            print 'keeping '+field.name
        elif field.name == 'SECTOR':
            print 'keeping '+field.name
        elif field.name == 'COMMENTS':
            print 'keeping '+field.name
        elif field.name == 'FACILITYID':
            print 'keeping '+field.name
        elif field.name == 'SYMBOLROTATION':
            print 'keeping '+field.name
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("CRs2", fieldNameList)
    arcpy.CopyFeatures_management ('CRs2', USIC+"\\"+"RectifierUSIC.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"RectifierUSIC.shp")
    if arcpy.Exists(CRs):
        arcpy.Delete_management(CRs)
    #########--GA_FittingLine
    GAFittingLine=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.GA_FittingLine"
    if arcpy.Exists(USIC+"\\"+"GAFittingLineUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"GAFittingLineUSIC.shp")
    GAs=r"C:\temp\NO_GIS_SP_2.gdb\CRInt"
    arcpy.CopyFeatures_management (GAFittingLine, GAs)
    arcpy.MakeFeatureLayer_management (GAs, 'GAs2')
    arcpy.CopyFeatures_management ('GAs2', USIC+"\\"+"GAFittingLineUSIC.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"GAFittingLineUSIC.shp")
    if arcpy.Exists(GAs):
        arcpy.Delete_management(GAs)
    #########--GA_FittingText
    GAFittingText=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.GA_FittingText"
    if arcpy.Exists(USIC+"\\"+"GAFittingTextUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"GAFittingTextUSIC.shp")
    GAFs=r"C:\temp\NO_GIS_SP_2.gdb\GAFInt"
    arcpy.CopyFeatures_management (GAFittingText, GAFs)
    arcpy.MakeFeatureLayer_management (GAFs, 'GAFs2')
    fieldNameList = []
    fields = arcpy.ListFields("GAFs2")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'SUBTYPECD':
            print 'keeping '+field.name
        elif field.name == 'FULLTEXT':
            print 'keeping '+field.name
        elif field.name == 'DIVISION':
            print 'keeping '+field.name
        elif field.name == 'TOWN':
            print 'keeping '+field.name
        elif field.name == 'SECTOR':
            print 'keeping '+field.name
        elif field.name == 'SYMBOLROTATION':
            print 'keeping '+field.name
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("GAFs2", fieldNameList)
    arcpy.CopyFeatures_management ('GAFs2', USIC+"\\"+"GAFittingTextUSIC.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"GAFittingTextUSIC.shp")
    if arcpy.Exists(GAFs):
        arcpy.Delete_management(GAFs)
    #########--Controllable Fittings
    CF=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.ControllableFitting"
    if arcpy.Exists(USIC+"\\"+"ControllableFittingUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"ControllableFittingUSIC.shp")
    CFs=r"C:\temp\NO_GIS_SP_2.gdb\CFInt"
    arcpy.CopyFeatures_management (CF, CFs)
    arcpy.MakeFeatureLayer_management (CFs, 'CFs2')
    fieldNameList = []
    fields = arcpy.ListFields("CFs2")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'SUBTYPECD':
            print 'keeping '+field.name
        elif field.name == 'COVER':
            print 'keeping '+field.name
        elif field.name == 'LOCATION1':
            print 'keeping '+field.name
        elif field.name == 'DISTANCE1':
            print 'keeping '+field.name
        elif field.name == 'DIRECTION2':
            print 'keeping '+field.name
        elif field.name == 'DIRECTION1':
            print 'keeping '+field.name
        elif field.name == 'DISTANCE2':
            print 'keeping '+field.name
        elif field.name == 'BUILDING1':
            print 'keeping '+field.name
        elif field.name == 'BUILDING2':
            print 'keeping '+field.name
        elif field.name == 'LOCATION2':
            print 'keeping '+field.name
        elif field.name == 'STREET1':
            print 'keeping '+field.name
        elif field.name == 'STREET2':
            print 'keeping '+field.name
        elif field.name == 'SYMBOLROTATION':
            print 'keeping '+field.name
        elif field.name == 'INSULATEDINDICATOR':
            print 'keeping '+field.name
        elif field.name == 'DIVISION':
            print 'keeping '+field.name
        elif field.name == 'TOWN':
            print 'keeping '+field.name
        elif field.name == 'SECTOR':
            print 'keeping '+field.name
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("CFs2", fieldNameList)
    arcpy.CopyFeatures_management ('CFs2', USIC+"\\"+"ControllableFittingUSIC.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"ControllableFittingUSIC.shp")
    if arcpy.Exists(CFs):
        arcpy.Delete_management(CFs)
    ############--Non-Controllable fittings
    NCF=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.NonControllableFitting"
    NCFs=r"C:\temp\NO_GIS_SP_2.gdb\NCFInt"
    arcpy.CopyFeatures_management (NCF, NCFs)
    arcpy.MakeFeatureLayer_management (NCFs, 'NCFs2')
    fieldNameList = []
    fields = arcpy.ListFields("NCFs2")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'SUBTYPECD':
            print 'keeping '+field.name
        elif field.name == 'COVER':
            print 'keeping '+field.name
        elif field.name == 'INSULATEDINDICATOR':
            print 'keeping '+field.name
        elif field.name == 'LOCATION1':
            print 'keeping '+field.name
        elif field.name == 'LOCATION2':
            print 'keeping '+field.name
        elif field.name == 'STREET1':
            print 'keeping '+field.name
        elif field.name == 'STREET2':
            print 'keeping '+field.name
        elif field.name == 'STYLE':
            print 'keeping '+field.name
        elif field.name == 'SYMBOLROTATION':
            print 'keeping '+field.name
        elif field.name == 'DISTANCE1':
            print 'keeping '+field.name
        elif field.name == 'DISTANCE2':
            print 'keeping '+field.name
        elif field.name == 'DIRECTION1':
            print 'keeping '+field.name
        elif field.name == 'DIRECTION2':
            print 'keeping '+field.name
        elif field.name == 'DIVISION':
            print 'keeping '+field.name
        elif field.name == 'TOWN':
            print 'keeping '+field.name
        elif field.name == 'SECTOR':
            print 'keeping '+field.name
        elif field.name == 'DESCRIPTION1':
            print 'keeping '+field.name
        elif field.name == 'LOCATION3':
            print 'keeping '+field.name
        elif field.name == 'DESCRIPTION2':
            print 'keeping '+field.name
        elif field.name == 'COMMENTS':
            print 'keeping '+field.name
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("NCFs2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"NonControllableFittingUSIC"):
        arcpy.Delete_management(USIC+"\\"+"NonControllableFittingUSIC")
    arcpy.CopyFeatures_management ('NCFs2', USIC+"\\"+"NonControllableFittingUSIC")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"NonControllableFittingUSIC.shp")
    if arcpy.Exists(NCFs):
        arcpy.Delete_management(NCFs)
    ################--WO Polys
    MxWoPoly=r"\\parcser02\GisServerManager\Data\pgis3.sde\MXSPAT.WOPoly"
    MxWoPoly2r=r"C:\temp\NO_GIS_SP_2.gdb\MxWoPolyInt"
    arcpy.CopyFeatures_management (MxWoPoly, MxWoPoly2r)
    arcpy.MakeFeatureLayer_management (MxWoPoly2r, 'MxWoPoly2r2')
    fieldNameList = []
    fields = arcpy.ListFields("MxWoPoly2r2")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Area':
            print 'keeping '+field.name
        elif field.name == 'STATUS':
            print 'keeping '+field.name
        elif field.name == 'MXWONUM':
            print 'keeping '+field.name
        elif field.name == 'DESCRIPTION':
            print 'keeping '+field.name
        elif field.name == 'WORKTYPE':
            print 'keeping '+field.name
        elif field.name == 'ZLAC_SUBWORKTYPE':
            print 'keeping '+field.name
        elif field.name == 'ACTFINISH':
            print 'keeping '+field.name
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("MxWoPoly2r2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"WorkOrderUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"WorkOrderUSIC.shp")
    MxWoPolyIntProj=r"C:\temp\NO_GIS_SP_2.gdb\MxWoPolyIntProj"
    if arcpy.Exists(MxWoPolyIntProj):
        arcpy.Delete_management(MxWoPolyIntProj)
    arcpy.Project_management("MxWoPoly2r2",MxWoPolyIntProj,"PROJCS['NAD_1983_StatePlane_Missouri_West_FIPS_2403_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',2788708.333333333],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-94.5],PARAMETER['Scale_Factor',0.9999411764705882],PARAMETER['Latitude_Of_Origin',36.16666666666666],UNIT['Foot_US',0.3048006096012192]]","'WGS_1984_Major_Auxiliary_Sphere_To_WGS_1984 + WGS_1984_(ITRF00)_To_NAD_1983'","PROJCS['WGS_1984_Web_Mercator',GEOGCS['GCS_WGS_1984_Major_Auxiliary_Sphere',DATUM['D_WGS_1984_Major_Auxiliary_Sphere',SPHEROID['WGS_1984_Major_Auxiliary_Sphere',6378137.0,0.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],UNIT['Meter',1.0]]")
    arcpy.MakeFeatureLayer_management (MxWoPolyIntProj, 'MxWoPolyIntProj')
    queried=r"STATUS in ( 'RJCTDFCOMP', 'FCOMP', 'GISREVW', 'WFFILE','CONTRCOMP', 'INPRG', 'LSNC','DISPATCH','ENROUTE','ASBUILTWAPPR','RJCTDASBUILTCOMP','CONTINST','RJCTDASBILTWAPPR','RJCTDWASBUILT','WASBUILT')"
    arcpy.SelectLayerByAttribute_management ('MxWoPolyIntProj', '', queried)
    arcpy.CopyFeatures_management ('MxWoPolyIntProj', USIC+"\\"+"WorkOrderUSIC.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"WorkOrderUSIC.shp")
    if arcpy.Exists(MxWoPoly2r):
        arcpy.Delete_management(MxWoPoly2r)
    ########------Map Grids-----######
    MapGrids=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_LAND.Landbase\LGC_LAND.MapGrid"
    MapGrids2r=r"C:\temp\NO_GIS_SP_2.gdb\MapGridInt"
    arcpy.CopyFeatures_management (MapGrids, MapGrids2r)
    arcpy.MakeFeatureLayer_management (MapGrids2r, 'MapGrids2r2')
    fieldNameList = []
    fields = arcpy.ListFields("MapGrids2r2")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Area':
            print 'keeping '+field.name
        elif field.name == 'MAPID100':
            print 'keeping '+field.name
        elif field.name == 'DISTRICT':
            print 'keeping '+field.name
        elif field.name == 'COUNTY':
            print 'keeping '+field.name
        elif field.name == 'DIVISION':
            print 'keeping '+field.name
        elif field.name == 'TOWN':
            print 'keeping '+field.name
        elif field.name == 'SECTOR':
            print 'keeping '+field.name
        else :
            print 'deleteing '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("MapGrids2r2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"MapGrid.shp"):
        arcpy.Delete_management(USIC+"\\"+"MapGrid.shp")
    arcpy.CopyFeatures_management ('MapGrids2r2', USIC+"\\"+"MapGrid.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"MapGrid.shp")
    if arcpy.Exists(MapGrids2r):
        arcpy.Delete_management(MapGrids2r)
    ####------Gas Valves-----######
    GasValves=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.GasValve"
    GasValves2r=r"C:\temp\NO_GIS_SP_2.gdb\GasValveInt"
    arcpy.CopyFeatures_management (GasValves, GasValves2r)
    arcpy.MakeFeatureLayer_management (GasValves2r, 'GasValves2r2')
    fieldNameList = []
    fields = arcpy.ListFields("GasValves2r2")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Area':
            print 'keeping '+field.name
        elif field.name == 'SUBTYPECD':
            print 'keeping '+field.name
        elif field.name == 'COMMENTS':
            print 'keeping '+field.name
        elif field.name == 'SYMBOLROTATION':
            print 'keeping '+field.name
        elif field.name == 'MATERIAL':
            print 'keeping '+field.name
        elif field.name == 'MATERIALMX':
            print 'keeping '+field.name
        elif field.name == 'VALVEDIAMETER':
            print 'keeping '+field.name
        elif field.name == 'VALVETYPE':
            print 'keeping '+field.name
        elif field.name == 'VALVEUSE':
            print 'keeping '+field.name
        elif field.name == 'CLOCKWISETOCLOSE':
            print 'keeping '+field.name
        elif field.name == 'INSULATEDINDICATOR':
            print 'keeping '+field.name
        elif field.name == 'NORMALPOSITION':
            print 'keeping '+field.name
        elif field.name == 'NUMBEROFTURNS':
            print 'keeping '+field.name
        elif field.name == 'NONESSENTIAL':
            print 'keeping '+field.name
        elif field.name == 'DISTANCE1':
            print 'keeping '+field.name
        elif field.name == 'DIRECTION1':
            print 'keeping '+field.name
        elif field.name == 'LOCATION1':
            print 'keeping '+field.name
        elif field.name == 'STREET1':
            print 'keeping '+field.name
        elif field.name == 'DISTANCE2':
            print 'keeping '+field.name
        elif field.name == 'DIRECTION2':
            print 'keeping '+field.name
        elif field.name == 'LOCATION2':
            print 'keeping '+field.name
        elif field.name == 'BUILDING2':
            print 'keeping '+field.name
        elif field.name == 'BUILDING1':
            print 'keeping '+field.name
        elif field.name == 'STREET2':
            print 'keeping '+field.name
        elif field.name == 'DIRECTION1MX':
            print 'keeping '+field.name
        elif field.name == 'DIRECTION2MX':
            print 'keeping '+field.name
        elif field.name == 'COVER':
            print 'keeping '+field.name
        elif field.name == 'VALVENUMBER':
            print 'keeping '+field.name
        elif field.name == 'VALVELOCATION1':
            print 'keeping '+field.name
        elif field.name == 'VALVELOCATION2':
            print 'keeping '+field.name
        elif field.name == 'VALVELOCATION3':
            print 'keeping '+field.name
        elif field.name == 'FITTINGNUMBER':
            print 'keeping '+field.name
        elif field.name == 'MXLOCATION':
            print 'keeping '+field.name
        elif field.name == 'DIVISION':
            print 'keeping '+field.name
        elif field.name == 'TOWN':
            print 'keeping '+field.name
        elif field.name == 'SECTOR':
            print 'keeping '+field.name
        else :
            print 'deleteing '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("GasValves2r2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"GasValve.shp"):
        arcpy.Delete_management(USIC+"\\"+"GasValve.shp")
    arcpy.CopyFeatures_management ('GasValves2r2', USIC+"\\"+"GasValve.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"GasValve.shp")
    if arcpy.Exists(GasValves2r):
        arcpy.Delete_management(GasValves2r)
    ##############--Abandoned Gas Pipe
    AbandGasPipe=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.AbandonedGasPipe"
    AbandGas=r"C:\temp\NO_GIS_SP_2.gdb\AbandGasInt"
    arcpy.CopyFeatures_management (AbandGasPipe, AbandGas)
    arcpy.MakeFeatureLayer_management (AbandGas, 'AbandGas2')
    fieldNameList = []
    fields = arcpy.ListFields("AbandGas2")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'DATECREATED':
            print 'keeping '+field.name
        elif field.name == 'DATEMODIFIED':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'SUBTYPECD':
            print 'keeping '+field.name
        elif field.name == 'RETIREDDATE':
            print 'keeping '+field.name
        elif field.name == 'FIELDBOOKPATH':
            print 'keeping '+field.name
        elif field.name == 'MATERIALMX':
            print 'keeping '+field.name
        elif field.name == 'REASON':
            print 'keeping '+field.name
        elif field.name == 'NOMINALDIAMETER':
            print 'keeping '+field.name
        elif field.name == 'RETIREDDATE':
            print 'keeping '+field.name
        elif field.name == 'MATERIAL':
            print 'keeping '+field.name
        elif field.name == 'WORKREQUESTID':
            print 'keeping '+field.name
        elif field.name == 'OPERATINGPRESSURE':
            print 'keeping '+field.name
        elif field.name == 'JOINTTRENCH':
            print 'keeping '+field.name
        elif field.name == 'DATEINSTALLED':
            print 'keeping '+field.name
        elif field.name == 'COATINGTYPE':
            print 'keeping '+field.name
        elif field.name == 'MAINTYPE':
            print 'keeping '+field.name
        elif field.name == 'COUNTY':
            print 'keeping '+field.name
        elif field.name == 'DIVISION':
            print 'keeping '+field.name
        elif field.name == 'TOWN':
            print 'keeping '+field.name
        elif field.name == 'SECTOR':
            print 'keeping '+field.name
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    print fieldNameList
    arcpy.DeleteField_management ("AbandGas2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"AbandonedGasPipeUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"AbandonedGasPipeUSIC.shp")
    arcpy.CopyFeatures_management ('AbandGas2', USIC+"\\"+"AbandonedGasPipeUSIC.shp")
    arcpy.MakeFeatureLayer_management (USIC+"\\"+"AbandonedGasPipeUSIC.shp", 'DistsssCalc')
    arcpy.AddField_management("DistsssCalc","FieldNote","TEXT","#","#","200","#","NULLABLE","NON_REQUIRED","#")
    arcpy.SelectLayerByAttribute_management ('DistsssCalc', '','"FIELDBOOKP" = '+"' '" )
    arcpy.CalculateField_management("DistsssCalc","FIELDBOOKP",'"None"',"PYTHON_9.3","#")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"AbandonedGasPipeUSIC.shp")
    if arcpy.Exists(AbandGas):
        arcpy.Delete_management(AbandGas)
    arcpy.DeleteField_management("DistsssCalc","FIELDBOOKP")
    ############--Abandoned Services
    AbandGasSrv=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.AbandonedGasService"
    AbandGasSer=r"C:\temp\NO_GIS_SP_2.gdb\AbandGasSerInt"
    arcpy.CopyFeatures_management (AbandGasSrv, AbandGasSer)
    arcpy.MakeFeatureLayer_management (AbandGasSer, 'AbandGasSer2')
    fieldNameList = []
    fields = arcpy.ListFields("AbandGasSer2")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'SUBTYPECD':
            print 'keeping '+field.name
        elif field.name == 'NOMINALDIAMETER':
            print 'keeping '+field.name
        elif field.name == 'MATERIAL':
            print 'keeping '+field.name
        elif field.name == 'FIELDBOOKPATH':
            print 'keeping '+field.name
        elif field.name == 'MXSTREETADDRESS':
            print 'keeping '+field.name
        elif field.name == 'MXTEELOCATION':
            print 'keeping '+field.name
        elif field.name == 'MXTEEDESCRIPTION':
            print 'keeping '+field.name
        elif field.name == 'MXCURBBOXLOCATION':
            print 'keeping '+field.name
        elif field.name == 'MXCURBDESCRIPTION':
            print 'keeping '+field.name
        elif field.name == 'MXSERVICELOCATION':
            print 'keeping '+field.name
        elif field.name == 'MXSERVICEDESCRIPTION':
            print 'keeping '+field.name
        elif field.name == 'MXRISERLOCATION':
            print 'keeping '+field.name
        elif field.name == 'MXRISERDESCRIPTION':
            print 'keeping '+field.name
        elif field.name == 'MXMAINLOCATION':
            print 'keeping '+field.name
        elif field.name == 'MXMAINSIZE':
            print 'keeping '+field.name
        elif field.name == 'MXMAINMATERIAL':
            print 'keeping '+field.name
        elif field.name == 'DATECREATED':
            print 'keeping '+field.name
        elif field.name == 'DATEMODIFIED':
            print 'keeping '+field.name
        elif field.name == 'OPERATINGPRESSURE':
            print 'keeping '+field.name
        elif field.name == 'MATERIAL':
            print 'keeping '+field.name
        elif field.name == 'STREETNUMBER':
            print 'keeping '+field.name
        elif field.name == 'STREETNAME':
            print 'keeping '+field.name
        elif field.name == 'STREETSUFFIX':
            print 'keeping '+field.name
        elif field.name == 'ONE_HUNDRED_FOOT_DISPLAY':
            print 'keeping '+field.name
        elif field.name == 'REASON':
            print 'keeping '+field.name
        elif field.name == 'DIVISION':
            print 'keeping '+field.name
        elif field.name == 'TOWN':
            print 'keeping '+field.name
        elif field.name == 'SECTOR':
            print 'keeping '+field.name
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("AbandGasSer2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"AbandonedGasServiceUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"AbandonedGasServiceUSIC.shp")
    arcpy.CopyFeatures_management ('AbandGasSer2', USIC+"\\"+"AbandonedGasServiceUSIC.shp")
    arcpy.MakeFeatureLayer_management (USIC+"\\"+"AbandonedGasServiceUSIC.shp", 'DistsssCalc')
    arcpy.AddSpatialIndex_management (USIC+"\\"+"AbandonedGasServiceUSIC.shp")
    if arcpy.Exists(AbandGasSer):
        arcpy.Delete_management(AbandGasSer)
    arcpy.DeleteField_management("DistsssCalc","FIELDBOOKP")
    ######--Services#################
    Srv=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.Service"
    servs=r"C:\temp\NO_GIS_SP_2.gdb\SerInterim"
    if arcpy.Exists(USIC+"\\"+"ServiceUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"ServiceUSIC.shp")
    arcpy.MakeFeatureLayer_management (Srv, 'SrvLyr')
    arcpy.SelectLayerByAttribute_management ('SrvLyr', '',"NOT FIELDBOOKPATH = 'NO FIELDBOOK'  OR OWNER = 'MoNat'" )
    arcpy.CopyFeatures_management('SrvLyr',servs)
    ##arcpy.CopyFeatures_management(Srv,servs)
    if arcpy.Exists("Servs"):
        arcpy.Delete_management("Servs")
    arcpy.MakeFeatureLayer_management (servs, 'Servs')
    fieldNameList = []
    fields = arcpy.ListFields("Servs")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'DATECREATED':
            print 'keeping '+field.name
        elif field.name == 'MXSTATUS':
            print 'keeping '+field.name
        elif field.name == 'STREETADDRESS':
            print 'keeping '+field.name
        elif field.name == 'SERVICETYPE':
            print 'keeping '+field.name
        elif field.name == 'BRANCHTYPE':
            print 'keeping '+field.name
        elif field.name == 'SERVICENUMBER':
            print 'keeping '+field.name
        elif field.name == 'FIELDBOOKPATH':
            print 'keeping '+field.name
        elif field.name == 'TEELOCATION':
            print 'keeping '+field.name
        elif field.name == 'TEEDESCRIPTION':
            print 'keeping '+field.name
        elif field.name == 'CURBBOXLOCATION':
            print 'keeping '+field.name
        elif field.name == 'CURBDESCRIPTION':
            print 'keeping '+field.name
        elif field.name == 'SERVICELOCATION':
            print 'keeping '+field.name
        elif field.name == 'SERVICEDESCRIPTION':
            print 'keeping '+field.name
        elif field.name == 'RISERLOCATION':
            print 'keeping '+field.name
        elif field.name == 'RISERDESCRIPTION':
            print 'keeping '+field.name
        elif field.name == 'MAINLOCATION':
            print 'keeping '+field.name
        elif field.name == 'MAINDESCRIPTION':
            print 'keeping '+field.name
        elif field.name == 'MAINDEPTH':
            print 'keeping '+field.name
        elif field.name == 'MAINSIZE':
            print 'keeping '+field.name
        elif field.name == 'MAINMATERIAL':
            print 'keeping '+field.name
        elif field.name == 'EFV':
            print 'keeping '+field.name 
        elif field.name == 'SUBTYPECD':
            print 'keeping '+field.name
        elif field.name == 'MXLOCATION':
            print 'keeping '+field.name
        elif field.name == 'DIVISION':
            print 'keeping '+field.name
        elif field.name == 'TOWN':
            print 'keeping '+field.name
        elif field.name == 'SECTOR':
            print 'keeping '+field.name
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("Servs", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"ServiceUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"ServiceUSIC.shp")
    arcpy.CopyFeatures_management("Servs",USIC+"\\"+"ServiceUSIC.shp")
    arcpy.MakeFeatureLayer_management (USIC+"\\"+"ServiceUSIC.shp", 'DistsssCalc')
    arcpy.AddField_management("DistsssCalc","FieldNote","TEXT","#","#","200","#","NULLABLE","NON_REQUIRED","#")
    arcpy.SelectLayerByAttribute_management ('DistsssCalc', '','"FIELDBOOKP" = '+"' '" )
    arcpy.CalculateField_management("DistsssCalc","FIELDBOOKP",'"None"',"PYTHON_9.3","#")
    cursor = arcpy.UpdateCursor(USIC+"\\"+"ServiceUSIC.shp")
    for row in cursor:
        fromRow=row.getValue('FIELDBOOKP')
        fromRows=fromRow
        if fromRows.rfind('\\')>0:
            that=fromRows.rfind('\\')
            that1= that+1
            theother=len(fromRow)
            print int(theother)
            ok=fromRows[that1:theother]
            ok2=ok.strip()
            these=fromRows.replace(str(that1),'')
            row.setValue('FieldNote', ok2)
            cursor.updateRow(row)
        if fromRows.rfind('/')>0:
            thats=fromRows.rfind('/')
            that1= thats+1
            theother=len(fromRow)
            print int(theother)
            ok=fromRows[that1:theother]
            ok2=ok.strip()
            these=fromRows.replace(str(that1),'')
            row.setValue('FieldNote', ok2)
            cursor.updateRow(row)        
    del row,cursor    
    from datetime import date, timedelta
    import datetime
    CUR_DATE = datetime.date.today().strftime('%Y-%m-%d')
    d = date.today() - timedelta(days=14)
    query='"DATECREATE" <= date '+"'"+CUR_DATE+"' AND "+'"DATECREATE" >= date '+"'"+str(d)+"'"
    print query
    arcpy.SelectLayerByAttribute_management ('DistsssCalc', '',query )
    cursor = arcpy.SearchCursor('DistsssCalc')
    import os
    arcpy.env.workspace = USICpdf
    import shutil
    for row in cursor:
        fromRows=row.getValue('FIELDBOOKP')
        if fromRows <>'None':
            if fromRows<>'\\\\gisappser2\\Engineering_GIS\\CompressedFieldBooks\\FieldBooks\\MoNatSketches':
                if fromRows<> 'NO FIELDBOOK':
                    print fromRows
                    shutil.copy2(fromRows, USICpdf)
    ##del row,cursor
    del cursor
    arcpy.AddSpatialIndex_management (USIC+"\\"+"ServiceUSIC.shp")
    if arcpy.Exists(servs):
        arcpy.Delete_management(servs)
    arcpy.DeleteField_management("DistsssCalc","FIELDBOOKP")
    ############--Distribution Main USIC---#######
    Dist=r"\\stl-pgisarc-120\gisservermanager\Data\Connection to GISM.sde\LGC_GAS.GasFacilities\LGC_GAS.DistributionMain"
    Dists=r"C:\temp\NO_GIS_SP_2.gdb\DistInterim2"
    USIC=r"\\pdatfile01\ProdData\GIS\USIC\MoWest"
    arcpy.CopyFeatures_management(Dist,Dists)
    arcpy.MakeFeatureLayer_management (Dists, 'Distsss')
    fieldNameList = []
    fields = arcpy.ListFields("Distsss")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'MXLOCATION':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'NOMINALDIAMETER':
            print 'keeping '+field.name
        elif field.name == 'DATEINSTALLED':
            print 'keeping '+field.name
        elif field.name == 'JOINTTRENCH':
            print 'keeping '+field.name
        elif field.name == 'LENGTHMX':
            print 'keeping '+field.name
        elif field.name == 'MATERIALMX':
            print 'keeping '+field.name
        elif field.name == 'MATERIAL':
            print 'keeping '+field.name
        elif field.name == 'FIELDBOOKPATH':
            print 'keeping '+field.name
        elif field.name == 'OPERATINGPRESSURE':
            print 'keeping '+field.name
        elif field.name == 'COATINGTYPE':
            print 'keeping '+field.name
        elif field.name == 'RELAYEDSIZE':
            print 'keeping '+field.name
        elif field.name == 'RELAYEDMATERIAL':
            print 'keeping '+field.name
        elif field.name == 'MAOP':
            print 'keeping '+field.name
        elif field.name == 'MOP':
            print 'keeping '+field.name
        elif field.name == 'DIVISION':
            print 'keeping '+field.name
        elif field.name == 'TOWN':
            print 'keeping '+field.name
        elif field.name == 'SECTOR':
            print 'keeping '+field.name
        elif field.name == 'WORKORDERNUMBER':
            print 'keeping '+field.name
            
        else :
            print 'deleting '+field.name
            fieldNameList.append(field.name)
    print fieldNameList
    arcpy.DeleteField_management ("Distsss", fieldNameList)
    arcpy.AddField_management("Distsss","Yr","SHORT")
    query=r"NOT DATEINSTALLED IS NULL AND NOT MXLOCATION = 'GMN001422772'" 
    arcpy.CalculateField_management("Distsss","Yr","len( !DATEINSTALLED! )","PYTHON","#")
    arcpy.SelectLayerByAttribute_management ("Distsss", "", r"NOT Yr >10")
    arcpy.CalculateField_management("Distsss","Yr","datetime.datetime.strptime(!DATEINSTALLED!, '%m/%d/%Y').year ","PYTHON","#")
    if arcpy.Exists(USIC+"\\"+"DistributionMainUSIC.shp"):
        arcpy.Delete_management(USIC+"\\"+"DistributionMainUSIC.shp")
    arcpy.SelectLayerByAttribute_management ("Distsss", "CLEAR_SELECTION")
    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"DistributionMainUSIC.shp")
    arcpy.MakeFeatureLayer_management (USIC+"\\"+"DistributionMainUSIC.shp", 'DistsssCalc')
    arcpy.AddField_management("DistsssCalc","FieldNote","TEXT","#","#","200","#","NULLABLE","NON_REQUIRED","#")
    arcpy.AddField_management("DistsssCalc","WORKORDERP","TEXT","#","#","200","#","NULLABLE","NON_REQUIRED","#")
    query=r'"WORKORDERN" in '+"( ' ', '0', 'NA','NONE' ) OR "+'"DIVISION" = '+"'04'"
    arcpy.SelectLayerByAttribute_management ("DistsssCalc", "", query)
    arcpy.SelectLayerByAttribute_management ("DistsssCalc", "SWITCH_SELECTION", "")
    print 'calculating work order p'
    arcpy.CalculateField_management("DistsssCalc", "WORKORDERP", '!WORKORDERN!+".TIF"', "PYTHON_9.3", "")
    arcpy.SelectLayerByAttribute_management ('DistsssCalc', '','"FIELDBOOKP" = '+"' '" )
    arcpy.CalculateField_management("DistsssCalc","FIELDBOOKP",'"None"',"PYTHON_9.3","#")
    cursor = arcpy.UpdateCursor(USIC+"\\"+"DistributionMainUSIC.shp")
    for row in cursor:
        fromRow=row.getValue('FIELDBOOKP')
        fromRows=fromRow
        if fromRows.rfind('\\')>0:
            that=fromRows.rfind('\\')
            that1= that+1
            theother=len(fromRow)
            ok=fromRows[that1:theother]
            ok2=ok.strip()
            these=fromRows.replace(str(that1),'')
            row.setValue('FieldNote', ok2)
            cursor.updateRow(row)
        if fromRows.rfind('/')>0:
            thats=fromRows.rfind('/')
            that1= thats+1
            theother=len(fromRow)
##            print int(theother)
            ok=fromRows[that1:theother]
            ok2=ok.strip()
            these=fromRows.replace(str(that1),'')
            row.setValue('FieldNote', ok2)
            cursor.updateRow(row)        
    del row,cursor    
    from datetime import date, timedelta
    import datetime
    CUR_DATE = datetime.date.today().strftime('%Y-%m-%d')
    d = date.today() - timedelta(days=14)
    query='"DATEINSTAL" <= date '+"'"+CUR_DATE+"' AND "+'"DATEINSTAL" >= date '+"'"+str(d)+"'"
    print query
    arcpy.SelectLayerByAttribute_management ('DistsssCalc', '',query )
    cursor = arcpy.SearchCursor('DistsssCalc')
    import os
    arcpy.env.workspace = USICpdf
    for csv_file in arcpy.ListFiles("*.pdf"):
        print csv_file
        os.remove(USICpdf+"\\"+csv_file)
    import shutil
    for row in cursor:
        fromRows=row.getValue('FIELDBOOKP')
        if fromRows <>'None':
            if arcpy.Exists(fromRows):
                shutil.copy2(fromRows, USICpdf)
            else:
                print 'This pdf doesnt exist! '+fromRows
    arcpy.SelectLayerByAttribute_management ('DistsssCalc', '','"FieldNote" LIKE '+"'%TIF%'" )
    arcpy.CalculateField_management("DistsssCalc","FieldNote",'""',"PYTHON_9.3","#")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"DistributionMainUSIC.shp")
    if arcpy.Exists(Dists):
        arcpy.Delete_management(Dists)
    arcpy.DeleteField_management("DistsssCalc","FIELDBOOKP")
    arcpy.MakeFeatureLayer_management (USIC+"\\"+"DistributionMainUSIC.shp", 'DistsssCalc2')
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"    
    log.write("" + pymsg + "\n")
    log.write("" + msgs + "")
    log.close()
