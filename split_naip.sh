#gdal_translate -srcwin 2048 0 2048 2048 -b 1 -b 2 -b 3 -of JPEG m_2908513_se_16_1_20171110.tif naip1.jpg
#gdal_translate -srcwin 2500 2049 2048 2048 -b 1 -b 2 -b 3 -of JPEG m_2908513_se_16_1_20171110.tif naip2.jpg
#gdal_translate -srcwin 3200 5098 2048 2048 -b 1 -b 2 -b 3 -of JPEG m_2908513_se_16_1_20171110.tif naip3.jpg
gdal_translate -srcwin 3200 5098 1024 1024 -b 1 -b 2 -b 3 -of JPEG m_2908513_se_16_1_20171110.tif naip4.jpg
gdal_translate -srcwin 3200 4074 1024 1024 -b 1 -b 2 -b 3 -of JPEG m_2908513_se_16_1_20171110.tif naip3.jpg
