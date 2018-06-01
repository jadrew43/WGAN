# -*- coding: utf-8 -*-
"""
Created on Wed May 30 13:56:10 2018

@author: colinpate
"""
import numpy as np
from scipy.ndimage import gaussian_filter
import os
import argparse
from PIL import Image


#parser = argparse.ArgumentParser()
#parser.add_argument("--input_dir", required=True, help="path to folder containing images")
#parser.add_argument("--output_dir", required=True, help="output path")
#a = parser.parse_args()

def fill_holes(valid_pixels, valid_pixel_vals):
    vp_blur = gaussian_filter(valid_pixels, (5, 5))
    vpv_blur = gaussian_filter(valid_pixel_vals, (5, 5))
    outputarr = np.zeros((300, 300), dtype=np.int32)
    for x in range(0, 300):
        for y in range(0, 300):
            if valid_pixels[x][y] == 0:
                if vp_blur[x][y] > 0:
                    outputarr[x][y] = vpv_blur[x][y]  / vp_blur[x][y]
                else:
                    outputarr[x][y] = 0
            else:
                outputarr[x][y] = valid_pixel_vals[x][y] / 1000000000
    return outputarr

def convert(src_path, dest_path_input, dest_path_target):
    block_width = 300
    
    foo = open(src_path, "rb")
    foo.read(3)
    width = int(foo.read(4))
    foo.read(1)
    height = int(foo.read(4))
    foo.read(11)
    fileout = foo.read()
    
    picture = np.reshape(np.frombuffer(fileout, np.float32), (height, width))
    
    print(np.amin(picture))
    good_slices = 0
    slices = 0
    
    input_slice = np.zeros((block_width, block_width), dtype=np.int32)
    
    max_val = 2**16 - 1
    
    min_bad = 100
    max_bad = 7000
    
    for block_num in range(50):
        valid_pix = np.zeros((block_width, block_width), dtype=np.float32)
        valid_pix_vals = np.zeros((block_width, block_width), dtype=np.float32)
        
        x_sel = np.random.randint(0, width - block_width)
        y_sel = np.random.randint(0, height - block_width)
        pic_slice = picture[y_sel:y_sel+block_width, x_sel:x_sel+block_width]
        
        bad_slice = 0
        num_bad_pix = 0
        for nx in range(block_width):
            prev_val = 0
            for ny in range(block_width):
                if np.isinf(pic_slice[ny][nx]):
                    num_bad_pix += 1
                    input_slice[ny][nx] = 0
                else:
                    this_val = max_val * 20 / pic_slice[ny][nx]
                    valid_pix_vals[ny][nx] = this_val * 1000000000
                    valid_pix[ny][nx] = 1000000000
                    input_slice[ny][nx] = this_val
                if num_bad_pix > max_bad:
                    bad_slice = 1
                    break
            if bad_slice:
                break
        slices += 1
        if (not bad_slice) and (num_bad_pix > min_bad):
            good_slices += 1
            img = Image.fromarray(input_slice, "I")
            img.save(dest_path_input + "x" + str(x_sel) + "y" + str(y_sel) + ".png")
            target_im = fill_holes(valid_pix, valid_pix_vals)
            img = Image.fromarray(target_im, "I")
            img.save(dest_path_target + "x" + str(x_sel) + "y" + str(y_sel) + ".png")
    print("max/good")
    print(slices)
    print(good_slices)
    img = Image.fromarray(picture, 'F')
    #img.show()
    foo.close() #y/1 = max/x --> max/y = x
    
def main():
    if not os.path.exists("pngtargets"):
        os.makedirs("pngtargets")
    if not os.path.exists("pnginputs"):
        os.makedirs("pnginputs")
    
    file_list = os.listdir("pfmfiles")
    
    for i in range(len(file_list)):
        filename = file_list[i]
        print("Pic " + str(i) + " out of " + str(len(file_list)))
        if filename[-4:] == ".pfm":
            convert("pfmfiles\\" + filename, "pnginputs\\" + filename[:-4], "pngtargets\\" + filename[:-4])
            
main()