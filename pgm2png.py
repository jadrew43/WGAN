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
    foo = open(src_path, "rb")
    foo.read(3)
    width = int(foo.read(4))
    foo.read(1)
    height = int(foo.read(4))
    foo.read(5)
    
    picture = np.reshape(np.frombuffer(foo.read(), np.uint8), (height, width))
    img = Image.fromarray(picture, 'L')
    img.save(dest_path)
    foo.close()
    
def main():
    if not os.path.exists("pngfiles"):
        os.makedirs("pngfiles")
    
    for filename in os.listdir("pgmfiles"):
        if filename[-4:] == ".pgm":
            convert("pgmfiles\\" + filename, "pngfiles\\" + filename[:-4] + ".png")
            
main()