import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
import pickle
from matplotlib import cm
from datetime import datetime
from pyproj import Transformer

def pcoord(x, y):
    """
    Convert x, y to polar coordinates r, az (geographic convention)
    r,az = pcoord(x, y)
    """
    r = np.sqrt(x**2 + y**2)
    az = np.degrees(np.arctan2(x, y))
    # az[where(az<0.)[0]] += 360.
    az = (az+360.)%360.
    return r, az


def xycoord(r, az):
    """
    Convert r, az [degrees, geographic convention] to rectangular coordinates
    x,y = xycoord(r, az)
    """
    x = r * np.sin(np.radians(az))
    y = r * np.cos(np.radians(az))
    return x, y


def UTM2Island(eutm, nutm, eoff=383520.0, noff=3860830.0, rot=42.0):
    """
    Convert UTM NAD83 Zone 18N easting, northing to N. Core Banks alongshore, cross-shore coordinates
    xisl, yisl = UTM2Island( eutm, nutm )
    Better to use values from the dict than defaults for translation/rotation values
    Defaults are associated with the dict read in from `small_island_box.yml`
    """
    [r, az] = pcoord(eutm-eoff, nutm-noff)
    az = az + rot
    [xisl,yisl] = xycoord(r,az)
    return xisl, yisl


def island2UTM(alongshore, across_shore, eoff=383520.0, noff=3860830.0, rot=42.):
    """Convert island coordinates to UTM
       Inverse of UTM2Island()
       Better to use values from the dict than defaults for translation/rotation values
       Defaults are associated with the dict read in from `small_island_box.yml`
       Here is code for UTM2island:
          [r, az] = pcoord(eutm-eoff, nutm-noff)
          az = az + rot
          [xisl,yisl] = xycoord(r,az)
    """
    r, az = pcoord(alongshore, across_shore)
    az = az - rot
    eUTM, nUTM = xycoord(r, az)
    eUTM = eUTM + eoff
    nUTM = nUTM + noff
    return eUTM, nUTM

def stat_summary(x, iprint=False):
    n = len(x)
    nnan = np.sum(np.isnan(x))
    nvalid = n-nnan
    # intitialize with NaNs

    if n > nnan:
        meanx = np.nanmean(x)
        stdx = np.nanstd(x)
        minx = np.nanmin(x)
        d5 = np.nanpercentile(x, 5.)
        d25 = np.nanpercentile(x, 25.)
        d50 = np.nanpercentile(x, 50.)
        d75 = np.nanpercentile(x, 75.)
        d95 = np.nanpercentile(x, 95.)
        maxx = np.nanmax(x)
    else:
        meanx = np.nan
        stdx = np.nan
        minx = np.nan
        d5 = np.nan
        d25 = np.nan
        d50 = np.nan
        d75 = np.nan
        d95 = np.nan
        maxx = np.nan

    # return it in a dict
    s = {'n':n, 'nnan':nnan, 'nvalid':nvalid, 'mean':meanx, 'std':stdx, 'min':minx, 'max':maxx,
         'd5':d5, 'd25':d25, 'd50':d50, 'd75':d75, 'd95':d95}
    # if iprint:
    #     for key, value in s.items():
    #         print('{:6s} = {:.3f}'.format(key, value)),
    if iprint:
        print("  n, nnan, nvalid: ",s['n'],s['nnan'],s['nvalid'])
        print("  mean, std, min, max   : {:.3f} {:.3f} {:.3f} {:.3f}"
            .format(s['mean'], s['std'], s['min'], s['max']))
        print("  d5, d25, d50, d75, d95: {:.3f} {:.3f} {:.3f} {:.3f} {:.3f}"
            .format(s['d5'], s['d25'], s['d50'], s['d75'], s['d95']))

    return s

def running_mean(y, npts):
    '''
    Smooth a 1-d array with a moving average
    https://stackoverflow.com/questions/20618804/how-to-smooth-a-curve-in-the-right-way

    Input:
        y - 1-d array
        npts - number of points to average
    Returns:
        ys - smoothed arrays
    '''
    box = np.ones(npts)/npts
    ys = np.convolve(y, box, mode='same')
    return ys

