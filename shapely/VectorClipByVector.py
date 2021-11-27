#coding:utf-8
from osgeo import gdal,osr,ogr
from shapely import geometry
from shapely.geometry import MultiPolygon
from shapely.geometry import MultiLineString
from shapely.geometry import MultiPoint
from shapely.geometry import Polygon
from shapely import wkt
#打开文件

def vectorclipbyvector(strinputbase,strinputclip,stroutput):
    #fn1=r"E:\shptest\DWFL_2018.shp"
    #fn2=r"E:\shptest\DWFL_2016.shp"
    datasource=ogr.Open(strinputbase,False)
    datasourcebefor=ogr.Open(strinputclip,False)
    #查看矢量图层的数目,shp文件只有一个图层
    layer_num=datasource.GetLayerCount()
    layer_numbefor=datasourcebefor.GetLayerCount()
    #获取矢量图层
    layer=datasource.GetLayerByIndex(0)  #矢量的索引从0开始，栅格的索引从1开始
    layer_before=datasourcebefor.GetLayerByIndex(0)
    #获取空间参考
    spatial_ref=layer.GetSpatialRef()
    spatial_refBefore=layer_before.GetSpatialRef()
    #获取每个要素的属性信息
    print ("SpatialReference: ",spatial_ref)
    print ("LayerCount: ",layer_num)
    print("Elements number:",layer.GetFeatureCount())
    print ("SpatialReference before: ",spatial_refBefore)
    print ("LayerCount before: ",layer_numbefor)
    print("Elements number before:",layer_before.GetFeatureCount())
    #计算裁剪后的矢量
    #写入矢量文件
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")  # 为了支持中文路径
    gdal.SetConfigOption("SHAPE_ENCODING", "CP936")  # 为了使属性表字段支持中文
    #stroutput = "E:\shptest\DWFL_2017.shp" # 定义写入路径及文件名
    ogr.RegisterAll()  # 注册所有的驱动
    strDriverName = "ESRI Shapefile"  # 创建数据，这里创建ESRI的shp文件
    oDriver = ogr.GetDriverByName(strDriverName)
    if oDriver == None:
        print("%s 驱动不可用！\n", strDriverName)
    
    oDS = oDriver.CreateDataSource(stroutput)  # 创建数据源
    if oDS == None:
        print("创建文件【%s】失败！", stroutput)
    
    srs = osr.SpatialReference()  # 创建空间参考
    srsout=spatial_ref.ExportToWkt()
    srs.ImportFromWkt(srsout) # 定义地理坐标系WGS1984
    papszLCO = []
    # 创建图层，创建一个多边形图层,"TestPolygon"->属性表名
    oLayer = oDS.CreateLayer("TestPolygon", srs, ogr.wkbMultiPolygon, papszLCO)
    if oLayer == None:
        print("图层创建失败！\n")
    
    oDefn = oLayer.GetLayerDefn()  # 定义要素
    #获取字段信息
    oSRCDefn = layer.GetLayerDefn()
    numFe=layer.GetFeatureCount()
    #创建字段
    if numFe>0:
        firstFeatur=layer.GetFeature(0)
        FieldNumber=firstFeatur.GetFieldCount()
        for itr in range(FieldNumber):
            curFiedDefn=oSRCDefn.GetFieldDefn(itr)
            fieldname=curFiedDefn.GetNameRef()
            #fiedTypeName=curFiedDefn.GetFieldTypeName(curFiedDefn.GetType())
            fieldtype=curFiedDefn.GetType()
            creatFieldN=ogr.FieldDefn(fieldname,fieldtype)
            creatFieldN.SetWidth(100)
            oLayer.CreateField(creatFieldN)
    #输出前50个点的属性
    listnow=[]
    listbefor=[]
    listFieldOut=[]
    listout=[]
    for feature_element in layer:
        #获取空间数据(获取x、y坐标)
        spatial_data=feature_element.geometry()
        fieldnum=feature_element.GetFieldCount()
        listnow.append(spatial_data.ExportToWkt())
        listonefeature=[]
        for ite in range(fieldnum):
            currenfielddefn=oSRCDefn.GetFieldDefn(ite)
            fieldname = currenfielddefn.GetNameRef()
            fiedlValue=feature_element.GetField(ite)
            listonefeature.append(fieldname)
            listonefeature.append(fiedlValue)
        listFieldOut.append(listonefeature)
    
    for feature_elementbefor in layer_before:
        spatial_databefore = feature_elementbefor.geometry()
        geobefore = spatial_databefore.ExportToWkt()
        listbefor.append(geobefore)
    #转换成shapely格式输出两个矢量面然后做裁剪工作；
    #TODO：将polygon转成multipolygon
    elementsnumber=layer.GetFeatureCount()
    elementsnumberberfore=layer_before.GetFeatureCount()
    fnm=len(listFieldOut)
    print("fnm is :",fnm)
    print("elementnumber is :",elementsnumber)
    listReserve=[]
    for i in range(elementsnumber):
        #构造shapely类型几何文件
        listinset = []
        geoi=wkt.loads(listnow[i])
        for j in range(elementsnumberberfore):
            geoj=wkt.loads(listbefor[j])
            geoinset=geoi.intersection(geoj)
            if not geoinset.is_empty:
                if geoinset.type=="Polygon":
                    if geoinset.is_valid:
                       listinset.append(geoinset.wkt)
                if geoinset.type=="MultiPolygon":
                   for g in geoinset:
                       if g.is_valid:
                          listinset.append(g.wkt)
                if geoinset.type=="GeometryCollection":
                    for g in geoinset:
                        if g.type=="Polygon":
                            if g.is_valid:
                               listinset.append(g.wkt)
                        if g.type=="MultiPolygon":
                            for tg in g:
                                if tg.is_valid:
                                   listinset.append(tg.wkt)
                # if geoinset.type=="LinearRing":
                # if geoinset.type=="MultiPoint":
                # if geoinset.type=="MultiLineString":
        numberout=len(listinset)
        if numberout==0:
            print("移除空polygon")
        elif numberout>1:
            geoi1=wkt.loads(listinset[0])
            mp1=MultiPolygon([geoi1])
            if not mp1.is_valid:
                print("多边形拓扑错误")
            for itr in range(1,numberout):
                geoi2=wkt.loads(listinset[itr])
                mp2=MultiPolygon([geoi2])
                if mp2.is_valid:
                   mp1=mp1.union(mp2)
            listout.append(mp1.wkt)
            listReserve.append(listFieldOut[i])
        else:
            pol=wkt.loads(listinset[0])
            mpol=MultiPolygon([pol])
            listout.append(mpol.wkt)
            listReserve.append(listFieldOut[i])
    #移除
    # 输出裁剪矢量
    outNum=len(listout)
    numberreserve=len(listReserve)
    if not outNum== numberreserve:
        print("拓扑错误！\n")
    for it in range(outNum):
        oFet=ogr.Feature(oDefn)
        fieldsubNumber=len(listFieldOut[it])
        for iu in range(0,fieldsubNumber,2):
            oFet.SetField(listReserve[it][iu],listReserve[it][iu+1])
        gemetrytt=ogr.CreateGeometryFromWkt(listout[it])
        oFet.SetGeometry(gemetrytt)
        oLayer.CreateFeature(oFet)
    oDS.Destroy()
    print("数据集创建完成！\n")


