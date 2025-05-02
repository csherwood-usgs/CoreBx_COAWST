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

### Plots for Warner Dorian paper  (revised May 2)

There continue to be lots of extraneous files.

Major changes associated with revisions to the paper:
* Attempts to split up big files and produce figures with files
* Improvments in multi-panel figures
* Correction of labelled sediment calculations
* Use of local versions of the concatenated `.his` files.

* Redo figure 2, panel c
* TODO - list figure changes

I was having problems pulling the big 4D datasets (like SSC) from THREDDS, so John W. used ncks to concatenate many (but not all) of the
 variables into one big `.his` file, which I downloaded to the Puget Systems Win10 desktop.

`ncrcat -v Hwave,Dwave,bath,bustr,bustrc,bustrw,bvstr,bvstrc,bvstrw,sandfrac_01,sandfrac_02,sandfrac_03,sandmass_01,sandmass_02,sandmass_03,u,v,ubar,vbar,sand_01,sand_02,sand_03  Dorian_NCB_his_000**.nc Dorian_NCB_his.nc`

Location on Poseidon: /proj/usgs-share/Projects/dorian/
#### THREDDS server; access via NCML
url_CSNV = 'http://geoport.whoi.edu/thredds/dodsC/vortexfs1/usgs/Projects/dorian/core_banks_jcw44/Output/dorian_his.ncml'  
url_CSYV = 'http://geoport.whoi.edu/thredds/dodsC/vortexfs1/usgs/Projects/dorian/core_banks_jcw45/Output/dorian_his.ncml'  
url_FSYV = 'http://geoport.whoi.edu/thredds/dodsC/vortexfs1/usgs/Projects/dorian/core_banks_jcw50/Output/dorian_his.ncml'  
url_FSNV = 'http://geoport.whoi.edu/thredds/dodsC/vortexfs1/usgs/Projects/dorian/core_banks_jcw51/Output/dorian_his.ncml'  

#### The local version does not have all of the variables
# The local version does not have all of the variables
url_CSNVc = 'D:/crs/src/CoreBx_COAWST/output/jcw44/Dorian_NCB_his.nc'  
url_CSYVc = 'D:/crs/src/CoreBx_COAWST/output/jcw45/Dorian_NCB_his.nc'  
url_FSYVc = 'D:/crs/src/CoreBx_COAWST/output/jcw50/Dorian_NCB_his.nc'  
url_FSNVc = 'D:/crs/src/CoreBx_COAWST/output/jcw51/Dorian_NCB_his.nc'  


   
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

`labels_to_ROMS_grid` - Interpolates landcover labels onto ROMS grid...only example is with older grid.  

#### Other stuff
`dems_to_ROMS_grid` - Adds canopy height TIFF to ROMS init.nc grid. Working with earlier Christy grid  

`create_composite_exp_files` - Make multi-band tiffs with various derivatives in bands (elevation, slope, veg. indices)  

`plot_observations` - Plots elev and elev diffs from TIFFS  

#### Files we dont need
`plot_model`  


#### Matlab files
`export_bbox.m` - Exports grid corners to CSV  
    
`load_grid.m` - Loads and old Christie grid  
