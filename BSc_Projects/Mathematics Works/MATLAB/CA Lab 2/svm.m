function a = svm(s,v)
    a = zeros(size(v));
    for i = 1:length(v)
        a(i) = s*v(i);
    end
end