def mask_array( x, wdm ):
    s = wdm.shape
    wdmr = np.ravel(wdm)
    xr = np.ravel(x)
    xr[np.where(wdmr==0)]=np.nan
    xm = np.reshape( xr, s )
    return xm

def nan_array_low( x, val=0.1 ):
    s = x.shape
    xr = np.ravel(x)
    xr[np.where(xr<=val)]=np.nan
    xm = np.reshape( xr, s )
    return xm

def despeckle( x, iks = 3 ):
    # despeckle like this? This expands the NaN regions with a 3x3 matrix
    ks = np.ones((iks, iks)) / (iks*iks)
    xs = convolve(x,ks,mode='nearest')
    return xs

# These next two routines are from ChatGPT....not totally sure they are trustworthy

def set_depth(h, zeta, hc, N, Vtransform, Vstretching, theta_s, theta_b, grid='rho'):
    """
    Calculates z_rho (center of depth layers, N=N)
    """
    # Prevent division by zero and handle theta_s = 0
    theta_s_safe = np.maximum(theta_s, 1e-10)  # Ensure theta_s is not zero
    sc = (np.arange(1, N + 1) - N - 0.5) / N if grid == 'rho' else np.arange(0, N + 1) / N - 1

    # Handle Cs calculation more carefully to avoid NaN/Inf issues
    Cs = (1 - theta_b) * np.sinh(theta_s_safe * sc) / np.sinh(theta_s_safe) + \
         theta_b * (np.tanh(theta_s_safe * (sc + 0.5)) - np.tanh(theta_s_safe / 2)) / (2 * np.tanh(theta_s_safe / 2))

    # Ensure no invalid values propagate
    if np.any(np.isnan(Cs)) or np.any(np.isinf(Cs)):
        print("Warning: NaN or Inf values in Cs. Adjusting.")
        Cs = np.nan_to_num(Cs, nan=0.0, posinf=0.0, neginf=0.0)

    if Vtransform == 1:
        z = sc[:, np.newaxis, np.newaxis] * hc + Cs[:, np.newaxis, np.newaxis] * h
        z = z + zeta[np.newaxis, :, :] * (1 + z / h)
    elif Vtransform == 2:
        z = (hc * sc[:, np.newaxis, np.newaxis] + Cs[:, np.newaxis, np.newaxis] * h) / \
            (hc + h)
        z = zeta[np.newaxis, :, :] + (zeta[np.newaxis, :, :] + h) * z
    else:
        raise ValueError("Unsupported Vtransform version")

    return z


def set_depth_w(h, zeta, hc, N, Vtransform, Vstretching, theta_s, theta_b):
    """
    Calculate depths at layer interfaces (w-points), size N+1.
    """
    sc = np.arange(0, N + 1) / N - 1  # w-levels from -1 to 0
    theta_s_safe = np.maximum(theta_s, 1e-10)

    Cs = (1 - theta_b) * np.sinh(theta_s_safe * sc) / np.sinh(theta_s_safe) + \
         theta_b * (np.tanh(theta_s_safe * (sc + 0.5)) - np.tanh(theta_s_safe / 2)) / \
         (2 * np.tanh(theta_s_safe / 2))

    if Vtransform == 1:
        z = sc[:, np.newaxis, np.newaxis] * hc + Cs[:, np.newaxis, np.newaxis] * h
        z = z + zeta[np.newaxis, :, :] * (1 + z / h)
    elif Vtransform == 2:
        z = (hc * sc[:, np.newaxis, np.newaxis] + Cs[:, np.newaxis, np.newaxis] * h) / (hc + h)
        z = zeta[np.newaxis, :, :] + (zeta[np.newaxis, :, :] + h) * z
    else:
        raise ValueError("Unsupported Vtransform version")
    return z  # shape: (N+1, eta, xi)


