from osgeo import gdal,osr,ogr
from osgeo.gdalconst import GA_Update
inputfile=r"E:\2123\HS_H08_20190227_0000_B01_FLDK_R10.tiff"
outtif=r"E:\2123\HS_H08_20190227_0000_B0u_FLDK_R10warp.tiff"
memDs = gdal.Open(inputfile,GA_Update)
cols = memDs.RasterXSize
rows = memDs.RasterYSize
if rows == 11000 and cols == 11000:
    res = 0.01
else:
    res = 0.02
# 几何校正
# 定义空间参考
srs = osr.SpatialReference()
# 定义地球长半轴a=6378137.0m，地球短半轴b=6356752.3m，卫星星下点所在经度140.7，目标空间参考
srs.ImportFromProj4('+proj=geos +h=35785863 +a=6378137.0 +b=6356752.3 +lon_0=140.7 +no_defs')
memDs.SetProjection(srs.ExportToWkt())
memDs.SetGeoTransform([-cols*res*50000, int(res*100000), 0, cols*res*50000, 0, int(-res*100000)])
dstFilePath = r"E:\2123\HS_H08_20190227_0000_B01_FLDK_R10warptt.tiff"

warpDs = gdal.Warp(outtif, memDs, dstSRS='EPSG:4326', outputBounds=(60.0, -90.0, 222.0, 90.0), xRes=res, yRes=res)
del warpDs
