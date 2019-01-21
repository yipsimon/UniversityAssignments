function res = matmult(m1,m2)

[n d1] = size(m1);
[d2 m] = size(m2);

if(d1~=d2)
      error('Matrix dimension don''t agree');
end
for i = 1:n
    for j = 1:m
            res(i,j) = dotprod(m1(i,:),m2(:,j));
    end
end

end
