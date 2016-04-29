clear;
runs = 5;
values = 26;
errorRateTesting = zeros(1,values);
errorRateTraining = zeros(1,values);
for i=[1:runs]
    errorRateTestingTemp = (importdata(strcat('Results/Run',int2str(i),'/errorRateTesting.txt')))';
    errorRateTrainingTemp = (importdata(strcat('Results/Run',int2str(i),'/errorRateTraining.txt')))';
    errorRateTrainingTemp = [errorRateTrainingTemp(1),errorRateTrainingTemp];
    errorRateTesting = errorRateTesting + errorRateTestingTemp;
    errorRateTraining = errorRateTraining + errorRateTrainingTemp;
end

errorRateTesting = errorRateTesting ./ runs;
errorRateTraining = errorRateTraining ./ runs;

hold on
plot(0:(length(errorRateTesting)-1),errorRateTesting);
plot(0:(length(errorRateTesting)-1),errorRateTraining);
legend('Testing','Training');
title(strcat('Average of ',32,int2str(runs), ' runs'));
xlabel('Itteration');
ylabel('Error rate');
if(errorRateTesting(1) > errorRateTraining(1))
    ylim([0 errorRateTesting(1)+0.05]);
else
    ylim([0 errorRateTraining(1)+0.05]);
end
grid on
grid minor
hold off