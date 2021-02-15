%% script for fitting sine tuning curves linking motor settings to motor speed
% use the turning pad to test the settings-speeds couplings and get
% that perfect dead reckoning for your pixyBot!
% made by DK
% last edited Daniel Ko 20/01/2020

clear;
close all;
clc

%% Change these values!
% The more settings you try, the better the motor settings tuning curve
% will be! - We suggest -1:0.1:1 for a great fit

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

leftWheelForwardsSettings = 0.2:0.2:1;
rightWheelForwardsSettings = 0.2:0.2:1;  % in our case, the right wheel did not move at 0.2 throttle so we omit it
leftWheelForwardsPerSec = [540,810,990,1020,1030]/4;
rightWheelForwardsPerSec = [410,740,980,1050,1050]/4;

leftWheelBackwardsSettings = -0.2:-0.2:-1;
rightWheelBackwardsSettings = -0.2:-0.2:-1;
leftWheelBackwardsPerSec = [510,800,910,970,980]/4;
rightWheelBackwardsPerSec = [650,880,980,990,990]/4;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Fitting the motor settings tuning curve
% create figure to inspect fit
f = figure;
ax = [subplot(1,2,1), subplot(1,2,2)];

% normalise speeds to lowest common maximum speed between the two wheels
minMaxSpeed = min([max(abs(leftWheelForwardsPerSec)), max(abs(rightWheelForwardsPerSec))]);
leftVal = leftWheelForwardsPerSec/minMaxSpeed;
rightVal = rightWheelForwardsPerSec/minMaxSpeed;

% fit sine wave to data
leftFMdl = sineModelFit(ax(2),leftWheelForwardsSettings,leftVal,'b');
rightFMdl = sineModelFit(ax(2),rightWheelForwardsSettings,rightVal,'r');

% normalise speeds to lowest common maximum speed between the two wheels
minMaxSpeed = min([max(abs(leftWheelBackwardsPerSec)), max(abs(rightWheelBackwardsPerSec))]);
leftVal = -leftWheelBackwardsPerSec/minMaxSpeed;
rightVal = -rightWheelBackwardsPerSec/minMaxSpeed;

% fit sine wave to data
leftBMdl = sineModelFit(ax(1),leftWheelBackwardsSettings,leftVal,'b');
rightBMdl = sineModelFit(ax(1),rightWheelBackwardsSettings,rightVal,'r');

% figure formatting
sgtitle('Sine fit of motor setting-speed coupling')
title(ax(1),'Backwards');
legend(ax(1),{'left','leftfit','right','rightfit'})
title(ax(2),'Forwards');
legend(ax(2),{'left','leftfit','right','rightfit'})

%% Insert the output of the following in the denoted lines of pixyBot.py - mind the indents!
% this should be in pixyBot.py. search for lines where lCoeff and rCoeff are defined
fprintf('lCoeff = [[%f, %f, %f], [%f, %f, %f]]\n',...
    leftFMdl.shift,leftFMdl.xscale,leftFMdl.yscale,...
    leftBMdl.shift,leftBMdl.xscale,leftBMdl.yscale);
fprintf('rCoeff = [[%f, %f, %f], [%f, %f, %f]]\n',...
    rightFMdl.shift,rightFMdl.xscale,rightFMdl.yscale,...
    rightBMdl.shift,rightBMdl.xscale,rightBMdl.yscale);
