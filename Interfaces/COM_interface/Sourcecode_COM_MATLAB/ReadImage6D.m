% #################################################################
% File       : ReadImage6D.m
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

% Read CZI image data into image6d array 
function out = ReadImage6D(filename)

% Get OME Meta-Information
MetaData = GetOMEData(filename);

% The main inconvenience of the bfopen.m function is that it loads all the content of an image regardless of its size.
% Initialize BioFormtas Reader
reader = bfGetReader(filename);

% add progress bar
h = waitbar(0,'Processing Data ...');
totalframes = MetaData.SeriesCount * MetaData.SizeC * MetaData.SizeZ * MetaData.SizeT;
framecounter = 0;

% Preallocate array with size (Series, SizeC, SizeZ, SizeT, SizeX, SizeY) 
image6d = zeros(MetaData.SeriesCount, MetaData.SizeT, MetaData.SizeZ,  MetaData.SizeC, MetaData.SizeY, MetaData.SizeX);

for series = 1: MetaData.SeriesCount

    % set reader to current series
    reader.setSeries(series-1);
    for timepoint = 1: MetaData.SizeT
        for zplane = 1: MetaData.SizeZ
            for channel = 1: MetaData.SizeC

                framecounter = framecounter + 1;
                 % update waitbar
                wstr = {'Reading Images: ', num2str(framecounter), ' of ', num2str(totalframes),'Frames' };
                waitbar(framecounter / totalframes, h, strjoin(wstr))

                % get linear index of the plane (1-based)
                iplane = loci.formats.FormatTools.getIndex(reader, zplane - 1, channel - 1, timepoint -1) +1;
                % get frame for current series
                image6d(series, timepoint, zplane, channel, :, :) = bfGetPlane(reader, iplane);

            end
        end
    end
end

% close waitbar
close(h)

% close BioFormats Reader
reader.close();

% store image data and meta information in cell array
out = {};
% store the actual image data as 6d array
out{1} = image6d;
% store the image metainformation
out{2} = MetaData;
    




