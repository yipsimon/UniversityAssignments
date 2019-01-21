function vec = thrrotz(v, ang)

temp = eye(4);
temp(1:2,1:2) = [cos(ang) -sin(ang); sin(ang) cos(ang)];

vec = temp*v;