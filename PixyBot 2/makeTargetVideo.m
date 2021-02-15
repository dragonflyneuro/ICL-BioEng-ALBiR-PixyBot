%%
for ii = [0.1,0.2:0.2:4.2]
    fprintf("starting %dHz\n",ii);
    vidMaker(ii,0);
    fprintf("made %dHz\n",ii);
end

%%
for ii = 0.6:0.4:4
    fprintf("starting occ %dHz\n",ii);
    vidMaker(ii,1);
    fprintf("made occ %dHz\n",ii);
end

%%
function vidMaker(f, mode)
fps = 60;
reps = 10;
sideLength = 300;
sideLengthArray = (-sideLength/2+1):sideLength/2;
middleRegionH = 1080/2 + sideLengthArray;
middleRegionW = 1920/2 + sideLengthArray;
boundary = sideLength/2+50;
occWidth = 550;
occArray = (-occWidth/2+1):occWidth/2;

if mode == 0
    writerObj = VideoWriter(['targetVideo_', num2str(f), 'Hz', '.avi']);
else
    writerObj = VideoWriter(['targetVideo_', num2str(f), 'Hz_occluded', '.avi']);
end

writerObj.FrameRate = fps;
open(writerObj);

% calibration
for ii = 0:0.2/fps:2
    % convert the image to a frame
    frame = ones(1080,1920,3);
    %      frame(1:100,1080/2 + (-99:100),1) = 1;
    frame(middleRegionH,round(-cos(2*pi*ii)*(1920/2-boundary)+middleRegionW),1:2) = 0;
    writeVideo(writerObj, frame);
end

if mode == 0
    for ii = 0:f/fps:reps
        % convert the image to a frame
        frame = ones(1080,1920,3);
        %      frame(1:100,1080/2 + (-99:100),1) = 1;
        frame(middleRegionH,round(-cos(2*pi*ii)*(1920/2-boundary)+middleRegionW),2:3) = 0;
        writeVideo(writerObj, frame);
    end
else
    for ii = 0:f/fps:reps
        % convert the image to a frame
        frame = ones(1080,1920,3);
        %      frame(1:100,1080/2 + (-99:100),1) = 1;
        frame(middleRegionH,round(-cos(2*pi*ii)*(1920/2-boundary)+middleRegionW),2:3) = 0;
        frame(middleRegionH,1920/2+occArray,:) = 1;
        writeVideo(writerObj, frame);
    end
end

close(writerObj);

end