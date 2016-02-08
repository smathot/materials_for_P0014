#-*- coding:utf-8 -*-

"""
This file is part of P0014.1.

P0014.1 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

P0014.1 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with P0014.1.  If not, see <http://www.gnu.org/licenses/>.
"""

from analysis.constants import *
from analysis import gaze

@validate
def filter(dm):

	"""
	desc:
		Filters and recodes the data for subsequent processing. Also calls
		gaze-analysis functions, which need to be done before filtering.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix

	returns:
		desc:	A DataMatrix.
		type:	DataMatrix
	"""

	assert(exp in validExp)
	if 'exp' not in dm.columns():
		dm = dm.addField('exp', dtype=str, default=exp)
	print('Filtering for %s' % exp)
	if exp == 'exp2':
		dm = dm.addField('attMatch', dtype=int, default=0)
		i = (dm['trialType'] == 'attention') & \
			(dm['attProbePos'] == dm['probePosTarget'])
		dm['attMatch'][np.where(i)] = 1
	elif exp == 'exp3':
		dm = dm.addField('trialType', dtype=str, default='memory')
	# The subject numbers do not match those deduced from the file names. So
	# we need to fix this and assert that we have exactly 30 unique subject
	# numbers
	for i in dm.range():
		if dm['exp'][i] == 'exp1':
			f = dm['file'][i]
			f = os.path.splitext(f)[0]
			dm['subject_nr'][i] = int(f[7:]) + 1000
		elif dm['exp'][i] == 'exp2':
			dm['subject_nr'][i] = int(dm['file'][i][2:4]) + 2000
		else:
			# TODO recode subject numbers for experiment 3
			dm['subject_nr'][i] = 3000
			pass
	for _dm in dm.group('file'):
		print('file %s -> subject_nr %d' % (_dm['file'][0], \
			_dm['subject_nr'][0]))
	print('%d subjects' % dm.count('subject_nr'))
	if 'no' in dm.unique('practice'):
		dm = dm.select('practice != "yes"')
	else:
		warnings.warn('This DataMatrix contains only practice trials!')
	# Numbers for results section
	print('Experiment 1:')
	dm1 = dm.select('exp == "exp1"')
	dm1 = dm1.select('maxGazeErr < 1024/6')
	dm1 = dm1.select('response_time != ""')
	print('Experiment 2:')
	dm2 = dm.select('exp == "exp2"')
	dm2 = dm2.select('trialType == "memory"')
	dm2 = dm2.select('maxGazeErr < 1024/6')
	dm2 = dm2.select('response_time != ""')
	# Gaze plot by Experiment
	Plot.new(size=(10,5))
	plt.subplots_adjust(wspace=0)
	for i, _exp in enumerate(['exp1', 'exp2', 'exp3']):
		_dm = dm.select('exp == "%s"' % _exp)
		plt.subplot(1, 3, i+1)
		plt.xticks(range(0, 4001, 1000))
		gaze.gazeTracePlot(_dm, subplot=True, suffix='.lmer.%s' % _exp)
		if _exp == 'exp2':
			plt.gca().yaxis.set_ticklabels([])
			plt.title('b) Gaze bias over time (Exp. 2)')
		else:
			plt.ylabel('Gaze-bias toward memory-match probe (deg.)')
			plt.title('a) Gaze bias over time (Exp. 1)')
		plt.xlabel('Time since cue offset (ms)')
		plt.axhline(1, linestyle=':', color='black')
	Plot.save('gazeTraceExp')
	gaze.gazeDev(dm, suffix='.pre')
	gaze.gazeDev(dm.select('memCue == 1'), suffix='.pre.memCue1')
	gaze.gazeDev(dm.select('memCue == 2'), suffix='.pre.memCue2')
	gaze.gazeTracePlot(dm, suffix='.pre')
	dm = dm.select('response_time != ""')
	dm = dm.select('maxGazeErr < 1024/6')
	_dm = dm.select('trialType == "memory"')
	gaze.gazeDev(dm, suffix='.post')
	gaze.gazeTracePlot(dm, suffix='.post')
	return dm

