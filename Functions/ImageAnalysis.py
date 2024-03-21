import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import numpy as np
import math
import time 
import os
from astrometry_net_client import Session		
from astrometry_net_client import FileUpload
from skimage.feature import blob_log
from skimage.color import rgb2gray
from math import sqrt
import astropy.units as u
from astropy.coordinates import SkyCoord, Angle, match_coordinates_sky
import skimage.filters
from astropy.io import fits
from astropy.time import Time
import dateutil.parser

def rgb2gray(rgb):
    dado = np.dot(rgb[...,:3], [0.2989, 0.5871, 0.1140])
    dado = dado.astype(int)
    return dado

def DrawSquare(Image,X,Y,l):
	Image[int(Y-l/2):int(Y+l/2),int(X-l/2):int(X+l/2)] = 255
	return Image

def DrawCircle(Image,X,Y,l,shape):
	y, x = np.ogrid[:shape[0], :shape[1]]
	distance = np.sqrt((x - X)**2 + (y - Y)**2)
	mask = distance <= l/2

	Image[mask] = 255
	return Image


def MaskApplier(X,Y,R,mascara):	
	binary = []
	for i in range(len(X)):
		if mascara[int(Y[i])][int(X[i])] == 255:
			binary.append(True)
		else:
			binary.append(False)
		
	X = X[binary]
	Y = Y[binary]
	R = R[binary]
	
	return X,Y,R
	
	
	height, width = imagem.shape
	for y in range(0,height):
		for x in range(0,width):
			if np.all(mascara[y][x]<[2,2,2]):
				imagem[y][x]=0
	return imagem
	
def VideoMaker(PastaInicio,PastaFim,fps,tempo):
	frame_array=[]
	files =  [f for f in os.listdir(PastaInicio) if isfile(join(PastaInicio,f))]
	
	for i in range(len(files)):
		filename=PastaInicio+files[i]
		img = cv2.imread(filename)
		height, width, layers = img.shape
		size = (width,height)
		

		for k in range (tempo):
			frame_array.append(img)
			
	out=cv2.VideoWriter(PastaFim,cv2.VideoWriter_fourcc(*'mp4v'),fps,size)
	for i in range(len(frame_array)):
		out.write(frame_array[i])
	out.release()
	
def StarFinder(image,max_sigma=1,num_sigma=10,threshold=.03,exclude_border=True,min_sigma=0):
	blobs = blob_log(image, max_sigma=max_sigma, num_sigma=num_sigma, threshold=threshold,exclude_border=exclude_border)
	blobs[:, 2] = blobs[:, 2] * sqrt(2)	
	return blobs[:,0],blobs[:,1],blobs[:,2]

def find_matching_stars(catalog_stars, image_stars, max_sep=0.5 * u.deg):
    if len(image_stars) == 0:
        return np.array([], dtype=int), np.zeros(len(catalog_stars), dtype=bool)

    idx, d2d, d3d = match_coordinates_sky(catalog_stars, image_stars)
    mask = d2d < max_sep

    return idx, mask
    
def read(path):
	name, ext = os.path.splitext(path)
	print(ext)
	if ext == 'fits.gz' or ext == '.gz' or ext == 'fit':
		with fits.open(path) as f:        
			img = f[0].data
			timestamp = Time(dateutil.parser.parse(f[0].header['TIMEUTC']))
	elif ext == '.fits':
		with fits.open(path) as f:
			img = f[0].data.astype(float)
			img /= 2**16
			timestamp = Time(f[0].header['DATE-OBS'])

			return img,timestamp

	else:
		raise TypeError
       
      
	img[np.isnan(img)] = 0.0
	img[img < 0.0] = 0.0
	img /= 2**16
	return img , timestamp
		
def FirstAnalysis(shape,l,X,Y):
	Image = np.zeros(shape)	
	for i in range(len(X)):
		Image = DrawCircle(Image,X[i],Y[i],l,shape)
		# Image = DrawSquare(Image,X[i],Y[i],l)

	
	return Image
		
def SecondAnalysis(Image,square,threshold):
	ImageCorrected = np.zeros(Image.shape)
	for i in range(Image.shape[0]):
		for j in range(Image.shape[1]):
			if np.sum(Image[int(i-square/2):int(i+square/2),int(j-square/2):int(j+square/2)] ) > threshold:
						ImageCorrected[i][j] = 255
	
	return ImageCorrected
       	
