url='http://geoport.whoi.edu/thredds/dodsC/vortexfs1/usgs/Projects/dorian/dorian_032/dorian_his.ncml';
lon=ncread(url,'lon_rho');
lat=ncread(url,'lat_rho');
bt=ncread(url,'bed_thickness');
figure
pcolorjw(lon,lat,squeeze(bt(:,:,1,end)));
colormap('jet')
caxis([5 9])
colorbar
