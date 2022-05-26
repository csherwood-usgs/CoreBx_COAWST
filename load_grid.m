% load_grid - Load parts of a ROMS grid file
% original version exported from Global Mapper with integer values
f = "C:\crs\proj\2019_DorianOBX\COAWST_model\Christie_grid\NCoreBanks_sub9_pre_post_veg.nc"
% corrected version done on laptop on 26 May 2022. Canopy elevations still
% need to be re-exported.
f2 = "C:\crs\proj\2019_DorianOBX\COAWST_model\Christie_grid\NCoreBanks_sub9_pre_post_vegv2.nc"

lon = ncread(f,"lon_rho");
lat = ncread(f,"lat_rho");
h = ncread(f,'h');
h_pre = ncread(f,'pre_Dorian_elev');
h_pst = ncread(f,'post_Dorian_elev');
h_prev2 = ncread(f2,'pre_Dorian_elev');
h_pstv2 = ncread(f2,'post_Dorian_elev');

x = ncread(f,'x_rho');
y = ncread(f,'y_rho');
%%
pcolor(h_pre)
shading interp

%%
plot(h_pre(600,:))
hold on
plot(h_prev2(600,:))