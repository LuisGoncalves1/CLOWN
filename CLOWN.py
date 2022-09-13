from Functions.ImageAnalysis import read, StarFinder, find_matching_stars, MaskApplier, FirstAnalysis, SecondAnalysis
from Functions.CoordinateChange import PixelToAltaz, AltazToPixel
from Functions.Catalogue import ReadCatalogue, Convert_Catalogue
from Functions.Reader import ReadConfig, ReadFile


from astropy.coordinates import EarthLocation
import astropy.units as u
import cv2

import matplotlib.pyplot as plt
import numpy as np

import time
from astropy.io import fits
import os

import sys


config_file = sys.argv[1]
# ~ config_file = 'ConfigPASO.txt'





#########################################################################################################################################################################################################################
def rgb2gray(rgb):
    dado = np.dot(rgb[...,:3], [0.2989, 0.5871, 0.1140])
    dado = dado.astype(int)
    return dado

information = ReadConfig(config_file)
zenith = (information['zenith_X'],information['zenith_Y'])
phase = information['phase']
max_magnitude = information['max_magnitude']
min_altitude = information['min_altitude']	
location=EarthLocation(
        lat=information['LAT']*u.deg,
        lon=information['LON']*u.deg,
        height=information['height'] * u.m
    )
max_sigma = information['max_sigma']
min_sigma = information['min_sigma']
num_sigma = int(information['num_sigma'])
threshold = information['threshold']
focal = information['focal_length']
pixel_size = information['pixel_size']
mapping = information['mapping']
precision = float(information['precision'])
reverse = information['reverse']
ImageFolder = 'Images/' + information['ImageFolder'] + '/'
Images = os.listdir(ImageFolder)
Mask = information['Mask']
l = int(information['l'])
square = int(information['square'])
AnalysisThreshold = information['AnalysisThreshold']*255

mascara = rgb2gray(cv2.imread(Mask))
catalogue = ReadCatalogue(information['catalogue'],max_magnitude = max_magnitude)		
if len(Images) > 1:
	for image in Images:
		Image,timestamp = ReadFile(ImageFolder,image,information['UTC'])												  # Reads the image
		print('Working on ' + image)
		catalog_stars, magnitude = Convert_Catalogue(catalogue, timestamp, location, min_altitude=min_altitude)  		  # selects only the stars visible in that location at that timestamp
		Y, X, R = StarFinder(Image,max_sigma=max_sigma,min_sigma=min_sigma,num_sigma=num_sigma,threshold=threshold)       # Finds the objects in the image
		if Mask != 'None':
			X, Y, R = MaskApplier(X,Y,R,mascara)
		coord = PixelToAltaz(X,Y,zenith,location,timestamp,phase,mapping,focal,pixel_size,reverse = reverse)			  # Transforms the pixel coordinates to Altitude/Azimute
		mask = coord.alt.deg > min_altitude 																			  # Removes stars with a lower altitude than the minimum chosen
		idx,found = find_matching_stars(catalog_stars, coord[mask], max_sep=precision * u.deg)							  # Matches the stars
		X2,Y2 = AltazToPixel(catalog_stars,zenith,phase,mapping,focal,pixel_size, reverse = reverse) 			  		  # Catalogue Stars
		X4,Y4 = X2[~found],Y2[~found]																					  # Missing Stars
		
		Image2 = FirstAnalysis(Image.shape[0:2],l,X4,Y4)
		Image3 = SecondAnalysis(Image2,square,AnalysisThreshold)
		if Mask != 'None':
			Image3 = np.maximum(Image3,~mascara+256)
		cv2.imwrite('Cloud Masks/' + information['ImageFolder'] + '/' + image, Image3)
		
					
		if information['GRAPH']:
			vmin = None
			vmax = None
			fig,axes = plt.subplots(1,4)
			ax = axes.ravel()
			ax[0].imshow(Image,cmap='gray',vmin=vmin or np.nanpercentile(Image, 0.1),vmax=vmax or np.nanpercentile(Image, 99))
			ax[1].imshow(Image,cmap='gray',vmin=vmin or np.nanpercentile(Image, 0.1),vmax=vmax or np.nanpercentile(Image, 99))
			for contador in range(len(Y)):
					c1 = plt.Circle((X[contador],Y[contador]),0.4, color = 'green', linewidth=2,fill=False)
					ax[1].add_patch(c1)
					
			for contador in range(len(Y2)):
					c1 = plt.Circle((X2[contador],Y2[contador]),0.4, color = 'red', linewidth=2,fill=False)
					ax[1].add_patch(c1)
			
			ax[2].imshow(Image2,cmap='gray',vmin=vmin or np.nanpercentile(Image, 0.1),vmax=vmax or np.nanpercentile(Image, 99))
			ax[3].imshow(Image3,cmap='gray',vmin=vmin or np.nanpercentile(Image, 0.1),vmax=vmax or np.nanpercentile(Image, 99))
			# ~ ax[4].imshow(Image4,cmap='gray',vmin=vmin or np.nanpercentile(Image, 0.1),vmax=vmax or np.nanpercentile(Image, 99))
			plt.show()
			
