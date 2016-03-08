# coding=utf-8

from analysis.constants import *


def brightness_plot(dm, suffix=''):

	if analysis.exp == 'exp2':
		print('Exp 2: Keeping only memory trials')
		dm = dm.trialType == 'memory'
	# if LMER_TRACE:
	# 	rm = lme4.lmer_series(dm,
	# 		'pupil ~ targetLum + (1+targetLum|subject_nr)',
	# 		winlen=WINLEN, cacheid='lmer-%s' % analysis.exp)
	dm_bright, dm_dark = ops.tuple_split(dm.targetLum, 'bright', 'dark')
	plot.new()
	plt.axhline(1, linestyle=':', color='black')
	plot.trace(dm_bright.pupil, color=tango.orange[1],
		label='Bright (N=%d)' % len(dm_bright))
	plot.trace(dm_dark.pupil, color=tango.blue[1],
		label='Dark (N=%d)' % len(dm_dark))
	# if LMER_TRACE:
	# 	a = srs.threshold(rm.t, lambda t: t > 2, min_length=MINLEN)
	# 	plot.threshold(a[1], color='black', linewidth=5, y=1)
	plt.xlabel('Time in retention interval (ms)')
	plt.ylabel('Pupil size (normalized)')
	plt.legend()
	plot.save('brightness-plot%s' % suffix, folder=analysis.exp)


def pupil_crossexp(dm):

	if LMER_TRACE:
		rm_ref1 = lme4.lmer_series(dm,
			'pupil ~ targetLum*task_ref1 + (1+targetLum*task_ref1|subject_nr)',
			winlen=WINLEN, cacheid='lmer-crossexp-ref1')
		rm_ref2 = lme4.lmer_series(dm,
			'pupil ~ targetLum*task_ref2 + (1+targetLum*task_ref2|subject_nr)',
			winlen=WINLEN, cacheid='lmer-crossexp-ref2')
	# xdata = np.arange(dm.pupil.depth)
	plot.new()
	plt.xlabel('Time in retention interval (ms)')
	plt.ylabel('Pupil effect (normalized)')
	plt.axhline(0, linestyle=':', color='black')
	rm = rm_ref1
	for color, (task, dm_) in zip([tango.green[1], tango.purple[1]],
		ops.split(dm.task_ref1)):
		dm_bright, dm_dark = ops.tuple_split(dm_.targetLum, 'bright', 'dark')
		pupil = dm_dark.pupil.mean - dm_bright.pupil.mean
		# plt.fill_between(xdata, rm.est[1]-rm.se[1], rm.est[1]+rm.se[1], color=color,
		# 	alpha=.25)
		# plt.plot(rm.est[1], label=task, color='black')
		plt.plot(pupil, label=task, color=color)
		rm = rm_ref2
	a = srs.threshold(rm_ref1.t, lambda t: np.abs(t) > 2, min_length=MINLEN)
	plot.threshold(a[1], y=.002, color=tango.green[1], linewidth=5)
	plot.threshold(a[3], y=-0, color='black', linewidth=5)
	a = srs.threshold(rm_ref2.t, lambda t: np.abs(t) > 2, min_length=MINLEN)
	plot.threshold(a[1], y=-.002, color=tango.purple[1], linewidth=5)
	plt.legend(loc='upper left')
	plot.save('crossexp-pupil', folder=analysis.exp)
