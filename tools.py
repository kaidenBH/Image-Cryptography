import numpy as np
from PIL import Image

def getImage(image_path):    # obtenir les pixels de la matrice 
    im = Image.open(image_path)   # ouvrir l'image 
    #width, height = im.size
    im_rgb = im.convert("RGB")   # le convertir en RGB 
    pixel = np.array(im_rgb)   # RGB matrice
    pixel = pixel.tolist()
    return pixel    # return la matrice

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def SaveImage(image, name):
    Image.fromarray(np.array(image).astype('uint8')).save('Images/Saved/'+name+'.png', format='png')
    return 'Images/Saved/'+name+'.png'

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def correct_image(image):
    np.putmask(image, image>255, 255)
    np.putmask(image, image<0, 0)
    return image

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def checkNull(var):
        return 0 if len(var) == 0 else var
        """
        if len(var) == 0: return 0
        else: return var
        """





