# coding=utf-8

import analysis
from analysis.constants import *
from datamatrix import cached
import os

@cached
def preprocess(dm):

	if analysis.exp == 'expX':
		return dm
	ops.keep_only(dm, [
		'practice', 'response_time', 'congruency', 'xtrace_retention',
		'ptrace_retention', 'targetLum', 'probePosTarget', 'memCue', 'correct',
		'subject_nr', 'path', 'ptrace_cue', 'trialType'
		])
	# The subject numbers do not match those deduced from the file names. So
	# we need to fix this and assert that we have exactly 30 unique subject
	# numbers
	for row in dm:
		if analysis.exp == 'exp1':
			f = os.path.splitext(row.path)[0]
			row.subject_nr = int(f[17:]) + 1000
		elif analysis.exp == 'exp2':
			row.subject_nr = int(row.path[12:-5]) + 2000
		elif analysis.exp == 'exp3':
			row.subject_nr = int(row.path[17:-4]) + 3000
		else:
			raise Exception()
	if analysis.exp == 'exp2':
		assert(2*len(dm.subject_nr.unique) == len(dm.path.unique))
	else:
		assert(len(dm.subject_nr.unique) == len(dm.path.unique))
	print('%d subjects' % len(dm.subject_nr.unique))
	# Remove practice
	dm = _summarize(dm, dm.practice == 'no', 'Practice')
	# Filter gaze errors
	dm.xgaze = srs.smooth(dm.xtrace_retention, winlen=31) - XC
	del dm.xtrace_retention
	dm.n_gaze_err = srs.reduce_(dm.xgaze, _gaze_error)
	# Process pupil trace
	dm.pupil = srs.blinkreconstruct(dm.ptrace_retention)
	dm.baseline = srs.blinkreconstruct(dm.ptrace_cue)
	del dm.ptrace_retention
	del dm.ptrace_cue
	dm.pupil = srs.smooth(dm.pupil, winlen=31)
	dm.baseline = srs.smooth(dm.baseline, winlen=31)
	dm.pupil = srs.baseline(dm.pupil, dm.baseline, BASELINE_WINDOW[0],
		BASELINE_WINDOW[1])
	if analysis.exp == 'exp3':
		dm.pupil.depth = DEPTH_EXP3
		dm.xgaze.depth = DEPTH_EXP3
	else:
		dm.pupil.depth = DEPTH_EXP12
		dm.xgaze.depth = DEPTH_EXP12
	io.writepickle(dm, '.cache/gaze-data-%s.pkl' % analysis.exp)
	dm = _summarize(dm, dm.n_gaze_err <= MAX_N_GAZE_ERR, 'Gaze errors')
	return dm


def _summarize(dm_before, dm_after, msg):

	print('%s: N(before) = %d, N(after) = %d' \
		% (msg, len(dm_before), len(dm_after)))
	return dm_after


def _gaze_error(a):

	return np.sum(np.abs(a) > MAX_GAZE_ERR)
