function colourhist(img)

   bins = 8;
   binwidth = 256/8; 
   Hist = zeros(bins,bins,bins);
   
   [hei wid dim] = size(img);
   
   data = reshape(img, hei*wid, dim);
   
   pix = floor(double(data)/binwidth)+1;
   
   for i=1:size(pix)
      Hist(pix(i,1),pix(i,2),pix(i,3)) = Hist(pix(i,1),pix(i,2),pix(i,3))+1;
   end
   
   Hist = Hist / sum(sum(sum(Hist)))
   
   histogram(Hist,binwidth)
   
   
end