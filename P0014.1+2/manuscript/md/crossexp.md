Because the results of Exp. 1 and 2 were similar, we performed a crossexperimental analysis on the combined data. First, we determined, per participant, the mean difference in pupil size between Probe-on-Dark and Probe-on-Bright trials in the 950 - 1050 ms interval (i.e. after the initial constriction; the results are not crucially dependent on the exact interval). As shown in %FigIndividual, there was a clear tendency for the pupil to be larger when the memory-matching probe appeared on a bright, compared to a dark, background.

%--
figure:
 source: FigIndividual.svg
 id: FigIndividual
 caption: |
  The effect of Probe Brightness on pupil size for individual participants. A positive value (green) indicates that the pupil was larger when the probe appeared on a dark, compared to a bright, background.
--%

Next, we used a default Bayesian paired-samples t-tests [@Rouder2009; using JASP 0.7.1.32] to test which model was best supported by the data: an Attention model, in which the pupil is largest for Probe-on-Dark trials; a Null model, in which Probe Brightness has no effect on pupil size; or an Inhibition model, in which the pupil is largest for Probe-on-Bright trials.

First we compared the Attention and Null models. This showed strong evidence in favor of the Null model (Bf = 16.8), suggesting that our failure to find an effect in the predicted direction is not due to insufficient statistical power. Next we compared the Null and Inhibition models. This showed moderate evidence in favor of the Inhibition model (Bf = 8.7). (For reference, a classical two-sided paired-samples t-test also revealed an effect of Probe brightness: t(29) = 2.7, p = 0.010)

In summary, a Bayesian analysis shows that, across the two experiments, the pupillary data suggests that attention was biased away from, rather than toward, the memory-matching probe.
