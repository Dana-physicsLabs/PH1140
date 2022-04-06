filepath = uigetfile('*.csv');
x = readmatrix(filepath);

position = x(4000:end,2);

Fs = 1/0.05;   %sampling frequncy
L = length(position);  %signal length
n = 2^nextpow2(L);  %very large number to pad fft with zeros
w = window(@hamming, L);

Y = fft(position.*w,n);


f = Fs*(0:(n/2))/n; %only care about half of the domain since fft is mirrored
P = abs(Y/n).^2;     

cutoff = 411;

plot(f(cutoff:end),P(cutoff:n/2+1))
title('Frequency Domain')
xlabel('Frequency (f)')
ylabel('|P(f)|^2')
findpeaks(P(cutoff:n/2+1),f(cutoff:end),'MinPeakHeight',1*10^-7); 