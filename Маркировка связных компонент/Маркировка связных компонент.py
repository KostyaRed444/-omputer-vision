import numpy as np
import matplotlib.pyplot as plt

def find(label,linked):
    j=label
    while linked[j]!=0:
        j=linked[j]
    return j

def union(l1,l2,linked):
    j=find(l1,linked)
    k=find(l2,linked)
    if j!=k:
        linked[k]=j


def check(B,y,x):
    if not 0<=y<B.shape[0]:
        return False
    if not 0<=x<B.shape[1]:
        return False
    if B[y,x]==0:
        return False
    return True


def prior_neighbors(B,y,x):
    left=y,x-1
    top=y-1,x
    if not check(B,*left):
        left=None
    if not check(B,*top):
        top=None
    return left,top


def exists(neighbors):
    return not all([n is None for n in neighbors])


def two_pass_labeling(B):
    size=np.ceil(B.shape[0]/2)*np.ceil(B.shape[1]/2)
    linked=np.zeros(int(size),dtype="int32")
    label=1
    LB=np.zeros_like(B)
    for i in range(B.shape[0]):
        for j in range(B.shape[1]):
            if B[i,j]!=0:
                A=prior_neighbors(B,i,j)

                if not exists(A):
                    M=label
                    label+=1
                else:
                    labels=[LB[i] for i in A if i is not None]
                    M=min(labels)
                LB[i,j]=M
                for t in A:
                    if t is not None:
                        lb=LB[t]
                        if lb!=M:
                            union(M,lb,linked)
    newLabels=[]
    for i in range(B.shape[0]):
        for j in range(B.shape[1]):
            if B[i,j]!=0:
                new_label=find(LB[i,j],linked)
                if new_label not in newLabels:
                    newLabels.append(new_label)
                LB[i,j]=newLabels.index(new_label)+1
    return LB
    
def quantity(im):
    c = len(set(im.ravel()))-1
    return c
    
if __name__=="__main__":
    image = np.zeros((20,20), dtype = "int32")
    image[1:-1, -2] = 1
    image[1, 1:5] = 1
    image[1, 7:12] = 1
    
    image[2,1:3] = 1
    image[2,6:8] = 1
    image[3:4, 1:7] = 1
    
    image[7:11, 11] = 1
    image[7:11, 14] = 1
    image[10:15, 10:15] = 1
    
    image[5:10, 5] = 1
    image[5:10, 6] = 1
    
    newim=two_pass_labeling(image)
    print("Labels - ", list(set(newim.ravel()))[1:])
    quantity(newim)
    plt.figure(figsize = (12,5))
    plt.subplot(121)
    plt.title("ORIGINAL")
    plt.imshow(image, cmap = "gray")
    plt.subplot(122)
    plt.title("NEW")
    plt.imshow(newim, cmap = "gray")
    plt.show()