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
    img = Image.open(src_path).convert("I")
    #img.show()
    im_width = 256
    a = np.asarray(img)#, dtype=np.uint8)
    
    max_val = 2**16 - 1
    
    print(src_path)
    picture = np.reshape(a, (im_width, im_width))
    newpic = np.zeros((im_width, im_width), dtype=np.int32)
    
    for x in range(im_width):
        for y in range(im_width):
            newpic[x, y] = max_val / max(picture[x, y], 1)
    
    img2 = Image.fromarray(newpic, 'I')
    #img2.show()
    #input("LOL")
    img2.save(dest_path + ".png")
    #foo.close() #y/1 = max/x --> max/y = x
    
def main():
    if not os.path.exists("dispar_files"):
        os.makedirs("dispar_files")
    
    dir_name = "outnew\images"
    for filename in os.listdir(dir_name):
        if filename[-4:] == ".png":
            convert(dir_name + "\\" + filename, "dispar_files\\" + filename[:-4])
            
main()