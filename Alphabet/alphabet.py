# -*- coding: utf-8 -*-
import numpy as np
from skimage import filters
from skimage.measure import label, regionprops
from skimage import morphology
from skimage import draw
import matplotlib.pyplot as plt


def count_holes(s):
    s = np.logical_not(s).astype('uint8')
    
    ss = np.ones((s.shape[0] + 2, s.shape[1] + 2))
    ss[1:-1, 1:-1] = s    
    LBs = label(ss)
    LBs[LBs == 1] = 0
    
    return len(np.unique(LBs))-1

def has_vline(s):
    line = np.sum(s, 0) // s.shape[0]
    return 1 in line

def hole_centers(s):
    s = np.logical_not(s).astype('uint8')
    ss = np.ones((s.shape[0] + 2, s.shape[1] + 2))
    ss[1:-1, 1:-1] = s
    LBs = label(ss)
    LBs[LBs == 1] = 0
    centers = []
    labels = np.unique(LBs)
    for lb in labels:
        if lb == 0:
            continue
        x = int(np.mean(np.where(LBs == lb)[0]))
        y = int(np.mean(np.where(LBs == lb)[1]))
        centers.append((x,y))
    return centers        
    
# Считает кол-во штрихов
def count_hatch(s):
    up = s[0, :]
    upe = np.zeros(len(up) + 2)
    upe[1: -1] = up
    upe = np.abs(np.diff(upe))
    
    intervals = np.where(upe > 0)[0]
    points_up = []
    
    for p1, p2 in zip( intervals[::2], intervals[1::2]):
        points_up.append((p2+p1) // 2)
#    print(points_up)
    
    down = s[-1, :]
    downe = np.zeros(len(down) + 2)
    downe[1: -1] = down
    downe = np.abs(np.diff(downe))
    
    intervals = np.where(downe > 0)[0]
    points_down = []
    
    for p1, p2 in zip( intervals[::2], intervals[1::2]):
        points_down.append((p2+p1) // 2)
#    print(points_down)    
    h = 0 # Кол-во штрихов.
    for p1 in points_up:
        for p2 in points_down:
            line = draw.line(0, p1, s.shape[0] - 1, p2)
            if np.all(s[line] == 1):
                h += 1
#    print (h)
    if (h == 0):
        h = has_vline(s)
    return h

def recognite(s):
#   Смотрим кол-во отверстий в букве.
    holes = count_holes(s)
    if holes == 2:
#        Считаем штрихи
        hatches = count_hatch(s)
        if hatches == 1:
            return "B"
        else:
            return "8"
    elif holes == 1:
        hatches = count_hatch(s)
        if hatches > 0:            
            if has_vline(s):
                if hole_centers(s)[0][0] <= s.shape[0]/2.6:
                    return "P"
                else:
                    return "D"
            else:
                return "A"
        else:
            return "0"
    else:
        hatches = count_hatch(s)
#        print(hatches)
        ratio = s.shape[0] / s.shape[1] # Соотношение (процентное) высоты к ширине
#        print("Ratio = ", ratio)
        if (hatches == 4):
            return "W"
        elif hatches == 2:
            return "X"
        elif has_vline(s) and ratio > 1:
            return "1"
        elif (hatches == 1) and (0.9 < ratio < 1.1):
            return "*"
        elif (hatches == 1) and (1.9 < ratio < 2.1):
            return "/"
        elif (hatches == 1) and (ratio < 0.5):
            return "-"
    return ""
    
if __name__ == "__main__":
    
    alphabet = plt.imread("C:/Users/1052126/Desktop/symbols.png")    
    alphabet = np.mean(alphabet, 2)    
    thresh = filters.threshold_otsu(alphabet)
    
    alphabet[alphabet < thresh] = 0
    alphabet[alphabet >= thresh] = 1
    
    count = len(np.unique(label(alphabet)))
    
    b_alpha = np.zeros_like(alphabet)
    b_alpha[alphabet < thresh] = 0
    b_alpha[alphabet >= thresh] = 1
    plt.figure(figsize = (20,20))
    plt.imshow(b_alpha)
    LB = label(b_alpha)
    props = regionprops(LB)
    
    count_symbols = {};
    index = 0;
    while (True):
        try:
           s = props[index].image 
           if count_symbols.get(recognite(s)):
               count_symbols[recognite(s)] = count_symbols[recognite(s)] + 1
               if recognite(s) == '':
                   plt.imshow(s)
                   plt.show()
#                   pass
           else:
               count_symbols[recognite(s)] = 1
           index += 1
        except Exception as e:
            print(e)
            break;
    print(count_symbols)

