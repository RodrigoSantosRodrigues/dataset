# -*- coding: utf-8 -*-
'''
# -*- coding: utf-8 -*-
# Copyright (C) 2008-2009  Murphy Lab
# Carnegie Mellon University
# 
# Written by Luis Pedro Coelho <luis@luispedro.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# For additional information visit http://murphylab.web.cmu.edu or
# send email to murphy@cmu.edu

Adapted by Rodrigo Junior R
email: rodrjuniorsantos@gmail.com
'''
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
from scipy import ndimage

#---------------------------------------------------------------------------------------------------
# Parameter for removing artifacts
#---------------------------------------------------------------------------------------------------
_min_obj_size = 32

#---------------------------------------------------------------------------------------------------
# Generating reference images.
# Input image, image containing only the boundary edges
#---------------------------------------------------------------------------------------------------
def _process_B(B):
    L,N = ndimage.label(~B)
    bg = 0
    bg_size = (L==bg).sum()
    for i in range(1,N+1):
        i_size = (L == i).sum()
        if i_size > bg_size:
            bg_size = i_size
            bg = i
        if i_size < _min_obj_size:
            L[L==i] = 0 
    L[L==bg]=0
    L,_ = ndimage.label(L!=0)
    return L

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
print ('STARTED')

#List all images from the directory.
folder= os.listdir('imgs_delineadas_PNG/')

#start counter for file names
num=0
# Scroll through all the images listed. 
for i in range(0,len(folder)):
    im_act= folder[i]
    print(im_act)
    
    directoryFile= 'imgs_delineadas_PNG//{0}'.format(im_act)
    
    #Open image
    im = imread(directoryFile)
    
    # Receiving only the edges (red channel of the image)       
    im_borders = (im[:,:,0] > im[:,:,1])

    # Receiving reference image on labels
    im_reference = _process_B(im_borders)

    # Converting labeled image to binary image
    im_reference_threshold = im_reference > 0

    #save images in gray level.
    plt.imsave('imgs_borders//{0}.png'.format(im_act), im_borders, cmap='gray')
    plt.imsave('imgs_reference//{0}.png'.format(im_act), im_reference, cmap='nipy_spectral')
    plt.imsave('imgs_threshold//{0}.png'.format(im_act), im_reference_threshold, cmap='gray')
    num += 1

print("End")
