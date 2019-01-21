function res = rot2d(v,ang)

tmat = eye(3);
tmat(1:2,1:2) = [cosd(ang) -sind(ang); sind(ang) cosd(ang)];
res = matmult(tmat,v);

end