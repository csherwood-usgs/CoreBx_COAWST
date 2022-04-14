% export a bounding box for grid
ulx = x(1,end)
uly = y(1,end)
urx = x(end,end)
ury = y(end,end)
llx = x(1,1)
lly = y(1,1)
lrx = x(end,1)
lry = y(end,1)
%%
figure(2); clf
plot(ulx,uly,'ok')
hold on
plot(urx,ury,'or')
plot(llx,lly,'og')
plot(lrx,lry,'om')
shg
%% Corners of the grid
fid = fopen('COAWST_corners.csv','w');
fprintf(fid,'%8.1f, %8.1f\n',ulx,uly);
fprintf(fid,'%8.1f, %8.1f\n',urx,ury);
fprintf(fid,'%8.1f, %8.1f\n',lrx,lry);
fprintf(fid,'%8.1f, %8.1f\n',llx,lly);
fprintf(fid,'%8.1f, %8.1f\n',ulx,uly);
fclose(fid);
%% Bounding box
fid = fopen('COAWST_bbox.csv','w');
fprintf(fid,'%8.1f, %8.1f\n',ulx,ury);
fprintf(fid,'%8.1f, %8.1f\n',lrx,ury);
fprintf(fid,'%8.1f, %8.1f\n',lrx,lly);
fprintf(fid,'%8.1f, %8.1f\n',ulx,lly);
fclose(fid);
%% GDAL coords (rounded to enclosing 10 m)
xstart = 10*(floor(ulx/10))
xend = 10*(ceil(lrx/10))
xn = xend-xstart
ystart = 10*(floor(lly/10))
yend = 10*(ceil(ury/10))
yn = yend-ystart