# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 13:36:35 2018

@author: colinpate
"""

import os
from PIL import Image
import numpy as np

height = 256
width = 256

def main():
    file_dir = input("Test output directory?")
    
    file_list = os.listdir(file_dir + "\\images")
    
    overall_se = 0
    pt_ct = 0
    
    for i in range(len(file_list)):
        filename = file_list[i]
        if filename[-11:] == "targets.png":
            pt_ct += width * height
            this_im_se = 0
            
            print("Pic " + str(i) + " out of " + str(len(file_list)))
            targ_im = Image.open(file_dir + "\\images\\" + filename)
            targ_arr = np.reshape(np.asarray(targ_im), (height, width, 3))
            out_im = Image.open(file_dir + "\\images\\" + filename[:-11] + "outputs.png")
            out_arr = np.reshape(np.asarray(out_im), (height, width, 3))
            input_im = Image.open(file_dir + "\\images\\" + filename[:-11] + "inputs.png")
            in_arr = np.reshape(np.asarray(input_im), (height, width, 3))
            
            for x in range(width):
                for y in range(height):
                    if in_arr[x,y,0] == 0:
                        overall_se += (float(targ_arr[x,y,0]) - float(out_arr[x,y,0]))**2
                        this_im_se += (float(targ_arr[x,y,0]) - float(out_arr[x,y,0]))**2
            print("This image MSE: " + str(this_im_se  / (width * height)))
    print("Final MSE: " + str(overall_se / pt_ct))
main()