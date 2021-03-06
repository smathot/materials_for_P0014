# coding=utf-8

from analysis.constants import *

def _get_corr_trace(dm, dv, shuffle):

	cm = _get_cm(dm, shuffle=shuffle)
	_r = np.empty(cm.pupil_effect.depth)
	_p = np.empty(cm.pupil_effect.depth)
	for j in range(cm.pupil_effect.depth):
		s, i, r, p, se = linregress(cm.pupil_effect[:,j], cm[dv][:,j])
		_p[j] = p
		_r[j] = r
	return _r, _p

@cached
def _permutation_correlations(dm, dv, N):

	shuffle_r = []
	for i in range(N):
		r, p = _get_corr_trace(dm, dv=dv, shuffle=True)
		shuffle_r.append(r.sum())
	return shuffle_r

def correlate_cuing(dm):

	"""
	desc:
		Determine the correlation between the pupil effect and the behavioral
		cuing effect in RT and accuracy.
	"""


	plot.new()
	for cue in (1, 2):
		cm = _get_cm(dm, cue)
		rt_p, rt_r, acc_p, acc_r = _regress(cm)
		plt.subplot(2,2,cue)
		plt.xlabel('Time in retention interval (ms)')
		plt.ylabel('Pupil effect (normalized)')
		plt.title('Individual pupil effects (cue %d)' % cue)
		plt.axhline(0, linestyle=':', color='black')
		plt.plot(cm.pupil_effect.plottable, color=tango.blue[1], alpha=.25)
		plt.plot(cm.pupil_effect.mean, color=tango.blue[1], linewidth=2)
		plt.ylim(-.1, .12)

		plt.subplot(2,2,cue+2)
		plt.ylim(-1, 1)
		plt.ylabel('R(pupil ~ behavior)')
		plt.xlabel('Time in retention interval (ms)')
		plt.axhline(0, linestyle=':', color='black')
		plt.plot(rt_r, color=tango.orange[1], label='Response time')
		plot.threshold(rt_p < .05, y=-.5, color=tango.orange[1], linewidth=5,
			min_length=MINLEN)
		plt.axhline(0, linestyle=':', color='black')
		plt.plot(acc_r, color=tango.blue[1], label='Accuracy')
		plot.threshold(acc_p < .05, y=-.5, color=tango.blue[1], linewidth=5,
			min_length=MINLEN)
		plt.legend(loc='lower right')
	plot.save('correlate_cuing', folder=analysis.exp)

@cached
def _get_cm(dm, cue):

	dm = dm[:]
	dm.pupil = srs.window(dm.pupil, start=LATENCY_SKIP)
	cm = DataMatrix(length=len(dm.subject_nr.unique))
	cm.pupil_effect = SeriesColumn(depth=dm.pupil.depth)
	cm.cuing_effect_rt = SeriesColumn(depth=dm.pupil.depth)
	cm.cuing_effect_acc = SeriesColumn(depth=dm.pupil.depth)
	cm.corr_rt_r = SeriesColumn(depth=dm.pupil.depth)
	cm.corr_rt_p = SeriesColumn(depth=dm.pupil.depth)
	for row, (subject_nr, dm_) in zip(cm, ops.split(dm.subject_nr)):
		print(subject_nr)
		dm_pupil = (dm_.correct == 1) & (dm_.memCue == cue)
		dm_bright, dm_dark = ops.tuple_split(dm_pupil.targetLum, 'bright', 'dark')
		dm_congruent, dm_incongruent = ops.tuple_split(dm_.congruency, 1, 0)
		row.cuing_effect_rt = (dm_incongruent.correct == 1).response_time.mean \
			- (dm_congruent.correct == 1).response_time.mean
		row.cuing_effect_acc = dm_incongruent.correct.mean \
			- dm_congruent.correct.mean
		row.pupil_effect = srs._smooth(
			dm_dark.pupil.mean - dm_bright.pupil.mean,
			winlen=SMOOTHWIN_PUPIL_MEAN)
		# row.pupil_effect = dm_dark.pupil.mean - dm_bright.pupil.mean
	return cm

def _regress(cm):

	rt_r = np.empty(cm.pupil_effect.depth)
	rt_p = np.empty(cm.pupil_effect.depth)
	acc_r = np.empty(cm.pupil_effect.depth)
	acc_p = np.empty(cm.pupil_effect.depth)
	for j in range(cm.pupil_effect.depth):
		s, i, r, p, se = linregress(cm.pupil_effect[:,j], cm.cuing_effect_rt[:,j])
		rt_p[j] = p
		rt_r[j] = r
		s, i, r, p, se = linregress(cm.pupil_effect[:,j], cm.cuing_effect_acc[:,j])
		acc_p[j] = p
		acc_r[j] = r
	return rt_p, rt_r, acc_p, acc_r
