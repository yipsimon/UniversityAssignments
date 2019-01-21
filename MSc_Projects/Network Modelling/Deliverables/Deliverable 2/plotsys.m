function plotsys()
%The three data values to be used
alpha1 = 0.35;
alpha2 = 0.45;
alpha3 = 0.55;
%Data storing
data1 = [];
data2 = [];
data3 = [];
sum = 0;

syms k;
%Iterate through the beta value from 0.7 to 0.9 incrementing in 0.02
for beta = 0.7:0.02:0.9
    si = alpha1*(1-beta)/ beta*(1-alpha1); %Calculating si formula
    pi0 = (1-beta)*(1 - si)/ (1 - beta*(1 - si)); %Calculating pi0 formula   
    sum = symsum(k*(pi0*(si^k/(1-beta))),k,0,Inf); %Sum of k*PI_k from k=0 to infinity
    w = sum / alpha1; %Calculate the mean
    data1 = [data1 [beta;w]]; %Storing the mean value
    %Similarly for the other two values
    si = alpha2*(1-beta)/ beta*(1-alpha2);
    pi0 = (1-beta)*(1 - si)/ (1 - beta*(1 - si));
    sum = symsum(k*(pi0*(si^k/(1-beta))),k,0,Inf);
    w = sum / alpha2;
    data2 = [data2 [beta;w]];
    
    si = alpha3*(1-beta)/ beta*(1-alpha3);
    pi0 = (1-beta)*(1 - si)/ (1 - beta*(1 - si));
    sum = symsum(k*(pi0*(si^k/(1-beta))),k,0,Inf);
    w = sum / alpha3;
    data3 = [data3 [beta;w]];
      
end   
figure
hold on;
plot(data1(1,:), data1(2,:),'-*');
plot(data2(1,:), data2(2,:),'-d');
plot(data3(1,:), data3(2,:),'-.');
grid on;
title('Discrete Time M/M/1, Showing Mean waiting time for three different alpha')
xlabel('beta, probability that a packet will depart in any time slot')
ylabel('Value of mean waiting time')
legend('alpha = 0.35','alpha = 0.45','alpha = 0.55');
hold off;
%axis([0.7 0.9 0 50]);
end