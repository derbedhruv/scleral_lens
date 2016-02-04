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
pts = zeros(max_y-min_y+1,2);
count = 1;

for i = min_y:max_y
    k = find(red(:,i));
    if ~isempty(k)
        idx = mean(k);
        pts(count,1) = i;
        pts(count,2) = idx;
        count = count + 1;
    end
end

pts = pts(1:count,:);

% Fit a spline to red pixel curve
pp = csaps(pts(:,1),pts(:,2),0.0001);
% Plot spline
%yy = ppval(pp, linspace(0,400,101));
hold on;
%plot(linspace(0,400,101), yy(1,:));
fnplt(pp);

figure;
imshow(red);

% Find dervatives and curvature
d1 = fnder(pp);
d2 = fnder(d1);

% Total hack, passing callback from image plot to obscured parent axes.
ax_callback = @(h,e)(disp(e.IntersectionPoint(1)));
set(ax,'ButtonDownFcn',ax_callback);
set(ima,'ButtonDownFcn',@(h,e)(ax_callback(h,e)));

