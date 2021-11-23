from osgeo import gdal,osr,ogr
from shapely import geometry
from shapely.geometry import MultiPolygon
from shapely.geometry import Polygon
from shapely import wkt
#打开文件
fn1=r"E:\shptest\DWFL_2018.shp"
fn2=r"E:\shptest\DWFL_2016.shp"
datasource=ogr.Open(fn1,False)
datasourcebefor=ogr.Open(fn2,False)
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
strVectorFile = "E:\shptest\DWFL_2017.shp" # 定义写入路径及文件名
ogr.RegisterAll()  # 注册所有的驱动
strDriverName = "ESRI Shapefile"  # 创建数据，这里创建ESRI的shp文件
oDriver = ogr.GetDriverByName(strDriverName)
if oDriver == None:
    print("%s 驱动不可用！\n", strDriverName)

oDS = oDriver.CreateDataSource(strVectorFile)  # 创建数据源
if oDS == None:
    print("创建文件【%s】失败！", strVectorFile)

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
        geotype=geoinset.type

        if not geoinset.is_empty:
            if geoinset.type=="Polygon":
                if geoinset.is_valid:
                   listinset.append(geoinset.wkt)
            if geoinset.type=="MultiPolygon":
               for g in geoinset:
                   if g.is_valid:
                      listinset.append(g.wkt)
               print("mul")
            if geoinset.type=="GeometryCollection":
                for g in geoinset:
                    if g.type=="Polygon":
                        if g.is_valid:
                           listinset.append(g.wkt)
                    if g.type=="MultiPolygon":
                        for tg in g:
                            if tg.is_valid:
                               listinset.append(tg.wkt)


                print("geocll")
            if geoinset.type=="LinearRing":
                print("linestring")
            if geoinset.type=="MultiPoint":
                print("multipoint")
            if geoinset.type=="MultiLineString":
                print("multinglinestrng")

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





# from osgeo import ogr
#
#
# fn = r"E:\\1_SHP\\国界线.shp"
# ds = ogr.Open(fn, 0)
# if ds is None:
#     sys.exit('Could not open {0}.'.format(fn))
#
# '''索引获取数据源中的图层方式'''
# lyr = ds.GetLayer(0)
# print(lyr.GetName())
#
# i = 0
# for fea in lyr:
#     pt = fea.geometry()
#
#     x = pt.GetX()
#     y = pt.GetY()
#     '''字段名称 获取属性值'''
#     code = fea.GetField('GBCODE')
#     '''对象方式获取属性值'''
#     length = fea.LENGTH
#     '''对象方式获取属性值2'''
#     lpoly_ = fea['LPOLY_']
#     '''索引方式获取属性值'''
#     fnode_ = fea.GetField(0)
#     '''获取特定类型的属性值'''
#     str_len = fea.GetFieldAsString('LENGTH')
#     print(code, length, fnode_, lpoly_, str_len, x, y)
#     i += 1
#     if i == 20:
#         break
#
# '''名称获取数据源中的图层'''
# lyr2 = ds.GetLayer('国家')
# print(lyr2.GetName())







