function mdl = sineModelFit(ax,testBase,testVals, col)
if ~iscolumn(testBase)
    testBase = testBase';
end
if ~iscolumn(testVals)
    testVals = testVals';
end

if ~ismember(0,testBase)
    [testBase, IA, ~] = unique([0; testBase]);
    testVals = [0; testVals];
    testVals = testVals(IA);
end
hold(ax,'on');

ft = fittype('sin((x - shift)/xscale)*yscale','coefficients',{'shift','xscale','yscale'});
mdl = fit(testBase,testVals,ft,'startpoint',[0,1,1]);

% plot actual coupling and fit coupling
if max(testBase) > 0
    fitBase = 0:0.01:1;
    xlim(ax,[0 1]);
else
    fitBase = -1:0.01:0;
    xlim(ax,[-1 0]);
end
plot(ax,testBase,testVals,col,fitBase,mdl(fitBase),[col,'-.']);

ylabel(ax,'Motor speed (deg/sec)');
xlabel(ax,'Motor setting');
ylim(ax,[-1.5 1.5]);
end