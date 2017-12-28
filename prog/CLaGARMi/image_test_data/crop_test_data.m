
o=v.o;
x=[1 2 3 4 5  51 52 53 54 55 101 102 103 104 105]; 
ox=o(:,1:30,x);

v.o=ox;

save('Rain_l15_y30','v')
save('Tmax_l15_y30','v')
save('Tmin_l15_y30','v')
