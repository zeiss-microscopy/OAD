% Simple Object Count inside a single frame
%
% Date: 13.10.2014
% Version: 1.0

function result = CountObjectsSimple(img, show)

% adapt to your needs ...
I = uint8(squeeze(img));
%I = uint16(squeeze(img));

% Create BW image from Otsu threshold and fill holes
th = graythresh(I);
bw = im2bw(I, th);
bw2 = imfill(bw,'holes');

% Remove all cells < XY pixels
bw4 = bwareaopen(bw2, 25);
bw4_perim = bwperim(bw4);
if show == true
    % creste image where object perimenter is visible
    overlay1 = imfuse(I, bw4_perim,'scaling', 'independent');
end

% get the number of objetcs
[L, numObjects] = bwlabel(bw4);

% Create overlay only once
if show == true
    mask = im2bw(L, 1);
    overlay2 = imfuse(I, mask);
end

result = {};
result{1} = numObjects;
if show == true
    result{2} = overlay1;
end



