# coding=utf-8

import analysis
from datamatrix import series as srs
from datamatrix.rbridge import lme4
from datamatrix import cached
from datamatrix import operations as ops
from datamatrix import plot, io, DataMatrix, SeriesColumn, FloatColumn
from datamatrix.colors import tango
from matplotlib import pyplot as plt
from scipy.stats import linregress, ttest_1samp
import numpy as np

MAX_GAZE_ERR = 170
MAX_N_GAZE_ERR = 10
XC, YC = 512, 384
HIST_BINS = 25
HIST_RANGE = -400, 400
DOWNSAMPLE = 1
MAXDEPTH = 5000
DEPTH_EXP12 = 5000
DEPTH_EXP3 = 2000
BASELINE_WINDOW = 900, 1000
LMER_TRACE = True
MINLEN = 200
WINLEN = 10
