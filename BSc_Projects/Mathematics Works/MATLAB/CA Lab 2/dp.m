function c = dp(v,w)
    c = 0;
    for i = 1:length(v)
        c = c + v(i)*w(i);
    end
end