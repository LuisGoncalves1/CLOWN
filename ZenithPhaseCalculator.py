import cv2
import matplotlib.pyplot as plt
from Functions.CoordinateChange import PixelToAltaz, AltazToPixel
from Functions.Reader import ReadFile, ReadConfig
from astropy.coordinates import EarthLocation, SkyCoord
import astropy.units as u
from astropy.time import Time
import numpy as np
import time
from astropy.io import fits




# ~ test = 'LNA'
test = 'PASO'

l = 40


# LNA
if test == 'LNA':
	# Coordinates of stars in pixels (X,Y) and AltAz, in the same order
	# In this example we used :Sirius,Altinak,Alnilam,Mintaka,Rigel,Hadar,Rigil Kentaurus,Spica,Algorab,Gienah,y Hya, Kraz, Minkar
	image = 'Images/2021-03-31T23:46:18.jpg' 
	config_file = 'Config.txt'
	X =np.array([432,463.5,466.5,468.5,495,333,335,165,206,216.5,205,223.5,233])
	Y =np.array([166,99.5,95.5,91.5,117.5,441.5,456,346,332,315.5,369,341,324])
	Az = np.array([271.7959,282.916,283.1225,283.5336,273.1939,147.8886,148.2719,89.89292,91.20428,91.39333,103.2425,101.134,98.73917])
	Alt = np.array([52.88247,32.75428,31.40958,30.06936,29.2325,28.90678,24.52286,30.91881,45.3345,48.84544,35.63539,45.73775,51.14686])
elif test == 'PASO':
	image = 'Images/2022-07-15T23-57-39-630.fit'
	config_file = 'ConfigPASO.txt'
	X = np.array([714,
	717,
	725,
	736,
	635,
	612.5,
	606,
	615.5,
	544,
	563,
	500,
	489,
	450,
	482,
	516,
	419,
	408,
	389,
	766.5,
	783.5,
	745
	])

	Y = np.array([568.5,
	578,
	569,
	574,
	601.4,
	593,
	608,
	626,
	621,
	655,
	675.5,
	690,
	352,
	401,
	441,
	545,
	586,
	602,
	697.5,
	664.5,
	677
	])

	Az = np.array([98.16767,
	89.80158,
	102.9794,
	102.8306,
	356.7273,
	339.2635,
	344.8003,
	356.5159,
	333.3094,
	347.9598,
	340.5381,
	341.7483,
	263.4436,
	267.2714,
	271.3178,
	303.655,
	312.4067,
	315.0956,
	66.48333,
	78.035,
	63.43056
	])

	Alt = np.array([82.84183,
	81.59297,
	81.02292,
	78.96236,
	78.67781,
	76.83325,
	74.29803,
	73.27672,
	64.11964,
	63.43694,
	52.73164,
	49.634,
	37.83167,
	47.83056,
	56.55806,
	45.53333,
	43.2,
	39.33694,
	60.3425,
	63.14278,
	65.18611
	])







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






Imagem = cv2.imread(image)



fig,axes = plt.subplots()
vmin = None
vmax = None
if test == 'PASO':
	A = fits.open(image)
	Imagem = A[0].data	
	axes.imshow(Imagem,cmap='gray',vmin=vmin or np.nanpercentile(Imagem, 0.1),vmax=vmax or np.nanpercentile(Imagem, 99))
elif test == 'LNA':
	Imagem = cv2.imread(image)
	axes.imshow(Imagem)
for contador in range(len(Y1)):
	c1 = plt.Circle((X1[contador],Y1[contador]),0.2, color = 'yellow', linewidth=2,fill=False)
	axes.add_patch(c1)

c1 = plt.Circle((zenith[0],zenith[1]),2, color = 'yellow', linewidth=2,fill=False)
axes.add_patch(c1)

plt.show()

