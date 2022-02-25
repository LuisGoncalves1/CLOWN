from Funcoes.AnaliseImagem import read, StarFinder, find_matching_stars,CircularMask2
from Funcoes.MudancaCoordenadas import PixelToAltaz, AltazToPixel
from Funcoes.Catalogo import ReadCatalogue, Convert_Catalogue
from Funcoes.Reader import ReadConfig, ReadFile


from astropy.coordinates import EarthLocation
import astropy.units as u
import cv2
# ~ from skimage.color import rgb2gray

import matplotlib.pyplot as plt
import numpy as np

import time
from astropy.io import fits
import os


config_file = 'Config.txt'
Directory = 'Images/'
catalogue = 'Funcoes/Ficheiros/hipparcos.fits.gz'

def rgb2gray(rgb):
    dado = np.dot(rgb[...,:3], [0.2989, 0.5871, 0.1140])
    dado = dado.astype(int)
    return dado
    







#########################################################################################################################################################################################################################
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
mapping = 'equidistant'
	
images = os.listdir(Directory)
catalogue = ReadCatalogue(catalogue,max_magnitude = max_magnitude)		



for image in images:
	Image,timestamp = ReadFile(Directory,image)

	catalog_stars, magnitude = Convert_Catalogue(catalogue, timestamp, location, min_altitude=min_altitude)

	Y, X, R = StarFinder(Image,max_sigma=max_sigma,min_sigma=min_sigma,num_sigma=num_sigma,threshold=threshold)       # Estrelas Encontradas em Pixeis
	coord = PixelToAltaz(X,Y,zenith,location,timestamp,phase,mapping,focal,pixel_size)

	mask = coord.alt.deg > min_altitude
	idx,found = find_matching_stars(catalog_stars, coord[mask], max_sep=1.5 * u.deg)								  # Índice nos catalogos
	idx2,found2 = find_matching_stars(coord, catalog_stars, max_sep=1.5 * u.deg)									  # Índice nas encontradas 

	X2,Y2 = AltazToPixel(catalog_stars        ,zenith,phase,mapping,focal,pixel_size) # Estrelas Catalogo
	X3,Y3 = AltazToPixel(catalog_stars[found] ,zenith,phase,mapping,focal,pixel_size) # Estrelas Catalogo Encontradas
	X4,Y4 = AltazToPixel(catalog_stars[~found],zenith,phase,mapping,focal,pixel_size) # Estrelas Catalogo Não Encontradas


	Image2 = np.zeros(Image.shape)	
	l = 5
	raio = 300
	quadrado = 11
	minimo = 6* 255*l**2
	# Ve qual estao a menos no catalogo
	for i in range(len(X4)):
		if int(Y4[i])<= Image2.shape[0] and int(X4[i])<= Image2.shape[1]:# and Imagem2[int(Y4[i])][int(X4[i])] == 0:
			Image2[int(Y4[i])-l:int(Y4[i])+l,int(X4[i])-l:int(X4[i])+l] = 255
		
		
	Image3 = np.zeros(Image2.shape)
	for i in range(Image3.shape[0]):
		for j in range(Image3.shape[1]):
			if np.sqrt((i-zenith[1])**2+(j-zenith[0])**2) <= raio:		
				if np.sum( Image2[int(i-quadrado/2):int(i+quadrado/2),int(j-quadrado/2):int(j+quadrado/2)] ) > minimo:
						Image3[i][j] = 255
							
		
	vmin = None
	vmax = None
	fig,axes = plt.subplots(1,3)
	ax = axes.ravel()
	ax[0].imshow(Image,cmap='gray',vmin=vmin or np.nanpercentile(Image, 0.1),vmax=vmax or np.nanpercentile(Image, 99))
	ax[1].imshow(Image,cmap='gray',vmin=vmin or np.nanpercentile(Image, 0.1),vmax=vmax or np.nanpercentile(Image, 99))
	for contador in range(len(Y)):
			c1 = plt.Circle((X[contador],Y[contador]),0.4, color = 'green', linewidth=2,fill=False)
			ax[1].add_patch(c1)
			
	for contador in range(len(Y2)):
			c1 = plt.Circle((X2[contador],Y2[contador]),0.4, color = 'red', linewidth=2,fill=False)
			ax[0].add_patch(c1)
	
	ax[2].imshow(Image3,cmap='gray',vmin=vmin or np.nanpercentile(Image, 0.1),vmax=vmax or np.nanpercentile(Image, 99))
plt.show()
