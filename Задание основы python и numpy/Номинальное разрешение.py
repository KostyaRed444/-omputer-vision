import numpy as np
import matplotlib.pyplot as plt

def getNominalResolution(image,realSize):
    lst=[]
    lst.append(np.where(image==1))
    max=0
    for i in range(len(lst[0][0])):
        for j in range(len(lst[0][0])):
            if i!=j:
                temp=((lst[0][0][i]-lst[0][0][j])**2 + (lst[0][1][i]-lst[0][1][j])**2)**0.5
                if temp>max: max=temp
    return (max/realSize)
    
for i in range(6):
    f="figure"+str(i+1)+".txt"
    ff=open(f)
    realSize=float(ff.readline())
    ff.close()
    data = np.genfromtxt(fname=f,skip_header=1)
    getNominalResolution(data,realSize)
    print(f," nominal resolution",getNominalResolution(data,realSize))