def VectorClipByVectorNew(strinputbase, strinputclip, stroutput):
    # fn1=r"E:\shptest\DWFL_2018.shp"
    # fn2=r"E:\shptest\DWFL_2016.shp"
    datasource = ogr.Open(strinputbase, False)
    datasourcebefor = ogr.Open(strinputclip, False)
    # 查看矢量图层的数目,shp文件只有一个图层
    layer_num = datasource.GetLayerCount()
    layer_numbefor = datasourcebefor.GetLayerCount()
    # 获取矢量图层
    layer = datasource.GetLayerByIndex(0)  # 矢量的索引从0开始，栅格的索引从1开始
    layer_before = datasourcebefor.GetLayerByIndex(0)
    # 获取空间参考
    spatial_ref = layer.GetSpatialRef()
    spatial_refBefore = layer_before.GetSpatialRef()
    # 获取每个要素的属性信息
    print("SpatialReference: ", spatial_ref)
    print("LayerCount: ", layer_num)
    print("Elements number:", layer.GetFeatureCount())
    print("SpatialReference before: ", spatial_refBefore)
    print("LayerCount before: ", layer_numbefor)
    print("Elements number before:", layer_before.GetFeatureCount())
    # 计算裁剪后的矢量
    # 写入矢量文件
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")  # 为了支持中文路径
    gdal.SetConfigOption("SHAPE_ENCODING", "CP936")  # 为了使属性表字段支持中文
    # stroutput = "E:\shptest\DWFL_2017.shp" # 定义写入路径及文件名
    ogr.RegisterAll()  # 注册所有的驱动
    strDriverName = "ESRI Shapefile"  # 创建数据，这里创建ESRI的shp文件
    oDriver = ogr.GetDriverByName(strDriverName)
    if oDriver == None:
       print("%s 驱动不可用！\n", strDriverName)
    oDS = oDriver.CreateDataSource(stroutput)  # 创建数据源
    if oDS == None:
       print("创建文件【%s】失败！", stroutput)
    srs = osr.SpatialReference()  # 创建空间参考
    srsout = spatial_ref.ExportToWkt()
    srs.ImportFromWkt(srsout)  # 定义地理坐标系WGS1984
    papszLCO = []
       # 创建图层，创建一个多边形图层,"TestPolygon"->属性表名
       # 获取字段信息
    oSRCDefn = layer.GetLayerDefn()
    numFe = layer.GetFeatureCount()
       #输入图层的图层类型
    listoutType=[]
    listOutLayer=[]
    # 创建字段
    if numFe > 0:
       firstFeatur = layer.GetFeature(0)
       FieldNumber = firstFeatur.GetFieldCount()
       firstFeGeo=firstFeatur.geometry()
       Baselayertype=firstFeGeo.GetGeometryName()
       listoutType.append(Baselayertype)
       if Baselayertype == "POLYGON" or Baselayertype == "MULTIPOLYGON":
          oLayer1= oDS.CreateLayer("TestPolygon", srs, ogr.wkbMultiPolygon, papszLCO)
          if oLayer1 == None:
              print("图层创建失败！\n")
          else:
              listOutLayer.append(oLayer1)
       elif Baselayertype == "LINESTRING" or Baselayertype == "MULTILINESTRING":
            oLayer1= oDS.CreateLayer("TestPolygon", srs, ogr.wkbMultiLineString, papszLCO)
            if oLayer1== None:
              print("图层创建失败！\n")
            else:
              listOutLayer.append(oLayer1)
       if Baselayertype == "POINT" or Baselayertype == "MULTIPOINT":
          oLayer1 = oDS.CreateLayer("TestPolygon", srs, ogr.wkbMultiPoint, papszLCO)
          if oLayer1 == None:
              print("图层创建失败！\n")
          else:
              listOutLayer.append(oLayer1)
       for itr in range(FieldNumber):
           curFiedDefn = oSRCDefn.GetFieldDefn(itr)
           fieldname = curFiedDefn.GetNameRef()
           # fiedTypeName=curFiedDefn.GetFieldTypeName(curFiedDefn.GetType())
           fieldtype = curFiedDefn.GetType()
           creatFieldN = ogr.FieldDefn(fieldname, fieldtype)
           creatFieldN.SetWidth(100)
           listOutLayer[0].CreateField(creatFieldN)
       # 输出前50个点的属性
    listnow = []
    listbefor = []
    listFieldOut = []
    listout = []
    Baselayertype=listoutType[0]
    if Baselayertype == "POLYGON" or Baselayertype == "MULTIPOLYGON":
       for feature_element in layer:
              # 获取空间数据(获取x、y坐标)
           spatial_data = feature_element.geometry()
           fieldnum = feature_element.GetFieldCount()
           listnow.append(spatial_data.ExportToWkt())
           listonefeature = []
           for ite in range(fieldnum):
               currenfielddefn = oSRCDefn.GetFieldDefn(ite)
               fieldname = currenfielddefn.GetNameRef()
               fiedlValue = feature_element.GetField(ite)
               listonefeature.append(fieldname)
               listonefeature.append(fiedlValue)
           layer_before.SetSpatialFilter(None)
           layer_before.SetSpatialFilter(spatial_data)
           shapegeomtsrs=wkt.loads(spatial_data.ExportToWkt())
           listdifferset = []
           for curfeat in layer_before:
               curgeomtry=curfeat.geometry()
               shapegeomt=wkt.loads(curgeomtry.ExportToWkt())
               geodiffer=shapegeomtsrs.intersection(shapegeomt)
               if not geodiffer.is_empty:
                    if geodiffer.type == "Polygon":
                       if geodiffer.is_valid:
                          listdifferset.append(geodiffer.wkt)
                    if geodiffer.type == "MultiPolygon":
                       for g in geodiffer:
                           if g.is_valid:
                              listdifferset.append(g.wkt)
                    if geodiffer.type == "GeometryCollection":
                       for g in geodiffer:
                           if g.type == "Polygon":
                              if g.is_valid:
                                 listdifferset.append(g.wkt)
                           if g.type == "MultiPolygon":
                              for tg in g:
                                  if tg.is_valid:
                                     listdifferset.append(tg.wkt)
           numberout = len(listdifferset)
           if numberout == 0:
              print("移除空polygon")
           elif numberout > 1:
              geoi1 = wkt.loads(listdifferset[0])
              mp1 = MultiPolygon([geoi1])
              if not mp1.is_valid:
                 print("多边形拓扑错误")
              for itr in range(1, numberout):
                  geoi2 = wkt.loads(listdifferset[itr])
                  mp2 = MultiPolygon([geoi2])
                  if mp2.is_valid:
                     mp1 = mp1.union(mp2)
                  listout.append(mp1.wkt)
                  listFieldOut.append(listonefeature)
           else:
                pol = wkt.loads(listdifferset[0])
                mpol = MultiPolygon([pol])
                listout.append(mpol.wkt)
                listFieldOut.append(listonefeature)
    elif Baselayertype == "LINESTRING" or Baselayertype == "MULTILINESTRING":
         for feature_element in layer:
            # 获取空间数据(获取x、y坐标)
            spatial_data = feature_element.geometry()
            fieldnum = feature_element.GetFieldCount()
            listnow.append(spatial_data.ExportToWkt())
            listonefeature = []
            for ite in range(fieldnum):
                currenfielddefn = oSRCDefn.GetFieldDefn(ite)
                fieldname = currenfielddefn.GetNameRef()
                fiedlValue = feature_element.GetField(ite)
                listonefeature.append(fieldname)
                listonefeature.append(fiedlValue)
            layer_before.SetSpatialFilter(None)
            layer_before.SetSpatialFilter(spatial_data)
            shapegeomtsrs=wkt.loads(spatial_data.ExportToWkt())
            listdifferset=[]
            for curfeat in layer_before:
                curgeomtry=curfeat.geometry()
                shapegeomt=wkt.loads(curgeomtry.ExportToWkt())
                geodiffer=shapegeomtsrs.intersection(shapegeomt)
                if not geodiffer.is_empty:
                    if geodiffer.type == "LineString":
                        if geodiffer.is_valid:
                            listdifferset.append(geodiffer.wkt)
                    if geodiffer.type == "MultiLineString":
                        for g in geodiffer:
                            if g.is_valid:
                               listdifferset.append(g.wkt)
                    if geodiffer.type == "GeometryCollection":
                       for g in geodiffer:
                           if g.type == "LineString":
                               if g.is_valid:
                                  listdifferset.append(g.wkt)
                           if g.type == "MultiLineString":
                              for tg in g:
                                  if tg.is_valid:
                                     listdifferset.append(tg.wkt)
            numberout = len(listdifferset)
            if numberout == 0:
                print("移除空polygon")
            elif numberout > 1:
                geoi1 = wkt.loads(listdifferset[0])
                mp1 = MultiLineString([geoi1])
                if not mp1.is_valid:
                    print("多边形拓扑错误")
                for itr in range(1, numberout):
                    geoi2 = wkt.loads(listdifferset[itr])
                    mp2 = MultiLineString([geoi2])
                    if mp2.is_valid:
                        mp1 = mp1.union(mp2)
                listout.append(mp1.wkt)
                listFieldOut.append(listonefeature)
            else:
                pol = wkt.loads(listdifferset[0])
                mpol = MultiLineString([pol])
                listout.append(mpol.wkt)
                listFieldOut.append(listonefeature)
    elif Baselayertype == "POINT" or Baselayertype == "MULTIPOINT":
         for feature_element in layer:
             # 获取空间数据(获取x、y坐标)

             spatial_data = feature_element.geometry()
             fieldnum = feature_element.GetFieldCount()
             listnow.append(spatial_data.ExportToWkt())
             listonefeature = []
             for ite in range(fieldnum):
                 currenfielddefn = oSRCDefn.GetFieldDefn(ite)
                 fieldname = currenfielddefn.GetNameRef()
                 fiedlValue = feature_element.GetField(ite)
                 listonefeature.append(fieldname)
                 listonefeature.append(fiedlValue)
             layer_before.SetSpatialFilter(None)
             layer_before.SetSpatialFilter(spatial_data)
             shapegeomtsrs=wkt.loads(spatial_data.ExportToWkt())
             listdifferset = []
             for curfeat in layer_before:
                 curgeomtry=curfeat.geometry()
                 shapegeomt=wkt.loads(curgeomtry.ExportToWkt())
                 geodiffer=shapegeomtsrs.intersection(shapegeomt)
                 if not geodiffer.is_empty:
                     if geodiffer.type == "Point":
                         if geodiffer.is_valid:
                             listdifferset.append(geodiffer.wkt)
                     if geodiffer.type == "MultiPoint":
                         for g in geodiffer:
                             if g.is_valid:
                                 listdifferset.append(g.wkt)
                     if geodiffer.type == "GeometryCollection":
                         for g in geodiffer:
                             if g.type == "Point":
                                 if g.is_valid:
                                    listdifferset.append(g.wkt)
                             if g.type == "MultiPoint":
                                 for tg in g:
                                     if tg.is_valid:
                                         listdifferset.append(tg.wkt)

             numberout = len(listdifferset)
             if numberout == 0:
               print("移除空polygon")
             elif numberout > 1:
                  geoi1 = wkt.loads(listdifferset[0])
                  mp1 = MultiPolygon([geoi1])
                  if not mp1.is_valid:
                     print("多边形拓扑错误")
                  for itr in range(1, numberout):
                      geoi2 = wkt.loads(listdifferset[itr])
                      mp2 = MultiPolygon([geoi2])
                      if mp2.is_valid:
                         mp1 = mp1.union(mp2)
                  listout.append(mp1.wkt)
                  listFieldOut.append(listonefeature)
             else:
                 pol = wkt.loads(listdifferset[0])
                 mpol = MultiPolygon([pol])
                 listout.append(mpol.wkt)
                 listFieldOut.append(listonefeature)
    # 移除
    # 输出裁剪矢量
    outNum = len(listout)
    numberreserve = len(listFieldOut)
    oLayer=listOutLayer[0]
    oDefn = oLayer.GetLayerDefn()
    if not outNum == numberreserve:
        print("Topo is Wrong！\n")
    for it in range(outNum):
        oFet = ogr.Feature(oDefn)
        fieldsubNumber = len(listFieldOut[it])
        for iu in range(0, fieldsubNumber, 2):
            oFet.SetField(listFieldOut[it][iu], listFieldOut[it][iu + 1])
        gemetrytt = ogr.CreateGeometryFromWkt(listout[it])
        oFet.SetGeometry(gemetrytt)
        oLayer.CreateFeature(oFet)
    oDS.Destroy()
    print("数据集创建完成！\n")
