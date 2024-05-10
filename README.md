# CoreBx_COAWST
Routines used to manipulate input grids and plot results for North Core Banks COAWST model

#### Notes on coordinate conversion
* Converted lat/lon to 'island' coordinates in two steps:
```
from pyproj import Transformer
transformer = Transformer.from_crs( 'epsg:4326', 'epsg:26918',  ) # WGS84 to UTM18

utmx, utmy = transformer.transform( lat, lon )
xisl, yisl = UTM2Island(utmx, utmy, eoff=383520.0, noff=3860830.0, rot=42.0)
print('Shape of xisl, yisl: ', xisl.shape, yisl.shape)
```
(UTM2Island is in ncbx_funcs.py)  
* Offset was determined based on the averarge shoreline postion (z=0) between i=100:1200 in the final CSYV bathy.  
This ended up being index 168, or y = 329.28 in island coordinates.

### Plots for Warner Dorian paper
`sed_calcs` - Plots for (mostly) CSYV  

`vol_calcs` - Recreate John's Matlab volume-change calcs
  
  
`four_run_plots` - Plots from all four model simulations  
* Volume calcs...using pm and pn.  

    * 8-panel plot of final bathy and bathy change `'four_run_elevation_change`
    * Maps of labelled sed distribution `XXXX__labelled_sed_mass_diff`
    * Profiles of labelled sed and bathy `four_labelled_sed_profiles`  
    * Maps of elevation change for four cases `XXXX_elevation_change`  
    * Maps of waterlevels, waves, vectors `CSYV_vector_plotXX`
    * Max. stress plot (calcs of maxes take a whle) `


`plot_models_and_observations` - Only plots the obs and modeled topobathy, based on the earlier grid made with/by Christy  

#### Files we dont need
`plot_model`
`plot_observations`
    
