import xlrd
wb=xlrd.open_workbook('work.xls')
ws=wb.sheet_by_name('数字表')
nrow=ws.nrows  #获取行列号
ncol=ws.ncols
print(nrow)
print(ncol)
row_data=ws.row_values(4) #读取行数据
print(row_data)
cell_data=ws.cell_value(2,1) #读取单元格数据
print(cell_data)
cell_dat=ws.cell(2,1) #可以获取表格的类型和值
print(cell_dat)




