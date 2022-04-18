% load_grid - Load parts of a ROMS grid file
f = 'C:\crs\proj\2019_DorianOBX\COAWST_model\Christie_grid\NCoreBanks_sub9_labels.nc'

h = ncread(f,'labels');
x = ncread(f,'x_rho');
y = ncread(f,'y_rho');