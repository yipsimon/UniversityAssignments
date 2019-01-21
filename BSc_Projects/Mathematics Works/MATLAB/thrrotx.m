function vec = thrrotx(v, ang)

temp = eye(4);
temp(2:3,2:3) = [cos(ang) -sin(ang); sin(ang) cos(ang)];

vec = temp*v;