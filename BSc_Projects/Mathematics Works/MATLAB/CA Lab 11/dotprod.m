function res = dotprod(v1,v2)
res = 0;
    for i = 1:length(v1)
        res = res + v1(i)*v2(i);
    end
end