# load the grid from CSYV and convert to island coordinates
url_CSNV = 'http://geoport.whoi.edu/thredds/dodsC/vortexfs1/usgs/Projects/dorian/core_banks_jcw44/Output/dorian_his.ncml'
url_CSYV = 'http://geoport.whoi.edu/thredds/dodsC/vortexfs1/usgs/Projects/dorian/core_banks_jcw45/Output/dorian_his.ncml'
url_FSYV = 'http://geoport.whoi.edu/thredds/dodsC/vortexfs1/usgs/Projects/dorian/core_banks_jcw50/Output/dorian_his.ncml'
url_FSNV = 'http://geoport.whoi.edu/thredds/dodsC/vortexfs1/usgs/Projects/dorian/core_banks_jcw51/Output/dorian_his.ncml'

# The local version does not have all of the variables
url_CSNVc = 'D:/crs/src/CoreBx_COAWST/output/jcw44/Dorian_NCB_his.nc'
url_CSYVc = 'D:/crs/src/CoreBx_COAWST/output/jcw45/Dorian_NCB_his.nc'
url_FSYVc = 'D:/crs/src/CoreBx_COAWST/output/jcw50/Dorian_NCB_his.nc'
url_FSNVc = 'D:/crs/src/CoreBx_COAWST/output/jcw51/Dorian_NCB_his.nc'

# load main case
ds_CSYV = xr.open_dataset(url_CSYV) 

# load lat/lon, convert to island coordinates
lon = np.squeeze( ds_CSYV.lon_rho.load().values )
lat = np.squeeze( ds_CSYV.lat_rho.load().values )

# Convert lat/lon to UTM zone 18N, and then to island coordinates
transformer = Transformer.from_crs( 'epsg:4326', 'epsg:26918',  ) # WGS84 to UTM18
utmx, utmy = transformer.transform( lat, lon )
xisl, yisl = UTM2Island(utmx, utmy, eoff=383520.0, noff=3860830.0, rot=42.0)
print('Shape of xisl, yisl: ', xisl.shape, yisl.shape)

# Calculate area of each cell
pn = np.squeeze( ds_CSYV.pn.load().values )
pm = np.squeeze( ds_CSYV.pm.load().values )
area = (1./pn * 1./pm )

t=ds_CSYV.ocean_time.load()
tstring = pd.to_datetime(t).strftime('%Y-%m-%d %H:%M')

# Use a central line for cross-shore distance
y = np.squeeze( yisl[:,550] )

# load initial and final bathymetry
# Minus sign converts from depth to elevation
bathi = -ds_CSYV.bath[1,:,:].load().values
bathf_CSYV = -ds_CSYV.bath[-1,:,:].load().values

# find the average initial shoreline location
mbathi = np.mean(bathi[:,100:1200], axis=1)

ishorey = np.argwhere(mbathi>=0.)[0]
print('Index of shoreline and y-location:')
print(ishorey, y[ishorey])
dy_offshore = y[ishorey]-y[0]
dy_onshore = y[-1]-y[ishorey]
print('Offshore model domain (dy_offshore): ',dy_offshore,', onshore (dy_onshore): ',dy_onshore)

# use this for the cross-shore location by adding the offset
offset = y[ishorey]
y = y-offset
yisl = yisl-offset
xisl = xisl-np.min(xisl[ishorey])
# make the alongshore coordinates
x = np.squeeze( xisl[ishorey] - np.min(xisl[ishorey]) )

# extract parameters needed for depth
#Hz=set_depth(Vtransform, Vstretching, theta_s, theta_b, hc, N, igrid, h, zeta, report)
#Hz=set_depth(2, 4, 0, 0, 0, 8, 1, h, zeta, 1
theta_s = ds_CSYV['theta_s'].values.item()
theta_b = ds_CSYV['theta_b'].values.item()
hc = ds_CSYV['hc'].values.item()
Vtransform = ds_CSYV['Vtransform'].values.item()
Vstretching = ds_CSYV['Vstretching'].values.item()
