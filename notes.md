### Notes on processing COAWST simulation on N. Core Banks
#### Make sure GDAL is installed in the Python environment  
> mamba install gdal

#### Options for extracting jpegs from tiff
* Global Mapper - draw box, export that region with tiles
* GDAL without tiling (must specify bands)
gdal_translate -srcwin 3200 5098 1024 1024 -b 1 -b 2 -b 3 -of JPEG m_2908513_se_16_1_20171110.tif naip4.jpg
gdal_translate -srcwin 3200 4074 1024 1024 -b 1 -b 2 -b 3 -of JPEG m_2908513_se_16_1_20171110.tif naip3.jpg

#### However, I did it by exporting from Global Mapper in 4 x 4 tiles.

#### Metadata for larger export box
FILENAME=
DESCRIPTION=
AREA COUNT=1
AREA VERTEX COUNT=5
LINE COUNT=0
POINT COUNT=0
MESH COUNT=0
UPPER LEFT X=393024.235
UPPER LEFT Y=3872654.234
LOWER RIGHT X=395649.131
LOWER RIGHT Y=3870034.481
WEST LONGITUDE=-76.17215697
NORTH LATITUDE=34.99110912
EAST LONGITUDE=-76.14307227
SOUTH LATITUDE=34.96721627
UL CORNER LONGITUDE=-76.17215697
UL CORNER LATITUDE=34.99083486
UR CORNER LONGITUDE=-76.14340057
UR CORNER LATITUDE=34.99110912
LR CORNER LONGITUDE=-76.14307227
LR CORNER LATITUDE=34.96749029
LL CORNER LONGITUDE=-76.17182043
LL CORNER LATITUDE=34.96721627
PROJ_DESC=UTM Zone 18 / NAD83_NSRS / meters
PROJ_DATUM=NAD83 (NSRS2011)
PROJ_UNITS=meters
EPSG_CODE=EPSG:6347
BBOX AREA=6.877 sq km
CODE_PAGE=0 (Default (Current System Language))

#### To pull maps out of larger DEM with gdal_translate  
> gdal_translate -of gtiff -projwin 393030. 3872660. 395650. 3870030.

#### Split large .tiff files into smaller .jpeg tiles
Two options:  
1 Global Mapper: Draw an ROI to export. Select the ROI and the data layer. Choose \layer\export and select tile and ROI options from the menus.  
2 Use gdal_translate

#### Run Doodler
* Move the .jpg images to ..\dash_doodler\assets\
* Clean out ..\dash_doodler\assets\
* Edit ..\dash_doodler\classes.txt
* ? What does `clear_doodler_cache.py` do?
* Run doodler:
> cd ..\dash_doodler  
> python doodler.py  

* Open a browser page to `http://127.0.0.1:8050/` to doddle
* Results will be in folders in ..\dash_doodler\results  
#### Process results  
> cd ..\dash_doodler\utils\
> python gen_images_and_labels.py

  [Select dated output folder from GUI. GUI might show lower-level folder with previous results...navigate up a level and choose correct folder.]  

To recombine:  
`gdal_translate [source].vrt [target]`  
If [target] is a .jgp file, a file called '.jpg.aux.xml' will be created.  
You can used code
