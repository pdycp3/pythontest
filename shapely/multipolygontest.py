from shapely.geometry import MultiPolygon
from shapely.geometry import Polygon
from shapely import wkt
a = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]
b = [(1, 1), (1, 2), (2, 2), (2, 1), (1, 1)]
c=[(0.1,0.1), (0.1,0.2), (0.2,0.2), (0.2,0.1)]
listtt=[]
listtt.append(1)
listtt.append(2)
listtt.append(3)
listtt.append(4)
listmark=[]
listmark.append(2)

print(listtt)
del listtt[listmark[0]]
print(listtt)
print("Test start..............\n")
p1=Polygon(a)
p2=Polygon(b)
p3=Polygon(c)
ps1=p1.wkt
ps2=p2.wkt
ps3=p3.wkt
print("this is polygon a:",ps1)
print("this is polygon b:",ps2)
print("this is polygon c:",ps3)
sps1="u"+ps1
sps2="u"+ps2
sps3="u"+ps3
print("sps1 is :",sps1)
print("sps2 is :",sps2)
print("sps3 is :",sps3)
print(sps3)
mp1=wkt.loads(ps1)
mp2=wkt.loads(ps2)
mp3=wkt.loads(ps3)
print("mp1 is :",mp1.type)
print("mp2 is :",mp2.type)
print("mp3 is :",mp3.type)
mlt1=MultiPolygon([mp1])
mlt2=MultiPolygon([mp2])
mlt3=MultiPolygon([mp3])
print("mlt1 type is :",mlt1.type)
print(mlt1)
print("mlt2 type is :",mlt2.type)
print(mlt2)
print("mlt3 type is :",mlt3.type)
print(mlt3)
mlt1=mlt1.union(mlt2)
print(mlt1)
#print(newmt)










n1=[a,[]]
print(len(n1))
print(type(n1[0]))
print(n1[0])
n2=[b,[]]
n3=[n1,n2]
t1=type(n1)
t2=type(n2)
t3=type(n3)
print(t1)
print(t2)
print(t3)
multi1 = MultiPolygon(n3)
c=a+b
list=[]
list1=[]
list.append("Polygon")
ap=Polygon(a)
bp=Polygon(b)
list.append(ap)
list.append(bp)
n1=type(list[0])
n2=type(list[1])
n3=type(list[2])
print(n1)
print(n2)
print(n3)
print(list)
ob = MultiPolygon( [ (((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)),[((0.1,0.1), (0.1,0.2), (0.2,0.2), (0.2,0.1))])] )

ntup=tuple(list)
new=type(ntup)
ob1=MultiPolygon(ntup)
print(new)
print("ob is :",ob)
print("ob type is:",ob.type)
print("ob1 is :",ob1)
print("ob1 type is:",ob1.type)


if ob1.is_valid:
    print("有效")
    obnew=ob.union(ob1)

    if obnew.is_valid:
        print("obnew is :",obnew)
        print("obnew type is :",obnew.type)
        print("youxiao")
        print(obnew.type)
