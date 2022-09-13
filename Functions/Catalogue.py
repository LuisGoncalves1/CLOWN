from astropy.coordinates import SkyCoord, AltAz
import numpy as np
from astropy.table import Table
from pkg_resources import resource_filename
from functools import lru_cache

# ~ catalog_path = resource_filename('all_sky_cloud_detection', 'resources/hipparcos.fits.gz')

@lru_cache(maxsize=10)
def ReadCatalogue(catalog_path,max_magnitude=None,min_magnitude=None,max_variability=None):
    catalog = Table.read(catalog_path)
    mask = np.isfinite(catalog['ra']) & np.isfinite(catalog['dec'])
    catalog = catalog[mask]

    if max_magnitude is not None:
        catalog = catalog[catalog['v_mag'] <= max_magnitude]
        
    if min_magnitude is not None:
        catalog = catalog[catalog['v_mag'] >= min_magnitude]

    if max_variability is not None:
        catalog = catalog[catalog['variability'] == max_variability]

    return catalog

def Convert_Catalogue(catalog, time, location, min_altitude=20):

    stars = SkyCoord(ra=catalog['ra'], dec=catalog['dec'], frame='icrs')
    stars_altaz = stars.transform_to(AltAz(obstime=time, location=location))

    visible = stars_altaz.alt.deg > min_altitude
    stars_altaz = stars_altaz[visible]
    magnitude = catalog['v_mag'][visible]

    return stars_altaz, magnitude
