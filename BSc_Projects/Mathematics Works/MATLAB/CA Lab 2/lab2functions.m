function fh = lab2functions
fh = localfunctions;
end

function a = svm1(s,v)
    [m,n] = size(v);
    for i = 1:n
        for j = 1:m
            v(j,i) = s*v(j,i);
        end
    end
    a = v;
end

