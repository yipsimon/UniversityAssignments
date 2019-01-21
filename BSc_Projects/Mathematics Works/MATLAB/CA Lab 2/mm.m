function i = mm(m,n)
    [a b] = size(m);
    [c d] = size(n);
    for o = 1:a 
        for p = 1:d
            i(o,p) = dp(m(o,:),n(:,p));
        end
    end
end

function c = dp(v,w)
    c = 0;
    for i = 1:length(v)
        c = c + v(i)*w(i);
    end
end

