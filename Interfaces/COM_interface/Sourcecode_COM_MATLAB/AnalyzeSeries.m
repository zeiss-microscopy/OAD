% #################################################################
% File       : AnalyzeSeries.m
% Version    : 1.0
% Author     : czsrh
% Date       : 06.12.2018
% Insitution : Carl Zeiss Microscopy GmbH
%
% Copyright (c) 2018 Carl Zeiss AG, Germany. All Rights Reserved.
%
% Permission is granted to use, modify and distribute this code,
% as long as this copyright notice remains part of the code.
% #################################################################


function [numObjects, img2show, show] = AnalyzeSeries(image6d)

dims = size(image6d);
% series is 1st dimension !
series = dims(1);
% create random image number to shwo later on
show = randi([1 series]);
% add progress bar
h = waitbar(0,'Processing Data ...');

for tp=1: series

    % update waitbar
    wstr = {'Processed: ', num2str(tp), ' of ', num2str(series),'Frames' };
    waitbar(tp / series, h, strjoin(wstr))
    % get current image from series
    img = image6d(tp, 1, 1, 1, :, :);
    % analyze current image
    if tp == show
        result = CountObjectsSimple(img,true);
        numObjects(tp) = result{1};
        img2show = result{2};
    else
        result = CountObjectsSimple(img, false);
        numObjects(tp) = result{1};
    end            
end

% close waitbar
close(h)




