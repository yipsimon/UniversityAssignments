function b = va(v,w)
    b = zeros(size(v));
    for i = 1:length(v)
        b(i) = v(i)+w(i);
    end
end