#VectorClipByVectorNew("E:\shptest\DWFL_2018.shp","E:\shptest\DWFL_2016.shp","E:\shptest\DWFL_2021newtt.shp")
def VectorInterSect(strinputbase, strinputclip, stroutput):
    # fn1=r"E:\shptest\DWFL_2018.shp"
    # fn2=r"E:\shptest\DWFL_2016.shp"
    datasource = ogr.Open(strinputbase, False)
    datasourcebefor = ogr.Open(strinputclip, False)
    # 查看矢量图层的数目,shp文件只有一个图层
    layer_num = datasource.GetLayerCount()
    layer_numbefor = datasourcebefor.GetLayerCount()
    # 获取矢量图层
    layer = datasource.GetLayerByIndex(0)  # 矢量的索引从0开始，栅格的索引从1开始
    layer_before = datasourcebefor.GetLayerByIndex(0)
    # 获取空间参考
    spatial_ref = layer.GetSpatialRef()
    spatial_refBefore = layer_before.GetSpatialRef()
    # 获取每个要素的属性信息
    print("SpatialReference: ", spatial_ref)
    print("LayerCount: ", layer_num)
    print("Elements number:", layer.GetFeatureCount())
    print("SpatialReference before: ", spatial_refBefore)
    print("LayerCount before: ", layer_numbefor)
    print("Elements number before:", layer_before.GetFeatureCount())
    # 计算裁剪后的矢量
    # 写入矢量文件
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")  # 为了支持中文路径
    gdal.SetConfigOption("SHAPE_ENCODING", "CP936")  # 为了使属性表字段支持中文
    # stroutput = "E:\shptest\DWFL_2017.shp" # 定义写入路径及文件名
    ogr.RegisterAll()  # 注册所有的驱动
    strDriverName = "ESRI Shapefile"  # 创建数据，这里创建ESRI的shp文件
    oDriver = ogr.GetDriverByName(strDriverName)
    if oDriver == None:
        print("%s 驱动不可用！\n", strDriverName)
    oDS = oDriver.CreateDataSource(stroutput)  # 创建数据源
    if oDS == None:
        print("创建文件【%s】失败！", stroutput)
    srs = osr.SpatialReference()  # 创建空间参考
    srsout = spatial_ref.ExportToWkt()
    srs.ImportFromWkt(srsout)  # 定义地理坐标系WGS1984
    papszLCO = []
    # 创建图层，创建一个多边形图层,"TestPolygon"->属性表名
    # 获取字段信息
    oSRCDefn = layer.GetLayerDefn()
    numFe = layer.GetFeatureCount()
    oSRCDefnBefor=layer_before.GetLayerDefn()
    numFeBefor=layer_before.GetFeatureCount()
    # 输入图层的图层类型
    listoutType = []
    listOutLayer = []
    # 创建字段
    if numFe > 0:
        firstFeatur = layer.GetFeature(0)
        FieldNumber = firstFeatur.GetFieldCount()
        firstFeGeo = firstFeatur.geometry()
        Baselayertype = firstFeGeo.GetGeometryName()
        listoutType.append(Baselayertype)
        if Baselayertype == "POLYGON" or Baselayertype == "MULTIPOLYGON":
            oLayer1 = oDS.CreateLayer("TestPolygon", srs, ogr.wkbMultiPolygon, papszLCO)
            if oLayer1 == None:
                print("图层创建失败！\n")
            else:
                listOutLayer.append(oLayer1)
        elif Baselayertype == "LINESTRING" or Baselayertype == "MULTILINESTRING":
            oLayer1 = oDS.CreateLayer("TestPolygon", srs, ogr.wkbMultiLineString, papszLCO)
            if oLayer1 == None:
                print("图层创建失败！\n")
            else:
                listOutLayer.append(oLayer1)
        if Baselayertype == "POINT" or Baselayertype == "MULTIPOINT":
            oLayer1 = oDS.CreateLayer("TestPolygon", srs, ogr.wkbMultiPoint, papszLCO)
            if oLayer1 == None:
                print("图层创建失败！\n")
            else:
                listOutLayer.append(oLayer1)
        for itr in range(FieldNumber):
            curFiedDefn = oSRCDefn.GetFieldDefn(itr)
            fieldname = curFiedDefn.GetNameRef()
            # fiedTypeName=curFiedDefn.GetFieldTypeName(curFiedDefn.GetType())
            fieldtype = curFiedDefn.GetType()
            creatFieldN = ogr.FieldDefn(fieldname, fieldtype)
            creatFieldN.SetWidth(100)
            listOutLayer[0].CreateField(creatFieldN)
    if numFeBefor >0:
        firstFeatur=layer_before.GetFeature(0)
        FieldNumber=firstFeatur.GetFieldCount()
        for itr in range(FieldNumber):
            curFiedDefn=oSRCDefnBefor.GetFieldDefn(itr)
            fieldname="1_"+curFiedDefn.GetNameRef()
            fieldtype=curFiedDefn.GetType()
            creatFieldN=ogr.FieldDefn(fieldname,fieldtype)
            creatFieldN.SetWidth(100)
            listOutLayer[0].CreateField(creatFieldN)

    # 输出前50个点的属性
    listnow = []
    listbefor = []
    listFieldOut = []
    listout = []
    Baselayertype = listoutType[0]
    if Baselayertype == "POLYGON" or Baselayertype == "MULTIPOLYGON":
        for feature_element in layer:
            # 获取空间数据(获取x、y坐标)
            spatial_data = feature_element.geometry()
            fieldnum = feature_element.GetFieldCount()
            listonefeature = []
            for ite in range(fieldnum):
                currenfielddefn = oSRCDefn.GetFieldDefn(ite)
                fieldname = currenfielddefn.GetNameRef()
                fiedlValue = feature_element.GetField(ite)
                listonefeature.append(fieldname)
                listonefeature.append(fiedlValue)
            layer_before.SetSpatialFilter(None)
            layer_before.SetSpatialFilter(spatial_data)
            shapegeomtsrs = wkt.loads(spatial_data.ExportToWkt())
            for curfeat in layer_before:
                listtwofeature=[]
                curgeomtry = curfeat.geometry()
                shapegeomt = wkt.loads(curgeomtry.ExportToWkt())
                geodiffer = shapegeomtsrs.intersection(shapegeomt)
                if not geodiffer.is_empty:
                    fielNumcure=curfeat.GetFieldCount()
                    for ite in range(fielNumcure):
                        currenfielddefn = oSRCDefnBefor.GetFieldDefn(ite)
                        fieldname = "1_"+currenfielddefn.GetNameRef()
                        fiedlValue = feature_element.GetField(ite)
                        listtwofeature.append(fieldname)
                        listtwofeature.append(fiedlValue)
                    if geodiffer.type == "Polygon":
                        if geodiffer.is_valid:
                           listout.append(geodiffer.wkt)
                           listFieldOut.append(listonefeature+listtwofeature)
                    if geodiffer.type == "MultiPolygon":
                        for g in geodiffer:
                            if g.is_valid:
                                listout.append(g.wkt)
                                listFieldOut.append(listonefeature + listtwofeature)
                    if geodiffer.type == "GeometryCollection":
                        for g in geodiffer:
                            if g.type == "Polygon":
                                if g.is_valid:
                                    listout.append(g.wkt)
                                    listFieldOut.append(listonefeature + listtwofeature)
                            if g.type == "MultiPolygon":
                                for tg in g:
                                    if tg.is_valid:
                                        listout.append(tg.wkt)
                                        listFieldOut.append(listonefeature + listtwofeature)
    elif Baselayertype == "LINESTRING" or Baselayertype == "MULTILINESTRING":
        for feature_element in layer:
            # 获取空间数据(获取x、y坐标)
            spatial_data = feature_element.geometry()
            fieldnum = feature_element.GetFieldCount()
            listonefeature = []
            for ite in range(fieldnum):
                currenfielddefn = oSRCDefn.GetFieldDefn(ite)
                fieldname = currenfielddefn.GetNameRef()
                fiedlValue = feature_element.GetField(ite)
                listonefeature.append(fieldname)
                listonefeature.append(fiedlValue)
            layer_before.SetSpatialFilter(None)
            layer_before.SetSpatialFilter(spatial_data)
            shapegeomtsrs = wkt.loads(spatial_data.ExportToWkt())
            for curfeat in layer_before:
                listtwofeature = []
                curgeomtry = curfeat.geometry()
                shapegeomt = wkt.loads(curgeomtry.ExportToWkt())
                geodiffer = shapegeomtsrs.intersection(shapegeomt)
                if not geodiffer.is_empty:
                    fielNumcure = curfeat.GetFieldCount()
                    for ite in range(fielNumcure):
                        currenfielddefn = oSRCDefnBefor.GetFieldDefn(ite)
                        fieldname = "1_" + currenfielddefn.GetNameRef()
                        fiedlValue = feature_element.GetField(ite)
                        listtwofeature.append(fieldname)
                        listtwofeature.append(fiedlValue)
                    if geodiffer.type == "LineString":
                        if geodiffer.is_valid:
                            listout.append(geodiffer.wkt)
                            listFieldOut.append(listonefeature + listtwofeature)
                    if geodiffer.type == "MultiLineString":
                        for g in geodiffer:
                            if g.is_valid:
                                listout.append(g.wkt)
                                listFieldOut.append(listonefeature + listtwofeature)
                    if geodiffer.type == "GeometryCollection":
                        for g in geodiffer:
                            if g.type == "LineString":
                                if g.is_valid:
                                    listout.append(g.wkt)
                                    listFieldOut.append(listonefeature + listtwofeature)
                            if g.type == "MultiLineString":
                                for tg in g:
                                    if tg.is_valid:
                                        listout.append(tg.wkt)
                                        listFieldOut.append(listonefeature + listtwofeature)
    elif Baselayertype == "POINT" or Baselayertype == "MULTIPOINT":
        for feature_element in layer:
            # 获取空间数据(获取x、y坐标)
            spatial_data = feature_element.geometry()
            fieldnum = feature_element.GetFieldCount()
            listonefeature = []
            for ite in range(fieldnum):
                currenfielddefn = oSRCDefn.GetFieldDefn(ite)
                fieldname = currenfielddefn.GetNameRef()
                fiedlValue = feature_element.GetField(ite)
                listonefeature.append(fieldname)
                listonefeature.append(fiedlValue)
            layer_before.SetSpatialFilter(None)
            layer_before.SetSpatialFilter(spatial_data)
            shapegeomtsrs = wkt.loads(spatial_data.ExportToWkt())
            for curfeat in layer_before:
                listtwofeature = []
                curgeomtry = curfeat.geometry()
                shapegeomt = wkt.loads(curgeomtry.ExportToWkt())
                geodiffer = shapegeomtsrs.intersection(shapegeomt)
                if not geodiffer.is_empty:
                    fielNumcure = curfeat.GetFieldCount()
                    for ite in range(fielNumcure):
                        currenfielddefn = oSRCDefnBefor.GetFieldDefn(ite)
                        fieldname = "1_" + currenfielddefn.GetNameRef()
                        fiedlValue = feature_element.GetField(ite)
                        listtwofeature.append(fieldname)
                        listtwofeature.append(fiedlValue)
                    if geodiffer.type == "Point":
                        if geodiffer.is_valid:
                            listout.append(geodiffer.wkt)
                            listFieldOut.append(listonefeature + listtwofeature)
                    if geodiffer.type == "MultiPoint":
                        for g in geodiffer:
                            if g.is_valid:
                                listout.append(g.wkt)
                                listFieldOut.append(listonefeature + listtwofeature)
                    if geodiffer.type == "GeometryCollection":
                        for g in geodiffer:
                            if g.type == "Point":
                                if g.is_valid:
                                    listout.append(g.wkt)
                                    listFieldOut.append(listonefeature + listtwofeature)
                            if g.type == "MultiPoint":
                                for tg in g:
                                    if tg.is_valid:
                                        listout.append(tg.wkt)
                                        listFieldOut.append(listonefeature + listtwofeature)
    # 移除
    # 输出裁剪矢量
    outNum = len(listout)
    numberreserve = len(listFieldOut)
    oLayer = listOutLayer[0]
    oDefn = oLayer.GetLayerDefn()
    if not outNum == numberreserve:
        print("Topo is Wrong！\n")
    for it in range(outNum):
        oFet = ogr.Feature(oDefn)
        fieldsubNumber = len(listFieldOut[it])
        for iu in range(0, fieldsubNumber, 2):
            oFet.SetField(listFieldOut[it][iu], listFieldOut[it][iu + 1])
        gemetrytt = ogr.CreateGeometryFromWkt(listout[it])
        oFet.SetGeometry(gemetrytt)
        oLayer.CreateFeature(oFet)
    oDS.Destroy()
    print("数据集创建完成！\n")
