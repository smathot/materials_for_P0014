Because Exp. 1 and 2 were similar in methods and results, we performed a crossexperimental analysis on the combined data. To test how reliable the attention bias away from the memory-match probe was when considering both experiments together, we determined, per participant, the mean difference in pupil size between Probe-on-Dark and Probe-on-Bright trials in the 950 - 1050 ms interval. The results are not crucially dependent on the exact interval; however, because of the initial pupillary constriction, we could not meaningfully analyze pupil size in the period during which the eyes were sometimes captured by the memory-match probe. (This may explain why we did not observe any attentional capture in the pupil-size results; we return to this point in the discussion.) As shown in %FigCrossExp::a, there was a clear tendency for the pupil to be larger on Probe-on-Bright, compared to Probe-on-Dark, trials.

%--
figure:
 source: FigCrossExp.svg
 id: FigCrossExp
 caption: |
  Results from crossexperimental analyses. a) The effect of Probe Brightness on pupil size for individual participants. A positive value (green) indicates that the pupil was larger when the memory-match probe appeared on a dark, compared to a bright, background. b) Pupil size over time as a function of Probe Brightness (Probe-on-Bright, Probe-on-Dark). The box and arrow indicate the 950-1050 ms interval on which the individual-participant data (a) are based. Gray shadings indicate a reliable effect of Probe Brightness. Error bands indicate standard errors.
--%

Next, we used default one-sided Bayesian paired-samples t-tests [@Rouder2009] to test which model was best supported by the data: an *Attention-Toward* (the memory-match probe) model, in which the pupil is largest for Probe-on-Dark trials; a *No-Attention-Bias* model, in which Probe Brightness has no effect on pupil size; or an *Attention-Away* (from the memory-match probe) model, in which the pupil is largest for Probe-on-Bright trials.

First we compared the Attention-Toward and No-Attention-Bias models. This showed strong evidence in favor of the No-Attention-Bias model (*BF* = 16.8), suggesting that the lack of an effect in the predicted direction was not due to insufficient statistical power. Next we compared the Attention-Away and No-Attention-Bias models. This showed moderate evidence in favor of the Attention-Away model (*BF* = 8.7). (For reference, a classical one-sided paired-samples t-test also revealed an effect of Probe Brightness: t(29) = 2.7, p = .005)

When analyzing pupil size over time, using the data from both experiments, the pupil was larger when the probe appeared on a bright, compared to a dark, background. This effect was reliable from 680 - 1570 ms (criterion: t > 2 for at least 200 ms; %FigCrossExp::b).

In summary, a Bayesian analysis revealed moderate evidence that, across the two experiments, there was an attention bias away from, rather than toward, the probe that matched the contents of visual working memory.
