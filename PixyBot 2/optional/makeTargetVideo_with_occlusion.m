%% SCRIPT TO MAKE TARGET TRACKING VIDEOS FOR PIXYBOT
% last edited 17/02/2021 by DK

%% make standard calibration + target video
for ii = [0.1:0.1:1,1.2:0.2:3]
    fprintf("starting %dHz\n",ii);
    vidMaker(ii,0);
    fprintf("made %dHz\n",ii);
end

%% make occluded calibration + target video
for ii = 0.2:0.4:3
    fprintf("starting occ %dHz\n",ii);
    vidMaker(ii,1);
    fprintf("made occ %dHz\n",ii);
end

%% call with frequency (f) and target occlusion (mode) on[1]/off[0]
function vidMaker(f, mode)
fps = 120; % video fps
reps = 10; % number of periods the target moves for
sideLength = 300; % side length of stimulus square
sideLengthArray = (-sideLength/2+1):sideLength/2; % area of stimulus square in coordinates
middleRegionH = 1080/4 + sideLengthArray; % height that the stimulus square covers
middleRegionW = 1920/2 + sideLengthArray; % width that the stimulus square covers in the centre
boundary = sideLength/2+50; % border around maximum travel of stimulus square
occWidth = 550; % width of obstruction
occArray = (-occWidth/2+1):occWidth/2; % area of obstruction in coordinates

% make video objects to write to
if mode == 0
    writerObj = VideoWriter(['targetVideo_', num2str(f), 'Hz', '.mp4'],'MPEG-4');
else
    writerObj = VideoWriter(['targetVideo_', num2str(f), 'Hz_occluded', '.mp4'],'MPEG-4');
end

% set framerate of video and open file
writerObj.FrameRate = fps;
open(writerObj);

% calibration with blue square
for ii = 0:0.2/fps:2
    % convert the image to a frame
    frame = ones(1080,1920,3); % blank frame
    frame(middleRegionH,round(-cos(2*pi*ii)*(1920/2-boundary)+middleRegionW),1:2) = 0; % remove colour channels in stimulus square
    writeVideo(writerObj, frame); % write frame
end

% fill time between calibration and target with green square
frame = ones(1080,1920,3);
frame(middleRegionH,round(-cos(0)*(1920/2-boundary)+middleRegionW),[1,3]) = 0;
for ii = 1:fps*2.5 % 2.5 seconds of intermission
    writeVideo(writerObj, frame);
end

% target with red square
if mode == 0 % no occlusion
    for ii = 0:f/fps:reps
        frame = ones(1080,1920,3);
        frame(middleRegionH,round(-cos(2*pi*ii)*(1920/2-boundary)+middleRegionW),2:3) = 0;
        writeVideo(writerObj, frame);
    end
else % with occlusion
    for ii = 0:f/fps:reps
        frame = ones(1080,1920,3);
        frame(middleRegionH,round(-cos(2*pi*ii)*(1920/2-boundary)+middleRegionW),2:3) = 0;
        frame(middleRegionH,1920/2+occArray,:) = 1; % add obstruction
        writeVideo(writerObj, frame);
    end
end

close(writerObj);

end