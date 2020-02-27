import sys, string, os, arcpy, calendar, datetime, traceback
from arcpy import env
try:
    d = datetime.datetime.now()
    log = open("C:\\Temp\PythonOutputLogFile.txt","a")
    log.write("----------------------------" + "\n")
    log.write("----------------------------" + "\n")
    log.write("Log: " + str(d) + "\n")
    log.write("\n")
    arcpy.env.overwriteOutput=True

    ######--Dimension Text MoNat USIC---
    Dist=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_LAND.Landbase\LGC_LAND.MoNatDimText"
    Dists=r"C:\temp\NO_GIS_SP_2.gdb\DimDimInterim"
    USIC=r"\\pdatfile01\ProdData\GIS\USIC\MoEast"
    USICpdf=r"\\pdatfile01\ProdData\GIS\USIC\MoEast"
    if arcpy.Exists(Dists):
        arcpy.Delete_management(Dists)
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
        elif field.name == 'SYMBOLROTATION':
            print 'keeping '+field.name
        elif field.name == 'SHAPE':
            print 'keeping '+field.name
        elif field.name == 'COUNTY':
            print 'keeping '+field.name
        elif field.name == 'DIMENSION':
            print 'keeping '+field.name   
        else :
            print 'deleting '+field.name
            fieldNameList.append(field.name)
    print fieldNameList
    arcpy.DeleteField_management ("Distsss", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"DimMoNatTextUSICMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"DimMoNatTextUSICMoEast.shp")
    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"DimMoNatTextUSICMoEast.shp")
    ##########--Marker Ball USIC---##
    Dist=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_GAS.GasFacilities\LGC_GAS.LocationIndicator"
    Dists=r"C:\temp\NO_GIS_SP_2.gdb\LocIndInterim"
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
    if arcpy.Exists(USIC+"\\"+"MarkerBallUSICMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"MarkerBallUSICMoEast.shp")
    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"MarkerBallUSICMoEast.shp")
    ######--Dimension Line MoNat USIC---
    Dist=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_LAND.Landbase\LGC_LAND.MoNatDimLine"
    Dists=r"C:\temp\NO_GIS_SP_2.gdb\DimLineInterim"
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
        elif field.name == 'OWNER':
            print 'COVER '+field.name
        elif field.name == 'SHAPE.LEN':
            print 'COVER '+field.name
        elif field.name == 'SHAPE':
            print 'COVER '+field.name
        else :
            print 'deleting '+field.name
            fieldNameList.append(field.name)
    print fieldNameList
    arcpy.DeleteField_management ("Distsss", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"DimLineMoNatUSICMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"DimLineMoNatUSICMoEast.shp")
    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"DimLineMoNatUSICMoEast.shp")
    ##########--Distribution Main Dimension USIC---
    Dist=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_GAS.GasFacilities\LGC_GAS.DistributionMainDimension"
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
    if arcpy.Exists(USIC+"\\"+"DistributionMainDimUSICMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"DistributionMainDimUSICMoEast.shp")
    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"DistributionMainDimUSICMoEast.shp")
    ######--Service Point--#########
    SP=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_GAS.GasFacilities\LGC_GAS.ServicePoint"
    SPs=r"C:\temp\NO_GIS_SP_2.gdb\SPInterim"
    arcpy.CopyFeatures_management(SP,SPs)
    arcpy.MakeFeatureLayer_management (SPs, 'SPss')
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
        elif field.name == 'SERVICEMXLOCATION':
            print 'keeping '+field.name
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("SPss", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"ServicePointUSICMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"ServicePointUSICMoEast.shp")
    arcpy.CopyFeatures_management ('SPss', USIC+"\\"+"ServicePointUSICMoEast.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"ServicePointUSICMoEast.shp")
    if arcpy.Exists(SPs):
        arcpy.Delete_management(SPs)
    ################--Test Points
    TP=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_GAS.GasFacilities\LGC_GAS.CPTestPoint"
    if arcpy.Exists(USIC+"\\"+"AnodeUSICMoEast"):
        arcpy.Delete_management(USIC+"\\"+"AnodeUSICMoEast.shp")
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
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("anode2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"AnodeUSICMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"AnodeUSICMoEast.shp")
    arcpy.CopyFeatures_management("anode2",USIC+"\\"+"AnodeUSICMoEast.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"AnodeUSICMoEast.shp")
    if arcpy.Exists(anode):
        arcpy.Delete_management(anode)
    #########--Controllable Fittings
    CF=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_GAS.GasFacilities\LGC_GAS.ControllableFitting"
    if arcpy.Exists(USIC+"\\"+"ControllableFittingUSICMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"ControllableFittingUSICMoEast.shp")
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
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("CFs2", fieldNameList)
    arcpy.CopyFeatures_management ('CFs2', USIC+"\\"+"ControllableFittingUSICMoEast.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"ControllableFittingUSICMoEast.shp")
    if arcpy.Exists(CFs):
        arcpy.Delete_management(CFs)
    ##############--Non-Controllable fittings
    NCF=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_GAS.GasFacilities\LGC_GAS.NonControllableFitting"
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
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("NCFs2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"NonControllableFittingMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"NonControllableFittingMoEast.shp")
    arcpy.CopyFeatures_management ('NCFs2', USIC+"\\"+"NonControllableFittingMoEast.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"NonControllableFittingMoEast.shp")
    if arcpy.Exists(NCFs):
        arcpy.Delete_management(NCFs)
    ##########--Abandoned Services
    AbandGasSrv=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_GAS.GasFacilities\LGC_GAS.AbandonedGasService"
    AbandGasSer=r"C:\temp\NO_GIS_SP_2.gdb\AbandGasSerInt"
    if arcpy.Exists(AbandGasSer):
        arcpy.Delete_management(AbandGasSer)
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
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("AbandGasSer2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"AbandonedGasServiceUSICMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"AbandonedGasServiceUSICMoEast.shp")
    arcpy.CopyFeatures_management ('AbandGasSer2', USIC+"\\"+"AbandonedGasServiceUSICMoEast.shp")
    arcpy.MakeFeatureLayer_management (USIC+"\\"+"AbandonedGasServiceUSICMoEast.shp", 'DistsssCalc')
    arcpy.AddSpatialIndex_management (USIC+"\\"+"AbandonedGasServiceUSICMoEast.shp")
    if arcpy.Exists(AbandGasSer):
        arcpy.Delete_management(AbandGasSer)
    arcpy.DeleteField_management("DistsssCalc","FIELDBOOKP")
    ###############--WO Polys
    MxWoPoly=r"\\parcser02\gisservermanager\Data\pgis3.sde\MXSPAT.WOPoly"
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
    ####------Drip-----######
    Drips=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_GAS.GasFacilities\LGC_GAS.Drip"
    Drips2r=r"C:\temp\NO_GIS_SP_2.gdb\DripInt"
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
        elif field.name == 'LOCATION1':
            print 'keeping '+field.name
        elif field.name == 'LOCATION2':
            print 'keeping '+field.name
        elif field.name == 'DIRECTION1':
            print 'keeping '+field.name
        elif field.name == 'STREET1':
            print 'keeping '+field.name
        elif field.name == 'DISTANCE2':
            print 'keeping '+field.name
        elif field.name == 'DIRECTION2':
            print 'keeping '+field.name
        elif field.name == 'STREET2':
            print 'keeping '+field.name
        elif field.name == 'MXLOCATION':
            print 'keeping '+field.name
        elif field.name == 'COVER':
            print 'keeping '+field.name
        elif field.name == 'SUBTYPECD':
            print 'keeping '+field.name
        elif field.name == 'BUILDING1':
            print 'keeping '+field.name
        elif field.name == 'BUILDING2':
            print 'keeping '+field.name
        else :
            print 'deleteing '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("Drips2r2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"DripMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"DripMoEast.shp")
    arcpy.CopyFeatures_management ('Drips2r2', USIC+"\\"+"DripMoEast.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"DripMoEast.shp")
    if arcpy.Exists(Drips2r):
        arcpy.Delete_management(Drips2r)
    ########------Gas Valves-----######
    GasValves=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_GAS.GasFacilities\LGC_GAS.GasValve"
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
        else :
            print 'deleteing '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("GasValves2r2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"GasValveMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"GasValveMoEast.shp")
    arcpy.CopyFeatures_management ('GasValves2r2', USIC+"\\"+"GasValveMoEast.shp")
    arcpy.AddSpatialIndex_management (USIC+"\\"+"GasValveMoEast.shp")
    if arcpy.Exists(GasValves2r):
        arcpy.Delete_management(GasValves2r)
    ####--Distribution Main USIC---
    Dist=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_GAS.GasFacilities\LGC_GAS.DistributionMain"
    Dists=r"C:\temp\NO_GIS_SP_2.gdb\DistInterim3"
    if arcpy.Exists(Dists):
        arcpy.Delete_management(Dists)
    query=r"NOT OWNER in ( 'Southern Star', 'MRT') AND NOT OWNER IS NULL"
    arcpy.MakeFeatureLayer_management (Dist, 'DistLyr')
    arcpy.SelectLayerByAttribute_management ('DistLyr', '',query )
    arcpy.CopyFeatures_management('DistLyr',Dists)
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
            
        else :
            print 'deleting '+field.name
            fieldNameList.append(field.name)
    print fieldNameList
    arcpy.DeleteField_management ("Distsss", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"DistributionMainUSICMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"DistributionMainUSICMoEast.shp")
    arcpy.CopyFeatures_management ('Distsss', USIC+"\\"+"DistributionMainUSICMoEast.shp")
    arcpy.MakeFeatureLayer_management (USIC+"\\"+"DistributionMainUSICMoEast.shp", 'DistsssCalc')
    arcpy.AddField_management("DistsssCalc","FieldNote","TEXT","#","#","200","#","NULLABLE","NON_REQUIRED","#")
    arcpy.SelectLayerByAttribute_management ('DistsssCalc', '','"FIELDBOOKP" = '+"' '" )
    arcpy.CalculateField_management("DistsssCalc","FIELDBOOKP",'"None"',"PYTHON_9.3","#")
    arcpy.SelectLayerByAttribute_management ('DistsssCalc','CLEAR_SELECTION')
    cursor = arcpy.UpdateCursor(USIC+"\\"+"DistributionMainUSICMoEast.shp")
    for row in cursor:
        fromRow=row.getValue('FIELDBOOKP')
        fromRows=fromRow
##        print fromRows
        if fromRows.rfind('\\')>0:
            that=fromRows.rfind('\\')
            that1= that+1
            theother=len(fromRow)
##            print int(theother)
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
    Dists4=r"C:\temp\NO_GIS_SP_2.gdb\DistInterim4"
    if arcpy.Exists(Dists4):
        arcpy.Delete_management(Dists4)
    arcpy.CopyFeatures_management ('DistsssCalc', Dists4)
    arcpy.MakeFeatureLayer_management (Dists4, 'DistsssCalc2')
    cursor = arcpy.SearchCursor('DistsssCalc2')
    import os
    arcpy.env.workspace = USICpdf
    for csv_file in arcpy.ListFiles("*.pdf"):
        os.remove(USICpdf+"\\"+csv_file)
    import shutil
    for row in cursor:
        fromRows=row.getValue('FIELDBOOKP')
        print fromRows
        if fromRows <>'None':
            if arcpy.Exists(fromRows):
                shutil.copy2(fromRows, USICpdf)
            else:
                print 'OS Error'
    del row,cursor
    arcpy.AddSpatialIndex_management (USIC+"\\"+"DistributionMainUSICMoEast.shp")
    if arcpy.Exists(Dists):
        arcpy.Delete_management(Dists)
    arcpy.DeleteField_management("DistsssCalc","FIELDBOOKP")
    ############--Services#################
    Srv=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_GAS.GasFacilities\LGC_GAS.Service"
    servs=r"C:\temp\NO_GIS_SP_2.gdb\SerInterim"
    servs2=r"C:\temp\NO_GIS_SP_2.gdb\SerInterim2"
    if arcpy.Exists(USIC+"\\"+"ServiceUSICMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"ServiceUSICMoEast.shp")
    if arcpy.Exists(servs):
        arcpy.Delete_management(servs)
    arcpy.CopyFeatures_management(Srv,servs)
    query=r"(NOT FIELDBOOKPATH IS null AND NOT FIELDBOOKPATH = 'NO FIELDBOOK' ) OR( OWNER = 'MoNat')"
    arcpy.MakeFeatureLayer_management (servs, 'ServsLyr')
    arcpy.SelectLayerByAttribute_management ('ServsLyr', '',query )
    if arcpy.Exists(servs2):
        arcpy.Delete_management(servs2)
    arcpy.CopyFeatures_management('ServsLyr',servs2)
    arcpy.MakeFeatureLayer_management (servs2, 'Servs')
    fieldNameList = []
    fields = arcpy.ListFields("Servs")
    for field in fields:
        if field.name == 'OBJECTID':
            print 'keeping '+field.name
        elif field.name == 'SHAPE_Length':
            print 'keeping '+field.name
        elif field.name == 'OWNER':
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
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    arcpy.DeleteField_management ("Servs", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"ServiceUSICMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"ServiceUSICMoEast.shp")
    arcpy.CopyFeatures_management("Servs",USIC+"\\"+"ServiceUSICMoEast.shp")
    arcpy.MakeFeatureLayer_management (USIC+"\\"+"ServiceUSICMoEast.shp", 'DistsssCalc')
    arcpy.AddField_management("DistsssCalc","FieldNote","TEXT","#","#","200","#","NULLABLE","NON_REQUIRED","#")
    arcpy.SelectLayerByAttribute_management ('DistsssCalc', '','"FIELDBOOKP" = '+"' '" )
    arcpy.CalculateField_management("DistsssCalc","FIELDBOOKP",'"None"',"PYTHON_9.3","#")
    cursor = arcpy.UpdateCursor(USIC+"\\"+"ServiceUSICMoEast.shp")
    for row in cursor:
        fromRow=row.getValue('FIELDBOOKP')
        fromRows=fromRow
##        print fromRows
        if fromRows.rfind('\\')>0:
            that=fromRows.rfind('\\')
            that1= that+1
            theother=len(fromRow)
##            print int(theother)
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
    query='"DATECREATE" <= date '+"'"+CUR_DATE+"' AND "+'"DATECREATE" >= date '+"'"+str(d)+"'"
    print query
    arcpy.SelectLayerByAttribute_management ('DistsssCalc', '',query )
    cursor = arcpy.SearchCursor('DistsssCalc')
    import os
    arcpy.env.workspace = USICpdf
    import shutil
    for row in cursor:
        fromRows=row.getValue('FIELDBOOKP')
##        print fromRows
        if fromRows <>'NO FIELDBOOK':
            if arcpy.Exists(fromRows):
                shutil.copy2(fromRows, USICpdf)
            else:
                print 'OS Error'
##    del row,cursor
    import shutil
    for row in cursor:
        fromRows=row.getValue('FIELDBOOKP')
        if fromRows.find(r'\\gisappser2\images'):
            if fromRows<>r'\\gisappser2\images\Laclede Gas\pdf\pdf 2B checked\Laclede\1643-75.pdf':
                if fromRows <>'NO FIELDBOOK':
                    shutil.copy2(fromRows, USICpdf)
    del row,cursor
    arcpy.AddSpatialIndex_management (USIC+"\\"+"ServiceUSICMoEast.shp")
    if arcpy.Exists(servs):
        arcpy.Delete_management(servs)
    if arcpy.Exists(servs2):
        arcpy.Delete_management(servs2)
    arcpy.DeleteField_management("DistsssCalc","FIELDBOOKP")
    ##############--Abandoned Gas Pipe
    AbandGasPipe=r"\\parcser02\GisServerManager\Data\PGISE.sde\LGC_GAS.GasFacilities\LGC_GAS.AbandonedGasPipe"
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
        else :
            print 'keeping '+field.name
            fieldNameList.append(field.name)
    print fieldNameList
    arcpy.DeleteField_management ("AbandGas2", fieldNameList)
    if arcpy.Exists(USIC+"\\"+"AbandonedGasPipeUSICMoEast.shp"):
        arcpy.Delete_management(USIC+"\\"+"AbandonedGasPipeUSICMoEast.shp")
    arcpy.CopyFeatures_management ('AbandGas2', USIC+"\\"+"AbandonedGasPipeUSICMoEast.shp")
    arcpy.MakeFeatureLayer_management (USIC+"\\"+"AbandonedGasPipeUSICMoEast.shp", 'DistsssCalc')
    arcpy.AddField_management("DistsssCalc","FieldNote","TEXT","#","#","200","#","NULLABLE","NON_REQUIRED","#")
    arcpy.SelectLayerByAttribute_management ('DistsssCalc', '','"FIELDBOOKP" = '+"' '" )
    arcpy.CalculateField_management("DistsssCalc","FIELDBOOKP",'"None"',"PYTHON_9.3","#")
    cursor = arcpy.UpdateCursor(USIC+"\\"+"AbandonedGasPipeUSICMoEast.shp")
    for row in cursor:
        fromRow=row.getValue('FIELDBOOKP')
        fromRows=fromRow
        print fromRows
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
    arcpy.AddSpatialIndex_management (USIC+"\\"+"AbandonedGasPipeUSICMoEast.shp")
    if arcpy.Exists(AbandGas):
        arcpy.Delete_management(AbandGas)
    arcpy.DeleteField_management("DistsssCalc","FIELDBOOKP")
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"    
    log.write("" + pymsg + "\n")
    log.write("" + msgs + "")
    print(msgs)
    log.close()
