function v = thrdscal(vec, sx, sy, sz)

temp = diag(convhom([sx;sy;sz]));
v = temp*vec;