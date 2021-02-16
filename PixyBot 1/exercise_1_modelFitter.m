%% script for fitting sine tuning curves linking motor settings to motor speed
% use the turning pad to test the settings-speeds couplings and get
% that perfect dead reckoning for your pixyBot!
% made by DK
% last edited Daniel Ko 16/02/2021

clear;
close all;
clc

%% Change these values!
% The more settings you try, the better the motor settings tuning curve
% will be! - We suggest -1:0.1:1 for a great fit

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

leftWheelForwardsSettings = 0.2:0.2:1;
rightWheelForwardsSettings = 0.2:0.2:1;
leftWheelForwardsDeg = [820,1270,1540,1560,1570];
rightWheelForwardsDeg = [840,1330,1550,1600,1630];

leftWheelBackwardsSettings = -0.2:-0.2:-1;
rightWheelBackwardsSettings = -0.2:-0.2:-1;
leftWheelBackwardsDeg = [820,1300,1510,1540,1560];
rightWheelBackwardsDeg = [720,1000,1340,1570,1570];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Fitting the motor settings tuning curve
% create figure to inspect fit
f = figure;
ax = [subplot(1,2,1), subplot(1,2,2)];

% normalise speeds to lowest common maximum speed between the two wheels
minMaxSpeed = min([max(abs(leftWheelForwardsDeg)), max(abs(rightWheelForwardsDeg))]);
leftVal = leftWheelForwardsDeg/minMaxSpeed;
rightVal = rightWheelForwardsDeg/minMaxSpeed;

% fit sine wave to data
leftFMdl = sineModelFit(ax(2),leftWheelForwardsSettings,leftVal,'b');
rightFMdl = sineModelFit(ax(2),rightWheelForwardsSettings,rightVal,'r');

% normalise speeds to lowest common maximum speed between the two wheels
minMaxSpeed = min([max(abs(leftWheelBackwardsDeg)), max(abs(rightWheelBackwardsDeg))]);
leftVal = -leftWheelBackwardsDeg/minMaxSpeed;
rightVal = -rightWheelBackwardsDeg/minMaxSpeed;

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
    rightBMdl.shift,rightBMdl.xscale,rightBMdl.yscale,...
    rightFMdl.shift,rightFMdl.xscale,rightFMdl.yscale);
