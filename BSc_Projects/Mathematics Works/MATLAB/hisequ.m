function ima = hisequ(image)
    h = imhist(image);
    csh = cumsum(h);
    csd = csh/csh(end);
    m = round(255*csd);
    ima = uint8(m(image+1));
end
    