function mdl = sineModelFit(ax,testBase,testVals, col)
% input checking
if ~iscolumn(testBase)
    testBase = testBase';
end
if ~iscolumn(testVals)
    testVals = testVals';
end
% sort the input and add a 0 speed setting, if it doesn't exist
if ~ismember(0,testBase)
    [testBase, IA, ~] = unique([0; testBase]);
    testVals = [0; testVals];
    testVals = testVals(IA);
end
hold(ax,'on');

% begin a sine fit - if you think you can get a better fit than sine, go for it!
ft = fittype('sin((x - shift)/xscale)*yscale','coefficients',{'shift','xscale','yscale'});
% set initial guess points of fitting as [0, 1, 1] for shift, xscale and yscale.
% play around with the initial guesses if you have time!
mdl = fit(testBase,testVals,ft,'startpoint',[0,1,1]);

% plot actual coupling and fit coupling of speeds and settings
if max(testBase) > 0
    fitBase = 0:0.01:1;
    xlim(ax,[0 1]);
else
    fitBase = -1:0.01:0;
    xlim(ax,[-1 0]);
end
plot(ax,testBase,testVals,col,fitBase,mdl(fitBase),[col,'-.']);

ylabel(ax,'Motor speed (relative to maximum speed)');
xlabel(ax,'Motor setting');
ylim(ax,[-1.5 1.5]);
end