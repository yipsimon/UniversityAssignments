function vec = thrroty(v, ang)

temp = eye(4);
temp(1:3,1:3) = [cos(ang) 0 sin(ang); 0 1 0; -sin(ang) 0 cos(ang)];

vec = temp*v;