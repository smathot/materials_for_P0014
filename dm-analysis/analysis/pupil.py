# coding=utf-8

from analysis.constants import *


@with_pupil_data
def green_plot(dm):

	dm_no_green = (dm.clrClsDist != 'green') & (dm.clrClsTarget != 'green')
	dm_green = (dm.clrClsDist == 'green') | (dm.clrClsTarget == 'green')
	plot.new()
	plt.subplot(211)
	plt.title('Without green stimulus')
	dm_bright, dm_dark = ops.tuple_split(dm_no_green.targetLum, 'bright', 'dark')
	plt.axhline(1, linestyle=':', color='black')
	plot.trace(dm_bright.pupil, color=tango.orange[1],
		label='Bright (N=%d)' % len(dm_bright))
	plot.trace(dm_dark.pupil, color=tango.blue[1],
		label='Dark (N=%d)' % len(dm_dark))
	plt.legend()
	plt.subplot(212)
	dm_bright, dm_dark = ops.tuple_split(dm_green.targetLum, 'bright', 'dark')
	plt.title('With green stimulus')
	plt.axhline(1, linestyle=':', color='black')
	plot.trace(dm_bright.pupil, color=tango.orange[1],
		label='Bright (N=%d)' % len(dm_bright))
	plot.trace(dm_dark.pupil, color=tango.blue[1],
		label='Dark (N=%d)' % len(dm_dark))
	plt.legend()
	plot.save('green-plot', folder=analysis.exp)


@with_pupil_data
def cue_plot_pupil(dm, suffix=''):

	plot.new()
	for linestyle, (cue, dm_) in zip((':', '-'), ops.split(dm.memCue)):
		dm_bright, dm_dark = ops.tuple_split(dm_.targetLum, 'bright', 'dark')
		plt.axhline(1, linestyle=':', color='black')
		plot.trace(dm_bright.pupil, err=False, linestyle=linestyle, color=tango.orange[1],
			label='Bright %d (N=%d)' % (cue, len(dm_bright)))
		plot.trace(dm_dark.pupil, err=False, linestyle=linestyle, color=tango.blue[1],
			label='Dark %d (N=%d)' % (cue, len(dm_dark)))
		plt.legend(loc='lower right')
	if LMER_TRACE:
		dm.cue = IntColumn
		dm.cue = dm.memCue*-1+2
		rm = lme4.lmer_series(dm,
			'pupil ~ targetLum*cue + (1+targetLum|subject_nr)',
			winlen=WINLEN, cacheid='lmer-cue-plot-%s%s' % (analysis.exp, suffix))
		a = srs.threshold(rm.t, lambda t: np.abs(t) > 2, min_length=MINLEN)
		plot.threshold(a[1], y=1.005, color=tango.green[1], linewidth=5)
		plot.threshold(a[2], y=1, color=tango.red[1], linewidth=5)
		plot.threshold(a[3], y=.995, color='black', linewidth=5)
	plot.save('cue-plot-pupil-%s%s' % (analysis.exp, suffix), folder=analysis.exp)


@with_pupil_data
def brightness_plot(dm, suffix=''):

	if LMER_TRACE:
		rm = lme4.lmer_series(dm,
			'pupil ~ targetLum + (1+targetLum|subject_nr)',
			winlen=WINLEN, cacheid='lmer-pupil-%s%s' % (analysis.exp, suffix))
	dm_bright, dm_dark = ops.tuple_split(dm.targetLum, 'bright', 'dark')
	plot.new()
	plt.axhline(1, linestyle=':', color='black')
	plot.trace(dm_bright.pupil, color=tango.orange[1],
		label='Bright (N=%d)' % len(dm_bright))
	plot.trace(dm_dark.pupil, color=tango.blue[1],
		label='Dark (N=%d)' % len(dm_dark))
	if LMER_TRACE:
		a = srs.threshold(rm.t, lambda t: t > 2, min_length=MINLEN)
		plot.threshold(a[1], color='black', linewidth=5, y=1)
	plt.xlabel('Time in retention interval (ms)')
	plt.ylabel('Pupil size (normalized)')
	plt.legend()
	plot.save('brightness-plot%s' % suffix, folder=analysis.exp)


