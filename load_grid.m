% load_grid - Load parts of a ROMS grid file
f = "NCoreBanks_sub9.nc"
lon = ncload(f,"lon_rho");
lat = ncread(f,"lat_rho");
h = ncread(f,'h');
x = ncread(f,'x_rho');
y = ncread(f,'y_rho');