import numpy as np
import matplotlib.pyplot as plt

holst=np.zeros((100,100))

def draw_circle(holst,radius,a,b,line_width):
    for i in range(holst.shape[0]):
        for j in range(holst.shape[1]):
            tt=((i-a)**2 + (j-b)**2)
            r=radius**2
            if tt<=r and tt>=r-line_width:
                holst[i][j]=1
                
draw_circle(holst,25,50,50,50)
plt.figure()
plt.imshow(holst)
plt.show()
