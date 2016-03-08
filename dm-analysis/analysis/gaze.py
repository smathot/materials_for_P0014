# coding=utf-8

import analysis
from analysis.constants import *


def gaze_plot(dm, suffix=''):

	dm = io.readpickle('.cache/gaze-data-%s.pkl' % analysis.exp)
	dm_left, dm_right = ops.tuple_split(dm.probePosTarget,
		'left', 'right')
	if analysis.exp == 'exp2':
		print('Exp 2: Keeping only memory trials')
		dm = dm.trialType == 'memory'
	plot.new()
	plt.xlim(HIST_RANGE)
	plt.axvspan(-170, 170, color=tango.gray[1], zorder=-1000)
	plt.axvline(0, color='black', linestyle=':')
	plt.axvline(-256, color='black', linestyle=':')
	plt.axvline(256, color='black', linestyle=':')
	left_peaks = srs.reduce_(dm_left.xgaze, _peak)
	y, edges = np.histogram(left_peaks, bins=HIST_BINS, range=HIST_RANGE)
	y = np.array(y, dtype=float)/y.max()
	x = .5*edges[1:]+.5*edges[:-1]
	plt.fill_between(x, y, color=tango.red[1], alpha=.25)
	right_peaks = srs.reduce_(dm_right.xgaze, _peak)
	y, edges = np.histogram(right_peaks, bins=HIST_BINS, range=HIST_RANGE)
	y = np.array(y, dtype=float)/y.max()
	x = .5*edges[1:]+.5*edges[:-1]
	plt.fill_between(x, y, color=tango.green[1], alpha=.25)
	plt.legend()
	plot.save('gaze-plot-hist%s' % suffix, folder=analysis.exp)
	plot.new()
	plot.trace(dm_left.xgaze, color=tango.orange[1],
		label='Left (N=%d)' % len(dm_left))
	plot.trace(dm_right.xgaze, color=tango.blue[1],
		label='Right (N=%d)' % len(dm_right))
	plt.legend()
	plot.save('gaze-plot-trace%s' % suffix, folder=analysis.exp)


def gaze_crossexp(dm):

	if LMER_TRACE:
		rm_ref1 = lme4.lmer_series(dm,
			'xgaze ~ probePosTarget*task_ref1 + (1+probePosTarget*task_ref1|subject_nr)',
			winlen=WINLEN, cacheid='lmer-gaze-crossexp-ref1')
		rm_ref2 = lme4.lmer_series(dm,
			'xgaze ~ probePosTarget*task_ref2 + (1+probePosTarget*task_ref2|subject_nr)',
			winlen=WINLEN, cacheid='lmer-gaze-crossexp-ref2')
	dm = io.readpickle('.cache/gaze-data-%s.pkl' % analysis.exp)
	# xdata = np.arange(dm.xgaze.depth)
	plot.new()
	plt.xlabel('Time in retention interval (ms)')
	plt.ylabel('Horiz. gaze bias toward probe/ cue (px)')
	plt.axhline(0, linestyle=':', color='black')
	rm = rm_ref1
	for color, (side, dm_) in zip([tango.green[1], tango.purple[1]],
		ops.split(dm.task_ref1)):
		dm_left, dm_right = ops.tuple_split(dm_.probePosTarget, 'left', 'right')
		pupil = dm_right.xgaze.mean - dm_left.xgaze.mean
		# plt.fill_between(xdata, rm.est[1]-rm.se[1], rm.est[1]+rm.se[1], color=color,
		# 	alpha=.25)
		# plt.plot(rm.est[1], label=task, color='black')
		plt.plot(pupil, label='%s (N=%d)' % (side, len(dm_)), color=color)
		rm = rm_ref2
	a = srs.threshold(rm_ref1.t, lambda t: np.abs(t) > 2, min_length=MINLEN)
	plot.threshold(a[1], y=7, color=tango.green[1], linewidth=5)
	plot.threshold(a[3], y=2.5, color='black', linewidth=5)
	a = srs.threshold(rm_ref2.t, lambda t: np.abs(t) > 2, min_length=MINLEN)
	plot.threshold(a[1], y=-2, color=tango.purple[1], linewidth=5)
	plt.legend(loc='upper left')
	plot.save('crossexp-gaze', folder=analysis.exp)


def _peak(a):

	min_ = np.nanmin(a)
	max_ = np.nanmax(a)
	if np.abs(min_) > np.abs(max_):
		# print('min', min_)
		return min_
	# print('max', max_)
	return max_
