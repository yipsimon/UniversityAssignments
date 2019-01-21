function tristripplot(tv)

for i = 3:size(tv,2) 
    tri(:,:,i-2) = [tv(:,i-2) tv(:,i-1) tv(:,i) tv(:,i-2)]
end

% now plot it
figure
hold on;
for i=1:size(tri,3)
    plot3(tri(1,:,i), tri(2,:,i), tri(3,:,i));
end
axis([-1 3 -1 3 -1 3]);
view(3);