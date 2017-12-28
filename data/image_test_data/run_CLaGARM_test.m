load image_test_data\Tmin_l163_y65_22x15.mat 
mv(1)=v;
load image_test_data\Tmax_l163_y65_22x15.mat
mv(2)=v;
load image_test_data\Rain_l152_y65_22x15.mat
mv(3)=v;
clear v
validateInputData(mv);
tic
split=1;
savefilename='out_image_test';
hashfilename='hash_image_test';
savefilename = strcat(savefilename,int2str(split));
hashfilename = strcat(hashfilename,int2str(split));
rng default
mv=CLaGARM_nohash(1000,12,mv,hashfilename);
disp('Saving...');
save(savefilename,'mv','-v7.3');
toc
