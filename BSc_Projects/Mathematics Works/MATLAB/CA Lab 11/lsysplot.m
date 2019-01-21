function lsysplot(lsys, angle)

dir = [1;0;1];
pos = [0;0;1];
figure
hold on
save = 0;
savepointp = eye(3);
savepointd = eye(3);
for i = 1:length(lsys)
    oldpos = pos;
    switch lsys(i)
        case 'F'
            pos = pos + dir;
            plot([oldpos(1) pos(1)],[oldpos(2) pos(2)]);
        case 'f'
            pos = pos + dir;
        case '+'
            dir = rot2d(dir,angle);
        case '-'
            dir = rot2d(dir,-angle);
        case '['
            save = save + 1;
            savepointp(:,save) = pos;
            savepointd(:,save) = dir;
        case ']'
            pos = savepointp(:,save);
            dir = savepointd(:,save);
            save = save - 1;
    end
end

end 