@with_pupil_data
def pupil_subject(dm):

	sm = DataMatrix(length=len(dm.subject_nr.unique))
	sm.subject_nr = -1
	sm.pupil = -1
	dm.mean_pupil = srs.reduce_(srs.window(dm.pupil, 950, 1050))
	for row, (subject_nr, dm_) in zip(sm, ops.split(dm.subject_nr)):
		dm_bright, dm_dark = ops.tuple_split(dm_.targetLum, 'bright', 'dark')
		row.subject_nr = subject_nr
		row.pupil = dm_dark.mean_pupil.mean - dm_bright.mean_pupil.mean
		print(subject_nr, row.pupil)
	io.writetxt(sm, 'output/%s/pupil-subject.csv' % analysis.exp)


@with_pupil_data
def pupil_crossexp(dm, suffix=''):

	"""
	Plots the pupil-size effect over time for all three experiments,
	separated by attention and memory trials.
	"""

	print('Filtering')
	dm = (dm.memCue == 2) | (dm.exp != 3)
	print('Done')
	for memCue, _dm in ops.split(dm.memCue):
		print(memCue, _dm.exp.unique)
	if LMER_TRACE:
		rm_ref1 = lme4.lmer_series(dm,
			'pupil ~ targetLum*task_ref1 + (1+targetLum*task_ref1|subject_nr)',
			winlen=WINLEN, cacheid='lmer-crossexp-ref1%s' % suffix)
		rm_ref2 = lme4.lmer_series(dm,
			'pupil ~ targetLum*task_ref2 + (1+targetLum*task_ref2|subject_nr)',
			winlen=WINLEN, cacheid='lmer-crossexp-ref2%s' % suffix)
	plot.new()
	plt.xlabel('Time in retention interval (ms)')
	plt.ylabel('Pupil effect (normalized)')
	plt.axhline(0, linestyle=':', color='black')
	rm = rm_ref1
	xdata =  np.arange(dm.pupil.depth)
	for color, (task, dm_) in zip([tango.green[1], tango.purple[1]],
		ops.split(dm.task_ref1)):
		dm_bright, dm_dark = ops.tuple_split(dm_.targetLum, 'bright', 'dark')
		pupil = dm_dark.pupil.mean - dm_bright.pupil.mean
		# plt.fill_between(xdata, rm.est[1]-rm.se[1], rm.est[1]+rm.se[1], color=color,
		# 	alpha=.25)
		# plt.plot(rm.est[1], label=task, color='black')
		plt.plot(pupil, label='%s (N=%d)' % (task, len(dm_)), color=color)
		rm = rm_ref2
	a = srs.threshold(rm_ref1.t, lambda t: np.abs(t) > 2, min_length=MINLEN)
	plot.threshold(a[1], y=.002, color=tango.green[1], linewidth=5)
	plot.threshold(a[3], y=-0, color='black', linewidth=5)
	a = srs.threshold(rm_ref2.t, lambda t: np.abs(t) > 2, min_length=MINLEN)
	plot.threshold(a[1], y=-.002, color=tango.purple[1], linewidth=5)
	plt.legend(loc='upper left')
	plot.save('crossexp-pupil%s' % suffix, folder=analysis.exp)


@with_pupil_data
def pupil_by_color(dm):

	plot.new()
	i = 1
	for probe_color, dm_ in ops.split(dm.clrClsTarget):
		for dist_color, dm__ in ops.split(dm_.clrClsDist):
			plt.subplot(3,2,i); i += 1
			plt.title('probe %s, dist %s' % (probe_color, dist_color))
			dm_bright, dm_dark = ops.tuple_split(
				dm__.targetLum, 'bright', 'dark')
			plt.axhline(1, linestyle=':', color='black')
			plot.trace(dm_bright.pupil, color=tango.orange[1],
				label='Bright (N=%d)' % len(dm_bright))
			plot.trace(dm_dark.pupil, color=tango.blue[1],
				label='Dark (N=%d)' % len(dm_dark))
	plot.save('pupil-by-color', folder=analysis.exp)
