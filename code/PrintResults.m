clear;
runId = 4;
errorRateTesting = importdata(strcat('Results/Run',int2str(runId),'/errorRateTesting.txt'));
errorRateTraining = importdata(strcat('Results/Run',int2str(runId),'/errorRateTraining.txt'));
errorRateTraining = [errorRateTraining(1);errorRateTraining];

hold on
plot(0:(length(errorRateTesting)-1),errorRateTesting);
plot(0:(length(errorRateTesting)-1),errorRateTraining);
legend('Testing','Training');
title(strcat('Run:',32,int2str(runId)));
xlabel('Iteration');
ylabel('Error rate');
if(errorRateTesting(1) > errorRateTraining(1))
    ylim([0 errorRateTesting(1)+0.05]);
else
    ylim([0 errorRateTraining(1)+0.05]);
end
grid on
grid minor
hold off