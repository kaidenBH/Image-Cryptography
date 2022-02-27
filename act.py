import cv2
from GeometricTransformations import *

def TransformationsGeo(image, imageCV, x, y, angle, factor, Value):
    if factor < 0: factorCV = 1/abs(factor - 1)
    else: factorCV = factor
    if Value == 1: return Translation(image, int(y), int(x)), cv2.warpAffine(imageCV, np.float32([[1, 0, x],[0, 1, y]]), (imageCV.shape[1], imageCV.shape[0])), 'Translation'
    elif Value == 2: return rotation(image, angle), cv2.warpAffine(imageCV, cv2.getRotationMatrix2D((imageCV.shape[1]/2, imageCV.shape[0]/2), angle, 1), (imageCV.shape[1], imageCV.shape[0])), 'Rotation'
    elif Value == 3: return resize(image, factor), cv2.resize(imageCV, None, fx=factorCV, fy=factorCV, interpolation = cv2.INTER_CUBIC), 'Scale'
    elif Value == 4: return Shear(image, float(y), float(x)), cv2.warpPerspective(imageCV, np.float32([[1, float(x), 0],[float(y), 1, 0],[0, 0, 1]]), (imageCV.shape[1], imageCV.shape[0])), 'shear'

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def stretchImage (image,factor):
    w, h = len(image[0]), len(image)  
    #for index in range(factor):
    newH,newW = h//factor,w*factor
    #print(newW,newH)
    newIm = np.zeros((newH,newW,3)).tolist()
    #for every pixel in origin image put:
    # (2x,y/2)          if 0<=x<1/2 
    # (2x-1,(y+1)/2)    if 1/2<=x<=1
    for col in range(w):
        for row in range(h-1):
            if row<h//factor:
                p = image[row][col]
                newIm[int(row//factor)][int(col*factor)] = p
            else:
                p = image[row][col]
                newIm[int((row+1)//factor)][int(factor*col-1)] = p
            
    return newIm, 'backed'
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def BackedMap(image,factor,value): 
    orW, orH = len(image[0]), len(image)  
    if factor <=1: 
        print(factor) 
        return image,'Backed_map'
    else:
        myIm = image
        #for index in range(factor):
        StrIm,name = stretchImage(myIm,factor)
        w, h = len(StrIm[0]), len(StrIm) 
        newW,newH = w//factor,h*factor
        #print(newW,newH)
        newIm = np.zeros((newH,newW,3)).tolist()
        #for every pixel in streched image put:
        # (x+height,y)          if 0<y<1/2 
        # (2,y-(width/2))    if 1/2<=y<=1
        for col in range(w-1):
            for row in range(h-1):
                p = StrIm[row][col]
                #row = original height del image -(colo/orignila width del image +1)*heigh del streched image+1
                #col = col d fiha howa-(col/orignila width del image)*orignila width del image
                newIm[orH-(col//orW+1)*h+1][col-(col//orW)*orW] = p
                '''if col < w//factor:
                    p = StrIm[row][col]
                    newIm[int(row+h)][col] = p
                else:
                    
                    p = StrIm[row][col]
                    newIm[row][int(col-(w//factor))] = p'''
        #myIm = newIm
                    
        return newIm,'Backed_map'
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def catMap(image, a, b):
    I = np.zeros_like(image)

    Ys, Xs = np.mgrid[0 : image.shape[0], 0 : image.shape[1]]

    nX = (Xs + a * Ys) % image.shape[0]
    nY = (b * Xs + (a * b + 1) * Ys) % image.shape[1]

    I[nY, nX] = image[Ys, Xs]
    image = np.copy(I)
    return I,'Cat_map'
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def FridDeffusion(image, cr,cg,cb, g):
    w,h = image.shape[1],image.shape[0]
    newIm = np.full((h,w, 3), [cr,cg,cb], dtype = np.uint8)
    for row in range(h):
        for col in range(w):
            if col == 0 and row == 0:
                p = np.add(image[row,col] , (g*newIm[0,0])% (256))
                newIm[row,col] = p
            elif col == 0 and row != 0:
                p = np.add(image[row,col] , (g*newIm[row-1,w-1])% (256))
                newIm[row,col] = p
            else:
                p = np.add(image[row,col] , (g*newIm[row,col-1])% (256))
                newIm[row,col] = p

    return newIm,'frid_Deff'
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def FridDecrypt(image, cr,cg,cb, g):
    w,h = image.shape[1],image.shape[0]
    newIm = np.full((h,w, 3), [cr,cg,cb], dtype = np.uint8)
    for row in range(h):
        for col in range(w):
            if col == 0 and row == 0:
                p = (image[row,col] - (g*newIm[0][0])% (256))
                newIm[row,col] = p
            elif col == 0 and row != 0:
                p = (image[row,col] - (g*image[row-1,w-1])% (256))
                newIm[row,col] = p
            else:
                p = (image[row,col] - (g*image[row,col-1])% (256))
                newIm[row,col] = p

    return newIm,'frid_decrypt'