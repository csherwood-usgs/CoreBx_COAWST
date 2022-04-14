### Notes on processing COAWST simulation on N. Core Banks
#### Make sure GDAL is installed in the Python environment  
> mamba install gdal

#### Options for extracting jpegs from tiff
* Global Mapper - draw box, export that region with tiles
* GDAL without tiling (must specify bands)
gdal_translate -srcwin 3200 5098 1024 1024 -b 1 -b 2 -b 3 -of JPEG m_2908513_se_16_1_20171110.tif naip4.jpg
gdal_translate -srcwin 3200 4074 1024 1024 -b 1 -b 2 -b 3 -of JPEG m_2908513_se_16_1_20171110.tif naip3.jpg

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
