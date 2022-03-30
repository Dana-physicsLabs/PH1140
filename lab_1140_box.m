%drag your excel file or csv file into the side bar
%replace filename and otherfilename with the actual name's of your file

my_data = readmatrix('filename.csv'); % assuming the file is freq and wavelength dataset 
other_data = readmatrix('other_filename.csv'); %assuming the file is just speeds

freq = my_data(:,1); %assuming col1 is freq
lambda = my_data(:,2); %assuming col2 is wavelength

spd=freq.*lambda;

%please change the title and labels :)
figure
boxplot([spd,other_data],labels={'moine','not moine'})
ylabel('Rollin around at the [s^(-1)/m^(-1)]')
title('eltit')