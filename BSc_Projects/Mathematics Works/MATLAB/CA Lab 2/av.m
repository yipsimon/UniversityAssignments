function e = av(v,w)
    e = acosd(dp(v,w)/(lv(v)*lv(w)));
end

function d = lv(v)
    d = sqrt(dp(v,v));
end

function c = dp(v,w)
    c = 0;
    for i = 1:length(v)
        c = c + v(i)*w(i);
    end
end