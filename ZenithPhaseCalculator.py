import cv2
import matplotlib.pyplot as plt
from Funcoes.MudancaCoordenadas import PixelParaAltaz, AltazParaPixel
from Funcoes.Reader import ReadFile
from astropy.coordinates import EarthLocation
import astropy.units as u
from astropy.time import Time
import numpy as np
from astropy.coordinates import SkyCoord
import time


# Coordinates of stars in pixels (X,Y) and AltAz, in the same order
# In this example we used :Sirius,Altinak,Alnilam,Mintaka,Rigel,Hadar,Rigil Kentaurus,Spica,Algorab,Gienah,y Hya, Kraz, Minkar

config_file = 'Config.txt'
image = 'ImagemA000.jpg' 


X =np.array([432,463.5,466.5,468.5,495,333,335,165,206,216.5,205,223.5,233])
Y =np.array([166,99.5,95.5,91.5,117.5,441.5,456,346,332,315.5,369,341,324])
Az = np.array([271.7959,282.916,283.1225,283.5336,273.1939,147.8886,148.2719,89.89292,91.20428,91.39333,103.2425,101.134,98.73917])
Alt = np.array([52.88247,32.75428,31.40958,30.06936,29.2325,28.90678,24.52286,30.91881,45.3345,48.84544,35.63539,45.73775,51.14686])







#------------------------------------------------------------------------------
information = ReadFile(config_file)


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
l = 40


#------------------------------------------------

tentativas = []
rotacao = 0

for a in range(0,l):
	for b in range(0,l):
		tentativas.append((centro[0]+a,centro[1]+b))



Erros = []
for zenith in tentativas:
	Calculados = PixelParaAltaz(X,Y,zenith,location,timestamp,rotacao,mapping,focal,pixel_size)
	erro = np.sum(np.absolute(Alt-Calculados.alt.value))
	Erros.append(erro)


print('--------------------------------')
zenith = tentativas[Erros.index(min(Erros))]
print('zenith: ',zenith)

Erros = []
for i in range(361):
	rotacao = i
	Calculados = PixelParaAltaz(X,Y,zenith,location,timestamp,rotacao,mapping,focal,pixel_size)
	erro = np.sum(np.absolute(Az-Calculados.az.value))
	Erros.append(erro)


rotacao = Erros.index(min(Erros))
print('phase: ',rotacao)


X1,Y1 =  AltazParaPixel(coord,zenith,rotacao,mapping,focal,pixel_size)



Imagem = cv2.imread(image)
fig,axes = plt.subplots()
axes.imshow(Imagem)
for contador in range(len(Y1)):
	c1 = plt.Circle((X1[contador],Y1[contador]),0.2, color = 'yellow', linewidth=2,fill=False)
	axes.add_patch(c1)

plt.show()

