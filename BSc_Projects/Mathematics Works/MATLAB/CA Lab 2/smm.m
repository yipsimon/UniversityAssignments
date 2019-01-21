function g = smm(s,m)
    [a b]= size(m);
    g = zeros(size(m));
    for i = 1:a
        for j = 1:b
            g(i,j) = a*m(i,j);
        end
    end
end