VectorInterSect("E:\shptest\DWFL_2018.shp","E:\shptest\DWFL_2016.shp","E:\shptest\DWFL_2021noooew.shp")
def VectorDifferByVector(strinputbase, strinputclip, stroutput):
    # fn1=r"E:\shptest\DWFL_2018.shp"
    # fn2=r"E:\shptest\DWFL_2016.shp"
    datasource = ogr.Open(strinputbase, False)
    datasourcebefor = ogr.Open(strinputclip, False)
    # 查看矢量图层的数目,shp文件只有一个图层
    layer_num = datasource.GetLayerCount()
    layer_numbefor = datasourcebefor.GetLayerCount()
    # 获取矢量图层
    layer = datasource.GetLayerByIndex(0)  # 矢量的索引从0开始，栅格的索引从1开始
    layer_before = datasourcebefor.GetLayerByIndex(0)
    # 获取空间参考
    spatial_ref = layer.GetSpatialRef()
    spatial_refBefore = layer_before.GetSpatialRef()
    # 获取每个要素的属性信息
    print("SpatialReference: ", spatial_ref)
    print("LayerCount: ", layer_num)
    print("Elements number:", layer.GetFeatureCount())
    print("SpatialReference before: ", spatial_refBefore)
    print("LayerCount before: ", layer_numbefor)
    print("Elements number before:", layer_before.GetFeatureCount())
    # 计算裁剪后的矢量
    # 写入矢量文件
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")  # 为了支持中文路径
    gdal.SetConfigOption("SHAPE_ENCODING", "CP936")  # 为了使属性表字段支持中文
    # stroutput = "E:\shptest\DWFL_2017.shp" # 定义写入路径及文件名
    ogr.RegisterAll()  # 注册所有的驱动
    strDriverName = "ESRI Shapefile"  # 创建数据，这里创建ESRI的shp文件
    oDriver = ogr.GetDriverByName(strDriverName)
    if oDriver == None:
       print("%s 驱动不可用！\n", strDriverName)
    oDS = oDriver.CreateDataSource(stroutput)  # 创建数据源
    if oDS == None:
       print("创建文件【%s】失败！", stroutput)
    srs = osr.SpatialReference()  # 创建空间参考
    srsout = spatial_ref.ExportToWkt()
    srs.ImportFromWkt(srsout)  # 定义地理坐标系WGS1984
    papszLCO = []
    # 创建图层，创建一个多边形图层,"TestPolygon"->属性表名
    # 获取字段信息
    oSRCDefn = layer.GetLayerDefn()
    numFe = layer.GetFeatureCount()
    #输入图层的图层类型
    listoutType=[]
    listOutLayer=[]
    # 创建字段
    if numFe > 0:
        firstFeatur = layer.GetFeature(0)
        FieldNumber = firstFeatur.GetFieldCount()
        firstFeGeo=firstFeatur.geometry()
        Baselayertype=firstFeGeo.GetGeometryName()
        listoutType.append(Baselayertype)
        if Baselayertype == "POLYGON" or Baselayertype == "MULTIPOLYGON":
           oLayer1= oDS.CreateLayer("TestPolygon", srs, ogr.wkbMultiPolygon, papszLCO)
           if oLayer1 == None:
               print("图层创建失败！\n")
           else:
               listOutLayer.append(oLayer1)
        elif Baselayertype == "LINESTRING" or Baselayertype == "MULTILINESTRING":
           oLayer1= oDS.CreateLayer("TestPolygon", srs, ogr.wkbMultiLineString, papszLCO)
           if oLayer1== None:
               print("图层创建失败！\n")
           else:
               listOutLayer.append(oLayer1)
        if Baselayertype == "POINT" or Baselayertype == "MULTIPOINT":
           oLayer1 = oDS.CreateLayer("TestPolygon", srs, ogr.wkbMultiPoint, papszLCO)
           if oLayer1 == None:
               print("图层创建失败！\n")
           else:
               listOutLayer.append(oLayer1)
        for itr in range(FieldNumber):
            curFiedDefn = oSRCDefn.GetFieldDefn(itr)
            fieldname = curFiedDefn.GetNameRef()
            # fiedTypeName=curFiedDefn.GetFieldTypeName(curFiedDefn.GetType())
            fieldtype = curFiedDefn.GetType()
            creatFieldN = ogr.FieldDefn(fieldname, fieldtype)
            creatFieldN.SetWidth(100)
            listOutLayer[0].CreateField(creatFieldN)
    # 输出前50个点的属性
    listnow = []
    listbefor = []
    listFieldOut = []
    listout = []
    Baselayertype=listoutType[0]
    if Baselayertype == "POLYGON" or Baselayertype == "MULTIPOLYGON":
        for feature_element in layer:
            # 获取空间数据(获取x、y坐标)

            spatial_data = feature_element.geometry()
            fieldnum = feature_element.GetFieldCount()
            listnow.append(spatial_data.ExportToWkt())
            listonefeature = []
            for ite in range(fieldnum):
                currenfielddefn = oSRCDefn.GetFieldDefn(ite)
                fieldname = currenfielddefn.GetNameRef()
                fiedlValue = feature_element.GetField(ite)
                listonefeature.append(fieldname)
                listonefeature.append(fiedlValue)
            layer_before.SetSpatialFilter(None)
            layer_before.SetSpatialFilter(spatial_data)
            shapegeomtsrs=wkt.loads(spatial_data.ExportToWkt())
            listdifferset = []
            for curfeat in layer_before:
                curgeomtry=curfeat.geometry()
                shapegeomt=wkt.loads(curgeomtry.ExportToWkt())
                geodiffer=shapegeomtsrs.difference(shapegeomt)
                if not geodiffer.is_empty:
                    if geodiffer.type == "Polygon":
                        if geodiffer.is_valid:
                            listdifferset.append(geodiffer.wkt)
                    if geodiffer.type == "MultiPolygon":
                        for g in geodiffer:
                            if g.is_valid:
                                listdifferset.append(g.wkt)
                    if geodiffer.type == "GeometryCollection":
                        for g in geodiffer:
                            if g.type == "Polygon":
                                if g.is_valid:
                                   listdifferset.append(g.wkt)
                            if g.type == "MultiPolygon":
                                for tg in g:
                                    if tg.is_valid:
                                        listdifferset.append(tg.wkt)
            numberout = len(listdifferset)
            if numberout == 0:
                print("移除空polygon")
            elif numberout > 1:
                geoi1 = wkt.loads(listdifferset[0])
                mp1 = MultiPolygon([geoi1])
                if not mp1.is_valid:
                    print("多边形拓扑错误")
                for itr in range(1, numberout):
                    geoi2 = wkt.loads(listdifferset[itr])
                    mp2 = MultiPolygon([geoi2])
                    if mp2.is_valid:
                        mp1 = mp1.union(mp2)
                listout.append(mp1.wkt)
                listFieldOut.append(listonefeature)
            else:
                pol = wkt.loads(listdifferset[0])
                mpol = MultiPolygon([pol])
                listout.append(mpol.wkt)
                listFieldOut.append(listonefeature)
    elif Baselayertype == "LINESTRING" or Baselayertype == "MULTILINESTRING":
         for feature_element in layer:
             # 获取空间数据(获取x、y坐标)
             spatial_data = feature_element.geometry()
             fieldnum = feature_element.GetFieldCount()
             listnow.append(spatial_data.ExportToWkt())
             listonefeature = []
             for ite in range(fieldnum):
                 currenfielddefn = oSRCDefn.GetFieldDefn(ite)
                 fieldname = currenfielddefn.GetNameRef()
                 fiedlValue = feature_element.GetField(ite)
                 listonefeature.append(fieldname)
                 listonefeature.append(fiedlValue)
             layer_before.SetSpatialFilter(None)
             layer_before.SetSpatialFilter(spatial_data)
             shapegeomtsrs=wkt.loads(spatial_data.ExportToWkt())
             listdifferset=[]
             for curfeat in layer_before:
                 curgeomtry=curfeat.geometry()
                 shapegeomt=wkt.loads(curgeomtry.ExportToWkt())
                 geodiffer=shapegeomtsrs.difference(shapegeomt)
                 if not geodiffer.is_empty:
                     if geodiffer.type == "LineString":
                         if geodiffer.is_valid:
                             listdifferset.append(geodiffer.wkt)
                     if geodiffer.type == "MultiLineString":
                         for g in geodiffer:
                             if g.is_valid:
                                listdifferset.append(g.wkt)
                     if geodiffer.type == "GeometryCollection":
                        for g in geodiffer:
                            if g.type == "LineString":
                                if g.is_valid:
                                   listdifferset.append(g.wkt)
                            if g.type == "MultiLineString":
                               for tg in g:
                                   if tg.is_valid:
                                      listdifferset.append(tg.wkt)
             numberout = len(listdifferset)
             if numberout == 0:
                 print("移除空polygon")
             elif numberout > 1:
                 geoi1 = wkt.loads(listdifferset[0])
                 mp1 = MultiLineString([geoi1])
                 if not mp1.is_valid:
                     print("多边形拓扑错误")
                 for itr in range(1, numberout):
                     geoi2 = wkt.loads(listdifferset[itr])
                     mp2 = MultiLineString([geoi2])
                     if mp2.is_valid:
                         mp1 = mp1.union(mp2)
                 listout.append(mp1.wkt)
                 listFieldOut.append(listonefeature)
             else:
                 pol = wkt.loads(listdifferset[0])
                 mpol = MultiLineString([pol])
                 listout.append(mpol.wkt)
                 listFieldOut.append(listonefeature)
    elif Baselayertype == "POINT" or Baselayertype == "MULTIPOINT":
          for feature_element in layer:
              # 获取空间数据(获取x、y坐标)

              spatial_data = feature_element.geometry()
              fieldnum = feature_element.GetFieldCount()
              listnow.append(spatial_data.ExportToWkt())
              listonefeature = []
              for ite in range(fieldnum):
                  currenfielddefn = oSRCDefn.GetFieldDefn(ite)
                  fieldname = currenfielddefn.GetNameRef()
                  fiedlValue = feature_element.GetField(ite)
                  listonefeature.append(fieldname)
                  listonefeature.append(fiedlValue)
              layer_before.SetSpatialFilter(None)
              layer_before.SetSpatialFilter(spatial_data)
              shapegeomtsrs=wkt.loads(spatial_data.ExportToWkt())
              listdifferset = []
              for curfeat in layer_before:
                  curgeomtry=curfeat.geometry()
                  shapegeomt=wkt.loads(curgeomtry.ExportToWkt())
                  geodiffer=shapegeomtsrs.difference(shapegeomt)
                  if not geodiffer.is_empty:
                      if geodiffer.type == "Point":
                          if geodiffer.is_valid:
                              listdifferset.append(geodiffer.wkt)
                      if geodiffer.type == "MultiPoint":
                          for g in geodiffer:
                              if g.is_valid:
                                  listdifferset.append(g.wkt)
                      if geodiffer.type == "GeometryCollection":
                          for g in geodiffer:
                              if g.type == "Point":
                                  if g.is_valid:
                                     listdifferset.append(g.wkt)
                              if g.type == "MultiPoint":
                                  for tg in g:
                                      if tg.is_valid:
                                          listdifferset.append(tg.wkt)

              numberout = len(listdifferset)
              if numberout == 0:
                print("移除空polygon")
              elif numberout > 1:
                   geoi1 = wkt.loads(listdifferset[0])
                   mp1 = MultiPolygon([geoi1])                     
                   if not mp1.is_valid:
                      print("多边形拓扑错误")
                   for itr in range(1, numberout):
                       geoi2 = wkt.loads(listdifferset[itr])
                       mp2 = MultiPolygon([geoi2])
                       if mp2.is_valid:
                          mp1 = mp1.union(mp2)
                   listout.append(mp1.wkt)
                   listFieldOut.append(listonefeature)
              else:
                  pol = wkt.loads(listdifferset[0])
                  mpol = MultiPolygon([pol])
                  listout.append(mpol.wkt)
                  listFieldOut.append(listonefeature)
    # 移除
    # 输出裁剪矢量
    outNum = len(listout)
    numberreserve = len(listFieldOut)
    oLayer=listOutLayer[0]
    oDefn = oLayer.GetLayerDefn()
    if not outNum == numberreserve:
        print("Topo is Wrong！\n")
    for it in range(outNum):
        oFet = ogr.Feature(oDefn)
        fieldsubNumber = len(listFieldOut[it])
        for iu in range(0, fieldsubNumber, 2):
            oFet.SetField(listFieldOut[it][iu], listFieldOut[it][iu + 1])
        gemetrytt = ogr.CreateGeometryFromWkt(listout[it])
        oFet.SetGeometry(gemetrytt)
        oLayer.CreateFeature(oFet)
    oDS.Destroy()
    print("数据集创建完成！\n")
#VectorDifferByVector("E:\shptest\DWFL_2018.shp","E:\shptest\DWFL_2016.shp","E:\shptest\DWFL_2021difff.shp")
#VectorClipByVectorNew("E:\shptest\DWFL_2018.shp","E:\shptest\DWFL_2016.shp","E:\shptest\DWFL_2021inter.shp")
