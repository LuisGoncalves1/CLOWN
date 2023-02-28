import cv2
import matplotlib.pyplot as plt
from Functions.CoordinateChange import PixelToAltaz, AltazToPixel
from Functions.Reader import ReadFile, ReadConfig, ReadCoordinates
from astropy.coordinates import EarthLocation, SkyCoord
import astropy.units as u
from astropy.time import Time
import numpy as np
import time
from astropy.io import fits

import sys

config_file = sys.argv[1]
AltAzFile = sys.argv[2]
XYFile = sys.argv[3]
l = int(sys.argv[4])


Alt, Az = ReadCoordinates(AltAzFile)
X, Y = ReadCoordinates(XYFile)


#------------------------------------------------------------------------------
information = ReadConfig(config_file)

location=EarthLocation(
        lat=information['LAT']*u.deg,
        lon=information['LON']*u.deg,
        height=information['height'] * u.m
    )
    
    
timestamp = Time('2021-04-01T00:46:18')
mapping = information['mapping']
focal = information['focal_length']
pixel_size = information['pixel_size']

coord = SkyCoord(
		alt=Alt*u.deg, #deg
		az=Az*u.deg, #rad 
		frame='altaz',
		location=location,
		obstime=timestamp)

#------------------------------__#



centro = [information['width']/2,information['height']/2]
tentativas = [(centro[0],centro[1])]
rotacao = 0

for a in range(0,l):
	for b in range(0,l):
		tentativas.append((centro[0]+a,centro[1]+b))
		tentativas.append((centro[0]+a,centro[1]-b))
		tentativas.append((centro[0]-a,centro[1]+b))
		tentativas.append((centro[0]-a,centro[1]-b))


Erros = []
for zenith in tentativas:
	Calculados = PixelToAltaz(X,Y,zenith,location,timestamp,rotacao,mapping,focal,pixel_size,information['reverse'])
	erro = np.sum(np.absolute(Alt-Calculados.alt.value))
	Erros.append(erro)


print('--------------------------------')
zenith = tentativas[Erros.index(min(Erros))]
print('zenith: ',zenith)
print('Average Error: ',min(Erros)/len(Erros))

Erros = []
for i in range(361):
	rotacao = i
	Calculados = PixelToAltaz(X,Y,zenith,location,timestamp,rotacao,mapping,focal,pixel_size,information['reverse'])
	erro = np.sum(np.absolute(Az-Calculados.az.value))
	Erros.append(erro)


rotacao = Erros.index(min(Erros))
print('phase: ',rotacao)
print('Average Error: ',min(Erros)/len(Erros))




X1,Y1 =  AltazToPixel(coord,zenith,rotacao,mapping,focal,pixel_size,information['reverse'])
Calculados = PixelToAltaz(X,Y,zenith,location,timestamp,rotacao,mapping,focal,pixel_size,information['reverse'])
Alt1 = Calculados.alt.value
Az1 = Calculados.az.value






# ~ Imagem = cv2.imread(image)
# ~ fig,axes = plt.subplots()
# ~ vmin = None
# ~ vmax = None
# ~ if test == 'PASO':
	# ~ A = fits.open(image)
	# ~ Imagem = A[0].data	
	# ~ axes.imshow(Imagem,cmap='gray',vmin=vmin or np.nanpercentile(Imagem, 0.1),vmax=vmax or np.nanpercentile(Imagem, 99))
# ~ elif test == 'LNA':
	# ~ Imagem = cv2.imread(image)
	# ~ axes.imshow(Imagem)
# ~ for contador in range(len(Y1)):
	# ~ c1 = plt.Circle((X1[contador],Y1[contador]),0.2, color = 'yellow', linewidth=2,fill=False)
	# ~ axes.add_patch(c1)

# ~ c1 = plt.Circle((zenith[0],zenith[1]),2, color = 'yellow', linewidth=2,fill=False)
# ~ axes.add_patch(c1)

# ~ plt.show()

