from osgeo import gdal,osr,ogr
import shapely
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
#输出前50个点的属性
list=[]
listbefor=[]
listout=[]
for feature_element in layer:
    #获取空间数据(获取x、y坐标)
    spatial_data=feature_element.geometry()
    gemwkt=spatial_data.ExportToWkt()
    #print(gemwkt)
    list.append(gemwkt)
for feature_elementbefor in layer_before:
    spatial_data=feature_elementbefor.geometry()
    genwkt=spatial_data.ExportToWkt()
    listbefor.append(genwkt)

#转换成shapely格式输出两个矢量面然后做裁剪工作；
elementsnumber=layer.GetFeatureCount()
elementsnumberberfore=layer_before.GetFeatureCount()
for i in range(elementsnumber):
    #构造shapely类型几何文件
    geoi=wkt.loads(list[i])
    for j in range(elementsnumberberfore):
        geoj=wkt.loads(listbefor[j])
        geoinset=geoi.intersection(geoj)
        #geodiffer=geoi.difference(geoj)
        listout.append(geoinset.wkt)
        #listout.append(geodiffer.wkt)
        # if geoinset!=None
        #     listout.append(geoinset.wkt)
        # if geodiffer!=None
        #     listout.append(geodiffer.wkt)
# geo1=wkt.loads(list[0])
# geo2=wkt.loads(list[1])
# geoin=geo1.intersection(geo2)
# geodiff=geo1.difference(geo2)
# geounion=geo1.union(geo2)
# print(geoin)
# print(geodiff)
# print(geounion)
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
oLayer = oDS.CreateLayer("TestPolygon", srs, ogr.wkbPolygon, papszLCO)
if oLayer == None:
    print("图层创建失败！\n")

oDefn = oLayer.GetLayerDefn()  # 定义要素

# # 创建单个面
# outwkt1=geoin.wkt
# outwkt2=geodiff.wkt
# print("ceshi",outwkt1)
# oFeatureTriangle = ogr.Feature(oDefn)
# oFeatureTTriangle=ogr.Feature(oDefn)
# geometrout1=ogr.CreateGeometryFromWkt(outwkt1)
# geometrout2=ogr.CreateGeometryFromWkt(outwkt2)
# oFeatureTriangle.SetGeometry(geometrout1)
# oFeatureTTriangle.SetGeometry(geometrout2)
# oLayer.CreateFeature(oFeatureTriangle)
# oLayer.CreateFeature(oFeatureTTriangle)
# 输出裁剪矢量
outNum=len(listout)
for it in range(outNum):
    oFet=ogr.Feature(oDefn)
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







