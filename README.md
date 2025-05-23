# CoreBx_COAWST
Routines used to manipulate input grids and plot results for North Core Banks COAWST model
#### Grid info
N = s_rho = 8 levels (evenly spaced)  
grid is (1057, 1317)  
eta_rho (y) 1057  
xi_rho  (x) 1317

#### Resolution on the fine grid
Cross-shore resolution ranges from 100 m at the seaward end to 17 to 1.5 from most of the grid.
Alongshore resoluton is 1.5 m

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

#### Notes on SSC calcs
ssc (e.g., `sand01`,`sand02`, etc.) is kg/m3. These are summed, total SSC is kg/m3  
sscc = ssc * delz [kg/m2]  
sscu = ssc * delz * u [kg/m/s] - eastward flux in each layer  
sscv = ssc * delz * v [kg/m/s] - southward flux in each layer  
sscu_tot = vertical sum( sscu ) [kg/m/s]  
sscv_tot = vertical sum( sscv ) [kg/m/s]  
##### Net flux off island is:
oflux = sum(sscv_tot[shoreline, all alongshore]) * dely [kg/s]  
##### Convert to volume flux by dividing by bed density rho_bed
rho_bed = 0.65*2650 [kg/m3]  

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

#### Local version
Downloaded from Poseidon. The local version does not have all of the variables  
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
