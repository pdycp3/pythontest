from shapely.geometry import MultiPolygon
from shapely.geometry import Polygon
a = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]
b = [(1, 1), (1, 2), (2, 2), (2, 1), (1, 1)]
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
