## Methods

### Materials and availability

Participant data, experimental scripts, and analysis scripts are available from <http://to.do/>.

### Participants

Fifteen participants were recruited from Utrecht University (7 women; age range 17 - 36; normal or normal-to-corrected vision). All participants signed informed consent before participating and received monetary compensation. The experiment was approved by the ethics committee of Utrecht University (++details++).

### Software and equipment

Eye position and pupil size were recorded with an Eyelink 1000 (SR Research, Mississauga, Canada, ON), a video-based eye tracker sampling at 1000 Hz. Stimuli were presented on a 19" Nokia Multigraph 446Xpro monitor (1024 x 768 px, 120 Hz). Stimulus presentation was controlled with OpenSesame [@MathôtSchreijTheeuwes2012] and PsychoPy [@Peirce2007].

### Procedure

Before the experiment, a nine-point eye-tracker calibration was performed. During the entire trial, the display was divided into a bright (94.7 cd/m^2^) and a dark (1.19 cd/m^2^) half, separated by a 9.7° horizontal luminance gradient (%FigParadigm::a). Participants kept their eyes on the display center from the start of the trial until the response interval (i.e. they were allowed to look at the response options). To control for small eye movements, from the onset of the first color stimulus, the central gradient was locked to gaze position; that is, when the eyes drifted slightly to the left, the gradient moved slightly to the left by an equal amount [cf. Exp. 2 from @Mathôt2013Plos]. This made sure that the eyes were always exactly in between the bright and dark sides of the screen. The maximum displacement of the gradient was 4.9°.

Each trial started with a period of ±3 s during which the pupil adapted to the display, and during which an automatic one-point recalibration (drift correction) was performed (the exact duration depended on the time needed for drift correction). Next, the first color stimulus (an unfilled colored circle; 3.6° diameter) appeared for 1 s, followed by a 1.5 s blank display. The color was randomly selected from six variations of red, green, and blue (%FigParadigm::b). Next, the second color stimulus appeared for 1 s, again followed by a 1.5 s blank display. The second color was always of a different category than the first; that is, if the first color was green, the second color was either red or blue. Next, a memory cue appeared (a centrally presented "1" or "2") for 1 s, indicating whether the first or second color should be remembered. We presented two colors, of which only one was to be remembered, to control for priming effects due to visual presentation of the to-be-remembered color. Next, there was a retention interval of 5 s during which two task-irrelevant probes were presented 7.3° to the left and right of the display center. The two probes were different variations of the same color categories as the two color stimuli; that is, if the color stimuli were red and green, the probes were different variations of red and green (marked as 'Probe colors' in %FigParadigm::b). Finally, three colored circles, all of the same color category as the memorized color, were presented. The participant indicated which of the three colors exactly matched the memorized color by pressing the 1, 2, or 3 key on the keyboard.

%--
figure:
 source: FigParadigm.svg
 id: FigParadigm
 caption: |
  The experimental paradigm. a) A schematic example trial. This example shows a Probe-on-Dark trial, because the memory-match probe (the green circle shown on the left during the retention interval) is on a dark background. b) The colors used for the experiment, including their hexadecimal RGB notation.
--%

The crucial manipulation was the placement of the probe that matched the memorized color (from now on: *memory-match probe*; in %FigParadigm::a this is the green circle on the left during the retention interval). On Probe-on-Dark trials, the memory-match probe was placed on the dark background (as in %FigParadigm::a); on Probe-on-Bright trials, the memory-match probe was placed on the bright background.

The experiment consisted of 24 practice trials, followed by 144 experimental trials, and took ±1.5 h. Probe Brightness (Probe-on-Dark, Probe-on-Bright) and Probe Side (Left, Right) were randomized within blocks.

## Results

### Trial-exclusion criteria

Trials were discarded when horizontal gaze deviation from the display center during the retention interval exceeded the maximum displacement of the central gradient (15.8%; see Methods: Procedure). Due to a technical problem, manual responses were not logged for some trials; these were excluded (1.3%). No participants were excluded. In total, 1,749 trials remained for further analysis.

### Behavioral results

Accuracy was 74.3% (SE = 1.8). Mean correct response time (RT) was 2.2 s (SE = 0.1).

### Eye-movement results

%--
figure:
 source: FigGazeDev.svg
 id: FigGazeDev
 caption: |
  A histogram of the per-trial maximum gaze deviation toward the memory-match probe. The shaded area indicates the maximum displacement of the gaze-locked central gradient; trials that fell outside of this area were removed for the main analyses. a) Results from Experiment 1. b) Results from Experiment 2.
--%

On about 15% of trials, gaze deviated considerably from the display center; trials with such gaze errors were discarded for the main (pupil-size and behavioral) analyses. However, to test whether the eyes were drawn toward the memory-match probe, we analyzed gaze deviation in the full, untrimmed data. For each trial, we determined the maximum gaze deviation from the center. Next, we split the data by the location of the memory-match probe (Left, Right), and conducted a default one-sided Bayesian paired-samples t-test on the per-participant average gaze deviation [@Rouder2009]. This revealed moderate evidence for a deviation toward the memory-match probe, compared to no systematic deviation (BF = 6.9). (For reference, a classical one-sided paired-samples t-test revealed the same bias: t(14) = 2.7, p = .009) This bias is clearly visible in the distribution of per-trial maximum gaze-deviations, which shows a distinct peak around the memory-match probe (%FigGazeDev::a).

### Pupil-size results

We analyzed pupil size during the retention interval. Mean pupil size during the last 100 ms of cue presentation was taken as a baseline, and all pupil size measures are reported in area (i.e., not diameter) relative to this baseline. Pupil size during blinks was reconstructed using cubic-spline interpolation [@Mathôt2013Blinks]. Pupil size was smoothed with a 31 ms Hanning window.

For each 10 ms period, we conducted a linear mixed-effects (LME) analysis with normalized pupil size as dependent measure, Probe Brightness (Probe-on-Dark, Probe-on-Bright) as fixed effect, and by-participant random intercept and slopes. Only correct-response trials were included in this analysis. We did not estimate p-values, but considered effects reliable if they corresponded to t > 2 for at least 200 ms [cf. @Mathôt2014Exo]. However, we emphasize effect sizes and overall patterns.

%FigPupilTrace::a shows pupil size over time as a function of Probe Brightness. There is an overall constriction from about 250 ms after the start of the retention interval; this is a visual response to the onset of the retention-interval display. This constriction is followed by a slow dilation, which is partly a recovery from the initial constriction, and partly an effect of memory load [e.g., @KahnemanBeatty1966]. Crucially, and in contrast to our prediction, the pupil was slightly (and not reliably) larger, rather than smaller, when the memory-match probe was on a bright (orange line), compared to a dark (blue line), background.

%--
figure:
 source: FigPupilTrace.svg
 id: FigPupilTrace
 caption: |
  Pupil size over time as a function of Probe Brightness (Probe-on-Bright, Probe-on-Dark). a) Results from Experiment 1. b) Results from Experiment 2. Gray shadings indicate a reliable effect of Probe Brightness. Error bands indicate standard errors.
--%

## Discussion

In Exp. 1, we found that the eyes were initially captured by the probe that matched the content of visual working memory (memory-match probe). However, the pupillary data suggest that this initial gaze bias did not result in a sustained shift of attention toward the memory-match probe throughout the retention interval; that is, when the memory-match probe appeared on a bright background, the pupil was not smaller than when it appeared on a dark background; rather, there was a tendency in the opposite direction.
