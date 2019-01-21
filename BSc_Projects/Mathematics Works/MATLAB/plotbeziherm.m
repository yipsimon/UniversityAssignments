function v = plotbeziherm()

figure
axis([0 10 0 10]);

bbasis = [ -1 3 -3 1; 3 -6 3 0; -3 3 0 0; 1 0 0 0];
hbasis = [2 -2 1 1; -3 3 -2 -1; 0 0 1 0; 1 0 0 0];



for i = 1:100
    t = i*0.01;
    tco = [t^3 t^2 t 1 ];
    a = tco * bbasis;
    b = tco * hbasis;
    bcurve(i,1)= a(1);
    bcurve(i,2)= a(2);
    bcurve(i,3)= a(3);
    bcurve(i,4)= a(4);
    hcurve(i,1)= b(1);
    hcurve(i,2)= b(2);
    hcurve(i,3)= b(3);
    hcurve(i,4)= b(4);
end
x = [0:0.01:1];
plot(x,bcurve(:,1), '--' );
end

