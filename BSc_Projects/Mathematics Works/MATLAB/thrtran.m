function v = thrtran(vec, tx,ty,tz)

temp = eye(4);
temp(1:3,end) = [tx;ty;tz];

v = temp*vec;