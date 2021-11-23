
# list=[]
# list1=[]
# list2=[]
# list.append(1)
# list.append("now")
# list.append("草地")
# list1.append(2)
# list1.append("before")
# list1.append("林地")
# list2.append(list)
# list2.append(list1)
# print(list2[0])
# print(list2[0][0])
# print(list2[1][1])

# print(len(list))
# print(list[0])
# print(list[1])
# print(list[2])
# list=[];
# list.append((1,"now","草地"))
# list.append((2,"before","林地"))
# print(len(list))
# print(list[0])
# print(list[1])
# print(list[0][0])
# print(list[1][1])
from tqdm import tqdm

pbar = tqdm(range(300))  # 进度条

for i in pbar:
    err = 'abc'
    pbar.set_description("Reconstruction loss: %s" % (err))
















