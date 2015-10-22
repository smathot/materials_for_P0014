Because Exp. 1 and 2 were similar in methods and results, we performed crossexperimental analyses on the combined data.

## Eye movements: Brief capture by the memory-match probe

To test when the eyes were captured by the memory-match probe, we analyzed gaze position over time during the retention interval. As for the other eye-movement analyses, this analysis was performed on the untrimmed data. (In the trimmed data, there was only a minimal gaze bias toward the memory-match probe, which was compensated for by the gaze-locked central gradient; data not shown.) For each 10 period, we conducted an LME with horizontal gaze position as dependent measure, Memory-Match-Probe Position (Left, Right) as fixed effect and by-participant random intercept and slopes. As shown in %FigGazeTrace, the eyes were sometimes captured by the memory-match probe at the start of the retention interval, but there was hardly any capture later in time (220 - 650 ms; criterion: t > 200 for at least 200 ms). The systematic gaze deviation is driven by a small and distinct proportion of trials on which the eyes were captured by the memory-match probe (%FigGazeDev).

%--
figure:
 source: FigGazeTrace.svg
 id: FigGazeTrace
 caption: |
  Mean horizontal gaze position as a function of memory-match probe (untrimmed data; positive = right). When the memory-match probe was presented on the right side of the screen, gaze was biased toward the right (brown line); when the memory-match probe was presented on the left, gaze was biased toward the left (purple line). This gaze bias is only present at the very beginning of the retention interval. Gray shadings indicate a reliable effect of Memory-Match-Probe Position. Error bands indicate standard errors.
--%

## Pupillometry: Sustained attention bias away from the memory-match probe

To test whether the attention bias away from the memory-match probe was reliable when considering both experiments together, we determined, per participant the mean difference in pupil size between Probe-on-Dark and Probe-on-Bright trials in the 950 - 1050 ms interval. The results are not crucially dependent on the exact interval; however, because of the initial pupillary constriction, we could not meaningfully analyze pupil size in the period during which the eyes were sometimes captured by the memory-match probe. As shown in %FigIndividual, there was a clear tendency for the pupil to be larger on Probe-on-Bright, compared to Probe-on-Dark, trials.

%--
figure:
 source: FigIndividual.svg
 id: FigIndividual
 caption: |
  The effect of Probe Brightness on pupil size for individual participants. A positive value (green) indicates that the pupil was larger when the memory-match probe appeared on a dark, compared to a bright, background.
--%

Next, we used default one-sided Bayesian paired-samples t-tests to test which model was best supported by the data: an *Attention-Toward* (the memory-match probe) model, in which the pupil is largest for Probe-on-Dark trials; a *No-Attention-Bias* model, in which Probe Brightness has no effect on pupil size; or an *Attention-Away* (from the memory-match probe) model, in which the pupil is largest for Probe-on-Bright trials.

First we compared the Attention-Toward and No-Attention-Bias models. This showed strong evidence in favor of the No-Attention-Bias model (BF = 16.8), suggesting that the lack of an effect in the predicted direction was not due to insufficient statistical power. Next we compared the Attention-Away and No-Attention-Bias models. This showed moderate evidence in favor of the Attention-Away model (BF = 8.7). (For reference, a classical one-sided paired-samples t-test also revealed an effect of Probe Brightness: t(29) = 2.7, p = .005)

In summary, a Bayesian analysis revealed moderate evidence that, across the two experiments, there was a sustained attention bias away from, rather than toward, the probe that matched the contents of visual working memory.
