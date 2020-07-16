import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
import pandas as pd
import seaborn as sns
from PIL import *
from PIL import ImageDraw
from PIL import ImageFilter
import random
from glitches.glitches import *

'''
add_pix_line(img, n)
add_pixel(img)
add_rainbow(img, max_width=500, max_height=500):
cut_and_paste(img,n):
repeat_pix_line(img, n):
skybo(img):
redshadows(img):
chaos(img):
'''

def choices():
    print(' add_pix_line(img, n) \n add_rainbow(img, max_width=500, max_height=500) \n cut_and_paste(img,n) \n repeat_pix_line(img, n) \n skybo(img) \n redshadows(img) \n chaos(img)')

def add_pix_line(img, n):

    ######################
    #add line of single width pixels at random neon color
    
    #img = image file
    #n = number of times repeated
    #####################


    #fuschia, green, cyan, reddish pink, yellow
    neon_opt = [(254, 89, 112), (250, 254, 89), (220,0,193), (255,198,0), (255,85,117), (241,59,62), (195,184,109),(222,205,190), (35,182,204),(245,246,60), (140,102,46), (66,217,243)]
    neon_choice = random.randint(0,len(neon_opt)-1)
    neon_color = neon_opt[neon_choice]
    #choose a random alpha 
    alpha_opt = random.randint(50,100)

    #create color/alpha for line
    pix_line_color = tuple(np.append(neon_color,alpha_opt))#.tolist()

    #choose a random start location; no more than half the width/height of the image
    start_width = random.randint(1, round(img.width/2))
    start_height = random.randint(1, round(img.height/2))

    #choose either across or down as the main direction
    pix_line_dir = random.randint(0,1)

    #choose length of line; no wider/longer than image
    poly = Image.new('RGBA', (img.width,img.height))
    pdraw = ImageDraw.Draw(poly)

    line_width = random.randint(1,5)
    if pix_line_dir == 0:
        #width
        pix_line_len = random.randint(10, (img.width-start_width))

        pdraw.line([start_width, start_height,start_width+pix_line_len,start_height],fill=pix_line_color,width=line_width)
    else:
        #height
        pix_line_len = random.randint(10, (img.height-start_height))
        pdraw.line([start_width, start_height,start_width,start_height+pix_line_len],fill=pix_line_color,width=line_width)

    img.paste(poly, (0,0), mask=poly)

    return img

def add_pixel(img):

    ######################
    #add box of changd pixel colors
    
    #img = image file
    #####################

    #choose a random start location; no more than half the width/height of the image
    start_width = random.randint(1, img.width)
    start_height = random.randint(1, img.height)
    end_width = min(start_width, start_width + random.randint(1, max(2,round((img.width-start_width)/5))))
    end_height = min(start_height, start_height + random.randint(1, max(2,round((img.height-start_height)/5))))

    source = img.split()

    px1 = source[0].load()
    px2 = source[1].load()
    px3 = source[2].load()

    for i in range(start_width, end_width, 1):    # for every col:
        for j in range(start_height, end_height,1):    # For every row

            r = random.randint(0,255)
            f = random.randint(0,2)
            if f == 0:  
                px1[i,j] = (r) # set the colour accordingly
            elif f== 1:
                px2[i,j] = (r) # set the colour accordingly
            elif f== 2:
                px3[i,j] = (r) # set the colour accordingly

    img = Image.merge(img.mode,source)

    return img

#can extend this to add random colored pixels in random box at random locations with random color palette...

def add_rainbow(img, max_width=500, max_height=500):

    #add rainbow to (crop or whole image)
    
    if max_width > np.shape(img)[0]:
        max_width = np.shape(img)[0]
    if max_height > np.shape(img)[1]:
        max_height=np.shape(img)[1]
        
    poly = Image.new('RGBA', (img.width,img.height))
    pixels = poly.load() # create the pixel map
    
    color_intensity = random.randint(0,250)
    
    rand_width = random.randint(0,min(max_width,img.width))
    rand_height = random.randint(0,min(max_height,img.height))
    w_p = random.randint(0,img.width-rand_width)
    h_p = random.randint(0,img.height-rand_height)

    for i in range(rand_width):    # for every col:
        for j in range(rand_height):    # For every row
            alpha = random.randint(10,50)
            pixels[w_p+i,h_p+j] = (i, j, color_intensity, alpha) # set the colour accordingly
    

    #     start_width = random.randint(0,img.width-rand_width)
    #     start_height = random.randint(0,img.height-rand_height)        
    
    poly.filter(filter=ImageFilter.UnsharpMask)
    
    
    img.paste(poly, (0,0), mask=poly)
    
    return img

def cut_and_paste(img,n):
    #cut and paste random strip of image
    
    for i in range(n):    
        w_start = random.randint(0,img.width)
        h_start = random.randint(0,img.height)
        w_end = random.randint(w_start,img.width)
        h_end = random.randint(h_start,img.height)

        #choose either across or down as the main direction
        pix_line_dir = random.randint(0,1)

        #choose thickness
        thick = random.randint(5,min(img.width, img.height))

        if pix_line_dir == 0:
            #width
            crop = img.crop((w_start, h_start, w_end, h_start+thick))
        else:
            #height
            crop = img.crop((w_start, h_start, w_start+thick, h_end))

        w_p = random.randint(0,img.width-crop.width)
        h_p = random.randint(0,img.height-crop.height)

        img.paste(crop, (w_p, h_p))
        
    return img


