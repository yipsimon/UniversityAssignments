function h = ma(m,n)
    h = zeros(size(m)); 
    [a b] = size(m);
    for i = 1:a 
        for j = 1:b 
            h(i,j) = m(i,j) + n(i,j);
        end
    end
end
  