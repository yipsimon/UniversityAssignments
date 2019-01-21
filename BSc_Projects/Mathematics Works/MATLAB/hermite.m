function v = hermite()

figure
axis([0 10 0 10]);
[x y] = getpts();
sp = [x(1) y(1)];
ep = [x(2) y(2)];
c1 = [x(3) y(3)];
c2 = [x(4) y(4)];

t1 = c1 - sp;
t2 = c2 - ep;

hold on
plot(x,y,'*');

for i = 1:20
    t = i*0.05;
    vec = [sp(1) sp(2); ep(1) ep(2); t1(1) t1(2); t2(1) t2(2)];
    basis = [2 -2 1 1; -3 3 -2 -1; 0 0 1 0; 1 0 0 0];
    tco = [t^3 t^2 t 1 ];
    a = tco * basis * vec;
    curve(i,1)=a(1);
    curve(i,2)=a(2);
end
plot(curve(:,1),curve(:,2), '--' );

end
