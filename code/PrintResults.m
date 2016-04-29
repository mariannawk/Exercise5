clear;
errorRateTesting = importdata('errorRateTesting.txt');
errorRateTraining = importdata('errorRateTraining.txt');
errorRateTraining = [errorRateTraining(1);errorRateTraining];

hold on
plot(0:(length(errorRateTesting)-1),errorRateTesting);
plot(0:(length(errorRateTesting)-1),errorRateTraining);
legend('Testing','Training');
title('Run5');
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