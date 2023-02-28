from Functions.CoordinateChange import PixelToAltaz, AltazToPixel
from Functions.Reader import ReadConfig, ReadCoordinates
from astropy.coordinates import EarthLocation, SkyCoord, AltAz
import astropy.units as u
import cv2
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

'''
Examples:
To run code type in CheckPoint.py directory: python CheckPoint.py configFile Mask Ra Dec
No Cloud: python3 CheckPoint.py ConfigPASO.txt -2022-08-24T02-39-08-106.jpg 70 50

Cloud:    python3 CheckPoint.py ConfigPASO.txt -2022-08-24T02-39-08-106.jpg 100 50
'''

# ~ '/home/luis/Desktop/Codigos/CLOWN/Cloud Masks/PASO/-2022-08-24T02-39-08-106.jpg 70 50'



config_file = sys.argv[1]
Mask = sys.argv[2]

try:
	sys.argv[4]
	try:
		Ra = []
		Ra.append(float(sys.argv[3]))
	except:
		raise Exception('The provided Ra is not a number')
		
	try:
		Dec = []
		Dec.append(float(sys.argv[4]))
	except:
		raise Exception('The provided Dec is not a number')
except:
	RaDecFile = sys.argv[3]
	Ra, Dec = ReadCoordinates(RaDecFile)


#########################################################################################################################################################################################################################
def rgb2gray(rgb):
    dado = np.dot(rgb[...,:3], [0.2989, 0.5871, 0.1140])
    dado = dado.astype(int)
    return dado

ClownDirectory = os.getcwd()
information = ReadConfig(config_file)
zenith = (information['zenith_X'],information['zenith_Y'])
phase = information['phase']
location=EarthLocation(
        lat=information['LAT']*u.deg,
        lon=information['LON']*u.deg,
        height=information['height'] * u.m
    )
focal = information['focal_length']
pixel_size = information['pixel_size']
mapping = information['mapping']
precision = float(information['precision'])
reverse = information['reverse']
DRa = float(information['RaDelta'])
DDec = float(information['DecDelta'])
UTC = information['UTC']

# Ler Mascara
Image = cv2.imread(f"{ClownDirectory}/CloudMasks/{information['ImageFolder']}/{Mask}",cv2.IMREAD_GRAYSCALE)
if information['GRAPH']:
		fig,axes = plt.subplots(1,2)
		ax = axes.ravel()
		ax[0].imshow(Image,cmap='gray')
		ax[1].imshow(Image,cmap='gray')

timestamp = Mask.split('/')[-1][1:20]
timestamp = list(timestamp)
timestamp[13] = ':'
timestamp[16] = ':'
timestamp = "".join(timestamp)

date_format_str = '%Y-%m-%dT%H:%M:%S'
timestamp = datetime.strptime(timestamp, date_format_str)
timestamp = timestamp - timedelta(hours=UTC)



n=30
visible = []
for l in range(len(Ra)):
	RaValues = []
	DecValues = []
	Decs = np.linspace(Dec[l]-DDec/2,Dec[l]+DDec/2,n)
	for k in range(len(Decs)):	
		dec = Decs[k]
		dRa = DRa/np.cos(np.pi*dec/180)
		for i in np.linspace(-dRa/2,dRa/2,n):
			RaValues.append(Ra[l]+i)
			DecValues.append(dec)

	coordinate_RaDec = SkyCoord(ra=np.array(RaValues)*u.deg, dec=np.array(DecValues)*u.deg, frame='icrs')
	coordinate_AltAz = coordinate_RaDec.transform_to(AltAz(obstime=timestamp, location=location))
	X,Y = AltazToPixel(coordinate_AltAz,zenith,phase,mapping,focal,pixel_size, reverse = reverse)
	X,Y = X.astype(int),Y.astype(int)

	value = sum(Image[Y,X])
	visible.append(False)
	if value == 0:
		visible[l] = True

	if information['GRAPH']:
		for contador in range(len(Y)):
			if visible[l]:
				color = 'green'
			else:
				color = 'red'	
			c1 = plt.Circle((X[contador],Y[contador]),0.4, color = color, linewidth=2,fill=False)
			ax[1].add_patch(c1)

print(visible)
if information['GRAPH']:
	plt.show()