def repeat_pix_line(img, n):

    #############################
    #add repeating set of lines
    
    #img = image file
    #n = number of lines repeated
    #############################
    
    #fuschia, reddish pink, yellow, brihgt pink,
    neon_opt = [(254, 89, 112), (250, 254, 89), (220,0,193), (255,198,0), (255,85,117), (241,59,62), (195,184,109),(222,205,190), (35,182,204),(245,246,60), (140,102,46), (66,217,243)]
    neon_choice = random.randint(0,len(neon_opt)-1)
    neon_color = neon_opt[neon_choice]

    #choose a random alpha 
    alpha_opt = random.randint(10,100)

    #choose a random start location; no more than half the width/height of the image
    start_width = random.randint(1, img.width) 
    start_height = random.randint(1, img.height) 

    pix_line_width = random.randint(1,3)
    if pix_line_width >= 2:
        alpha_opt = round(alpha_opt/4)

    #choose either across or down as the main direction
    pix_line_dir = random.randint(0,1)

    #choose length of line; no wider/longer than image
    poly = Image.new('RGBA', (img.width,img.height))
    pdraw = ImageDraw.Draw(poly)
    
    #create color/alpha for line
    pix_line_color = tuple(np.append(neon_color,alpha_opt))

    if pix_line_dir == 0:
        #width
        pix_line_len = random.randint(10, max(11,(img.width-start_width)))

        pdraw.line([start_width, start_height,start_width+pix_line_len,start_height],fill=pix_line_color,width=pix_line_width)
    else:
        #height
        pix_line_len = random.randint(10, max(11,(img.height-start_height)))
        pdraw.line([start_width, start_height,start_width,start_height+pix_line_len],fill=pix_line_color,width=pix_line_width)

    #img.paste(poly, (0,0), mask=poly)

    spacing = random.randint(4,8)
    
    for i in range(n):
        i = i+1
        #adjust color 
        pix_line_alt = tuple( min(255, max(0, j + random.randint(-40,40))) for j in pix_line_color)
        pix_line_color = pix_line_alt
        
        if pix_line_dir == 0:
        
            pdraw.line([start_width, start_height+i*spacing,start_width+pix_line_len,start_height+i*spacing],fill=pix_line_color,width=pix_line_width)
               
        else:

            pdraw.line([start_width+i*spacing, start_height,start_width+i*spacing,start_height+pix_line_len],fill=pix_line_color,width=pix_line_width)


        #choose length of line; no wider/longer than image
        #poly = Image.new('RGBA', (img.width,img.height))
        pdraw = ImageDraw.Draw(poly)

        img.paste(poly, (0,0), mask=poly)
        
        #option to only return poly? then can alter using skybo or redshadows

    return img    

def skybo(img):
    # split the image into individual bands
    source = img.split()

    R, G, B = 0, 1, 2

    # select regions where blue is greater than 200
    mask = source[B].point(lambda i: i >200 and 255)

    # process the red band
    out = source[R].point(lambda i: i + i * random.randint(-1,1)*random.random())

    # paste the processed band back, but only where red was < 100
    source[G].paste(out, None , mask)

    # build a new multiband image
    img = Image.merge(img.mode, source)
    
    return img

def bog(img):
    # split the image into individual bands
    source = img.split()

    R, G, B = 0, 1, 2
    
    s = random.randint(0,2)

    #
    r = random.randint(1,254)
    mask = source[s].point(lambda i: i <r)
    
    s = random.randint(0,2)
    #
    out = source[s].point(lambda i: i + i * random.randint(-10,10)*random.random())
    
    s = random.randint(0,2)
    # paste the processed band back, but only where red was < 100
    source[s].paste(out, None , mask)

    # build a new multiband image
    img = Image.merge(img.mode, source)
    
    return img


def redshadows(img):
    # split the image into individual bands
    source = img.split()
    
    R, G, B = 0, 1, 2

    # select regions where red is less than 100
    mask = source[R].point(lambda i: i <100 and i <50)

    # process the green band
    out = source[B].point(lambda i: i + i * random.randint(-1,1)*random.random())

    # paste the processed band back, but only where red was < 100
    source[R].paste(out, None , mask)

    # build a new multiband image
    img1 = Image.merge(img.mode, source)
    
    #want to be able to tune img so that we can make pasted pixels transparent
    
    return img1


def chaos(img):
    # split the image into individual bands
    source = img.split()
    img1 = img
    
    # select regions where rand source is </> rand int
    s = random.randint(0,2)
    minn = random.randint(1,100)
    maxx = random.randint(minn, 255)
    mask = source[s].point(lambda i: i <maxx and i >minn and 255)
    
    s = random.randint(0,2)
    # process the green band
    out = source[s].point(lambda i: i + i * random.randint(-1,1)*random.random())
    
    s = random.randint(0,2)
    # paste the processed band back, but only where red was < 100
    source[s].paste(out, None , mask)

    # build a new multiband image
    img1 = Image.merge(img1.mode, source)

    data = np.array(img1)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    for i in range(np.shape(alpha)[0]):
        for j in range(np.shape(alpha)[1]):
            alpha[i,j] = random.randint(1,255)

    data[:,:,3] = alpha.T

    img1 = Image.fromarray(data)
    img = img.paste(img1)
    #want to be able to tune img so that we can make pasted pixels transparent
    
    return img

