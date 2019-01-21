function lsys = lsysprint( rule, start, no )
[f frep] = strtok(rule,':');
frep = strrep(frep,':','');
lsys = start;
for i=1:no
        disp(lsys);
        lsys = strrep(lsys, f, frep);     
end

end

