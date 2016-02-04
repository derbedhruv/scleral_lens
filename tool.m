close all;
clear all;

% Create main figure window, need to override window resizing logic
fig = figure('Visible','off');
% Create uipanel object
ui = uipanel;
% Create an axes object that overlaps uipanel
ax = axes('Parent',ui,'Position',[0 0 1 1]);
fig.Visible = 'on';

% Read and display image
img = imread('images/Tiff/cropped2_borders.tiff');
ima = imshow(img,'Parent',ax);

% Find red pixels in image
red = all(cat(3,img(:,:,1)>180,img(:,:,2)<60,img(:,:,3)<60),3);
[rows,cols] = find(red);

% Remove non unique values for a particular column
min_y = min(cols);
max_y = max(cols);

for i = min_y:max_y
    
end

% Fit a spline to red pixel curve
%pp = spline(cols,rows);

% Total hack, passing callback from image plot to obscured parent axes.
ax_callback = @(h,e)(disp(e));
set(ax,'ButtonDownFcn',ax_callback);
set(ima,'ButtonDownFcn',@(h,e)(ax_callback(h,e)));

figure;
imshow(red);

