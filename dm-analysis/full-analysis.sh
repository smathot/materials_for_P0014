#!/bin/bash
rm -Rf plot/
rm -Rf output/
python3 analyze.py --exp1 @gaze_plot @brightness_plot @green_plot @cue_plot_pupil @cue_plot_gaze
python3 analyze.py --exp2 @gaze_plot @brightness_plot @green_plot @cue_plot_pupil @cue_plot_gaze
python3 analyze.py --exp3 @gaze_plot @brightness_plot @green_plot @cuing_effect @correlate_cuing @cue_plot_pupil @cue_plot_gaze
python3 analyze.py --expX @pupil_crossexp @gaze_crossexp
