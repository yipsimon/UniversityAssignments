function v = lininterp()

figure
axis([0 10 0 10]);
[x y] = getpts();
sp = [x(1) y(1)];
ep = [x(2) y(2)];

hold on
plot(x,y,'*');

for i = 1:100
    t= i*0.01;
    p(i,1) = (1-t)*sp(1) + t*(ep(1));
    p(i,2) = (1-t)*sp(2) + t*(ep(2));
end

plot(p(:,1), p(:,2), '*-' );



end

