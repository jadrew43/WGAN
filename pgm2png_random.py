# -*- coding: utf-8 -*-
"""
Created on Wed May 30 13:56:10 2018

@author: colinpate
"""
import numpy as np
import os
import argparse
from PIL import Image


#parser = argparse.ArgumentParser()
#parser.add_argument("--input_dir", required=True, help="path to folder containing images")
#parser.add_argument("--output_dir", required=True, help="output path")
#a = parser.parse_args()

def convert(src_path, dest_path):
    block_width = 300
    
    foo = open(src_path, "rb")
    foo.read(3)
    width = int(foo.read(4))
    foo.read(1)
    height = int(foo.read(4))
    foo.read(11)
    #print(foo.read(11))
    fileout = foo.read()
    #print(width * height*4)
    #print(len(fileout))
    
    picture = np.reshape(np.frombuffer(fileout, np.float32), (height, width))
    
    print(np.amin(picture))
    good_slices = 0
    slices = 0
    
    out_slice = np.zeros((block_width, block_width), dtype=np.int32)
    max_val = 2**16 - 1
    
    for block_num in range(60):
        x_sel = np.random.randint(0, width - block_width)
        y_sel = np.random.randint(0, height - block_width)
        pic_slice = picture[y_sel:y_sel+block_width, x_sel:x_sel+block_width]
        bad_slice = 0
        num_bad_pix = 0
        for nx in range(block_width):
            for ny in range(block_width):
                #out_slice[ny][nx] = max_val / block_width * nx
                if np.isinf(pic_slice[ny][nx]):
                    num_bad_pix += 1
                else:
                    out_slice[ny][nx] = max_val * 20 / pic_slice[ny][nx]
                if num_bad_pix > block_width / 3:
                    bad_slice = 1
                    break
            if bad_slice:
                break
        slices += 1
        if not bad_slice:
            good_slices += 1
            img = Image.fromarray(out_slice, "I")
            img.save(dest_path + "x" + str(x_sel) + "y" + str(y_sel) + ".png")
    print("max/good")
    print(slices)
    print(good_slices)
    img = Image.fromarray(picture, 'F')
    #img.show()
    foo.close() #y/1 = max/x --> max/y = x
    
def main():
    if not os.path.exists("pngfiles"):
        os.makedirs("pngfiles")
    
    for filename in os.listdir("pfmfiles"):
        if filename[-4:] == ".pfm":
            convert("pfmfiles\\" + filename, "pngfiles\\" + filename[:-4])
            
main()