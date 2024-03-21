import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord, Angle
from .mapping_functions import mapping_functions, inverse_mapping_functions



def PixelToPolar(X, Y,zenith,reverse): 
	dx = X - zenith[0]
	dy = Y - zenith[1]
	if reverse:
		dx = -dx
	
	r = np.sqrt(dx**2 + dy**2)
	phi = np.pi - np.arctan2(-dx, dy)
	
	mask = phi== 2*np.pi
	phi[mask] = 0
	return r, phi * u.rad  # angulo em radianos, distancia em pixeis

def PolarToPixel(r,phi,zenith,reverse):
	if reverse:
		X = zenith[0] - r * np.sin(-phi)
	else:
		X = zenith[0] + r * np.sin(-phi)
		
	Y = zenith[1] - r * np.cos(-phi)	
	return X,Y

def PixelToAltaz(X,Y,zenith,location,time,phase,mapping,focal,pixel_size,reverse):
	r , azimuth = PixelToPolar(X, Y,zenith,reverse) # distancia ao centro e angulo ( que é o azimuth )	
	azimuth -= phase *u.deg # Corrigir a rotacao da imagem, para o Norte ficar na vertical
	
	altitude = inverse_mapping_functions[mapping](r*pixel_size,focal) #Transformar a distancia do centro ao ponto para o ângulo
	altitude = Angle('90d') - altitude #Mudar a origem do angulo
	altitude[altitude.deg < 0] = Angle('0d') #Corrigir angulos menores que 0
	altitude[altitude.deg > 90] = Angle('90d') #Corrigir angulos maiores que 90

	return SkyCoord(
		alt=altitude, #deg
		az=azimuth, #rad 
		frame='altaz',
		location=location,
		obstime=time)

def AltazToPixel(coord,zenith,rotacao,mapping,focal,tamanho_pixel,reverse):
	phi = coord.az + rotacao *u.deg #deg
	
	altitude = Angle('90d') - coord.alt #deg
	
	distancia = mapping_functions[mapping](altitude,focal)/tamanho_pixel
	# ~ distancia = distancia.value
	
	X,Y = PolarToPixel(distancia,phi,zenith,reverse)
	return X,Y


