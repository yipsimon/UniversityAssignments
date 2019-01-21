function v = beziermatrix()

figure
axis([0 10 0 10]);
[x y] = getpts();
spx = x(1);
spy = y(1);

c1px = x(2);
c1py = y(2);

c2px = x(3);
c2py = y(3);

epx = x(4);
epy = y(4);

hold on
plot(x,y,'*');

for i = 1:100
    t=i*0.01;
vec = [spx spy; c1px c1py; c2px c2py; epx epy];
basis = [ -1 3 -3 1; 3 -6 3 0; -3 3 0 0; 1 0 0 0];
tco = [t^3 t^2 t 1 ];

%[x,y] = getpoints(h);

a = tco * basis * vec;
curve(i,1)=a(1);
curve(i,2)=a(2);
end
plot(curve(:,1),curve(:,2), '--' );



end

