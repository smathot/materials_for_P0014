#!/bin/bash
rm -Rf plot/
rm -Rf output/
python3 analyze.py --exp1 @gaze_plot @brightness_plot
python3 analyze.py --exp2 @gaze_plot @brightness_plot
python3 analyze.py --exp3 @gaze_plot @brightness_plot @cuing_effect
python3 analyze.py --expX @pupil_crossexp @gaze_crossexp
