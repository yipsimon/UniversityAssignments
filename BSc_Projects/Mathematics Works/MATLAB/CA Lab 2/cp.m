function f = cp(v,w)
    f = zeros(size(v));
    f(1) = v(2)*w(3)-w(2)*v(3);
    f(1) = w(1)*v(3)-v(1)*w(3);
    f(1) = v(1)*w(2)-w(1)*v(2);
end