% #################################################################
% File       : DisplayObjectNumbers.m
% Version    : 1.0
% Author     : czsrh
% Date       : 06.12.2018
% Insitution : Carl Zeiss Microscopy GmbH
%
%
% Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
% #################################################################

function DisplayObjectNumbers(numObjects, segimage, show)

%create figure
figure('position', [100, 100, 1000, 600])  % create new figure with specified size

% 1st plot - Histogram
subplot(2,2,1)
hist(numObjects);
title('Distribution', 'FontSize', 14)
xlabel('Number of Objects', 'FontSize', 12)
ylabel('Occurence', 'FontSize', 12)
grid on

% 2nd plot - Follow Acquisition
subplot(2,2,2)
bar(numObjects, 1.0, 'r')
title('Follow Acquisition', 'FontSize', 14)
xlabel('Frame', 'FontSize', 12)
ylabel('Number', 'FontSize', 12)
grid on
axis([1 length(numObjects) 0 max(numObjects)*1.1])

% 3rd plot - Display Heatmap
subplot(2,2,3)
% Remark: This works for Comb-Style Acqusition only ...
well = reshape(numObjects, 8,12);
imagesc(well);
axis equal tight
set(gca,'xtick', [1:12]); % Well Columns
set(gca,'ytick', [1:8]);  % Well Rows
set(gca,'YTickLabel',{'A','B','C','D','E','F','G','H'});
colorbar
title('Objetcs per Well', 'FontSize', 14);

% 4th plot - Segmentation Example
subplot(2,2,4)
imagesc(segimage);
tstr = {'Frame : ', num2str(show), ' - Objects Detected : ', num2str(numObjects(show)) };
title(strjoin(tstr), 'FontSize', 14)
axis equal tight
xlabel('X [pixel]')
ylabel('Y [pixel]')


