# coding=utf-8

import analysis
from datamatrix import series as srs
from datamatrix.rbridge import lme4
from datamatrix import cached
from datamatrix import operations as ops
from datamatrix import plot, io, DataMatrix, SeriesColumn, FloatColumn, IntColumn
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
BASELINE_WINDOW = 950, 1000
LMER_TRACE = True
MINLEN = 200
WINLEN = 100
LATENCY_SKIP = 200
SMOOTHWIN_PUPIL = 31
SMOOTHWIN_PUPIL_MEAN = 101
SMOOTHWIN_GAZE = 31

def with_pupil_data(fnc):

	"""
	A decorator to filter pupil data before passing it to a pupil-analysis
	function.
	"""

	def inner(dm, *arglist, **kwdict):
		print('Running with pupil data')
		print('All experiments: Keeping only correct trials')
		dm = dm.correct == 1
		if analysis.exp == 'exp2':
			print('Exp 2: Keeping only memory trials')
			dm = dm.trialType == 'memory'
		return fnc(dm)

	return inner


def with_gaze_data(fnc):

	"""
	A decorator to filter gaze data before passing it to a gaze-analysis
	function.
	"""

	def inner(dm, *arglist, **kwdict):
		print('Running with gaze data')
		dm = io.readpickle('.cache/gaze-data-%s.pkl' % analysis.exp)
		print('All experiments: Keeping only correct trials')
		dm = dm.correct == 1
		if analysis.exp == 'exp2':
			print('Exp 2: Keeping only memory trials')
			dm = dm.trialType == 'memory'
		return fnc(dm)

	return inner