@validate
def descriptives(dm):

	"""
	desc:
		Provide some descriptives, such as cellcount, overall accuracy, etc.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	if exp == 'expX':
		dm = dm.select('trialType == "memory"')
	if exp in ['exp1', 'expX']:
		pm = PivotMatrix(dm, ['subject_nr'], ['subject_nr'], dv='correct',
			func='size')
		pm._print('N')
		pm.save('output/cellcount.csv')
	elif exp == 'exp2':
		for trialType in ['attention', 'memory']:
			_dm = dm.select('trialType == "%s"' % trialType)
			pm = PivotMatrix(_dm, ['subject_nr'], ['subject_nr'], dv='correct',
				func='size')
			pm._print('N (%s)' % trialType)

@validate
def behavior(dm):

	"""
	desc:
		Analyzes accuracy and response times.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
	"""

	if exp == 'expX':
		dm = dm.select('trialType == "memory"')
	if exp in ['exp1', 'expX']:
		pm = PivotMatrix(dm, ['subject_nr'], ['subject_nr'], dv='correct')
		pm._print('Accuracy')
		pm.save('output/correct.csv')
		pm = PivotMatrix(dm, ['clrClsTarget'], ['subject_nr'], dv='correct')
		pm._print('Accuracy')
		pm.save('output/correct.clrClsTarget.csv')
		pm = PivotMatrix(dm, ['subject_nr'], ['subject_nr'], dv='response_time')
		pm._print('Response times')
		pm.save('output/response_time.csv')
	elif exp == 'exp2':
		for trialType in ['attention', 'memory']:
			_dm = dm.select('trialType == "%s"' % trialType)
			pm = PivotMatrix(_dm, ['subject_nr'], ['subject_nr'], dv='correct')
			pm._print('Accuracy (%s)' % trialType)
			pm.save('output/correct.%s.csv' % trialType)
			pm = PivotMatrix(_dm, ['subject_nr'], ['subject_nr'],
				dv='response_time')
			pm._print('Response times (%s)' % trialType)
			pm.save('output/response_time.%s.csv' % trialType)
			if trialType == 'attention':
				_dmCor = _dm.select('correct == 1')
				pm = PivotMatrix(_dm, ['attMatch'],
					['subject_nr'], dv='correct')
				pm._print('Accuracy by attMatch')
				pm.save('output/correct.attention-by-attMatch.csv')
				pm = PivotMatrix(_dmCor, ['attMatch'],
					['subject_nr'], dv='response_time')
				pm._print('Response times by attMatch')
				pm.save('output/response_time.attention-by-attMatch.csv')
				cm = _dm.collapse(['attMatch', 'clrClsTarget'],
					'correct')
				cm.save('output/cm.correct.csv')
				print(cm)
				cm = _dmCor.collapse(['attMatch', 'clrClsTarget'],
					'response_time')
				cm.save('output/cm.rt.csv')
				print(cm)

def behavioralCuingEffect(dm):

	dmCor = dm.select('correct == 1')
	pm = PivotMatrix(dm, ['subject_nr'], ['congruency'], dv='correct',
		func='shape[0]')
	pm._print('N')
	pm = PivotMatrix(dm, ['subject_nr'], ['congruency'], dv='correct')
	pm._print('Accruacy')
	pm = PivotMatrix(dm, ['subject_nr'], ['congruency'], dv='response_time')
	pm._print('RT')
	pm = PivotMatrix(dm, ['subject_nr'], ['targetLoc', 'probePosTarget'],
		dv='correct', func='shape[0]')
	pm._print('N')
	pm = PivotMatrix(dm, ['subject_nr'], ['targetLoc', 'probePosTarget'],
		dv='correct')
	pm._print('Accruacy')
	pm = PivotMatrix(dm, ['subject_nr'], ['targetLoc', 'probePosTarget'],
		dv='response_time')
	pm._print('RT')
