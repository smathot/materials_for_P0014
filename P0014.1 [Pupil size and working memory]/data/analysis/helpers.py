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

@validate
def filter(dm):

	"""
	desc:
		Filters and recodes the data for subsequent processing.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix

	returns:
		desc:	A DataMatrix.
		type:	DataMatrix
	"""

	assert(exp in validExp)
	print('Filtering for %s' % exp)
	if exp == 'exp2':
		dm = dm.addField('attMatch', dtype=int, default=0)
		i = (dm['trialType'] == 'attention') & \
			(dm['attProbePos'] == dm['probePosTarget'])
		dm['attMatch'][np.where(i)] = 1
	# The subject numbers do not match those deduced from the file names. So
	# we need to fix this and assert that we have exactly 21 unique subject
	# numbers
	for i in dm.range():
		dm['subject_nr'][i] = int(dm['file'][i][2:4])
	for _dm in dm.group('file'):
		print('file %s -> subject_nr %d' % (_dm['file'][0], \
			_dm['subject_nr'][0]))
	print('%d subjects' % dm.count('file'))
	if 'no' in dm.unique('practice'):
		dm = dm.select('practice != "yes"')
	else:
		warnings.warn('This DataMatrix contains only practice trials!')
	# Gaze error must be smaller than maximum displacement of stabilizer.
	dm = dm.select('maxGazeErr < 1024/6')
	dm = dm.select('response_time != ""')
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

	if exp == 'exp1':
		pm = PivotMatrix(dm, ['subject_nr'], ['subject_nr'], dv='correct',
			func='size')
		pm._print('N')
	elif exp == 'exp2':
		for trialType in ['attention', 'memory']:
			_dm = dm.select('trialType == "%s"' % trialType)
			pm = PivotMatrix(_dm, ['subject_nr'], ['subject_nr'], dv='correct',
				func='size')
			pm._print('N (%s)' % trialType)

@validate
def pupilTracePlot(dm, traceParams=defaultTraceParams, suffix='',
	subplot=False, model=None, trialType='memory'):

	"""
	desc:
		Plots the pupil trace during the retention interval, separately for cue-
		on-bright and cue-on-dark trials.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix

	keywords:
		traceParams:
			desc:	The pupil-trace parameters.
			type:	dict
		suffix:
			desc:	A suffix for the output files.
			type:	str
		subplot:
			desc:	Indicates if the plot is a subplot of a bigger plot, in
					which case no new figure is created and saved.
			type:	bool
		trialType:
			desc:	The trial type to analyze. Only applicable to exp2.
			type:	str
	"""

	if exp == 'exp2':
		dm = dm.select('trialType == "%s"' % trialType)
	tk.plotTraceContrast(dm, q1, q2, model=model, winSize=winSize,
		cacheId='lmerTrace%s' % suffix, minSmp=1, **traceParams)
	if not subplot:
		Plot.save('pupilTracePlot%s' % suffix, show=show)

def pupilTracePlotLmer(dm):

	pupilTracePlot(dm, model=model, suffix='.lmer')

def pupilTracePlotAttention(dm):

	pupilTracePlot(dm, suffix='.attention', trialType='attention',
		traceParams=attentionTraceParams)

@validate
def pupilTracePlotSubject(dm, traceParams=defaultTraceParams):

	"""
	desc:
		Plots the pupil trace during the retention interval, separately for cue-
		on-bright and cue-on-dark trials, and separately for each participant.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix

	keywords:
		traceParams:
			desc:	The pupil-trace parameters.
			type:	dict
	"""

	N = dm.count('subject_nr')
	i = 1
	Plot.new(Plot.xl)
	for subject_nr in dm.unique('subject_nr'):
		_dm = dm.select('subject_nr == %d' % subject_nr)
		plt.subplot(math.ceil(N/3.), 3, i)
		plt.title('subject %d (N=%d)' % (subject_nr, len(_dm)))
		pupilTracePlot(_dm, subplot=True)
		i += 1
	Plot.save('pupilTracePlotSubject')

@validate
def pupilTracePlotCorrect(dm, traceParams=defaultTraceParams):

	"""
	desc:
		Plots the pupil trace during the retention interval, separately for cue-
		on-bright and cue-on-dark trials, and separately for correct and
		incorrect trials.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix

	keywords:
		traceParams:
			desc:	The pupil-trace parameters.
			type:	dict
	"""

	Plot.new(Plot.w)
	for correct in [0, 1]:
		_dm = dm.select('correct == %d' % correct)
		plt.subplot(2, 1, correct+1)
		plt.title('Correct = %d (N=%d)' % (correct, len(_dm)))
		pupilTracePlot(_dm, subplot=True)
	Plot.save('pupilTraceCorrect')

@validate
def pupilTracePlotColorClass(dm, traceParams=defaultTraceParams):

	"""
	desc:
		Plots the pupil trace during the retention interval, separately for cue-
		on-bright and cue-on-dark trials, and separately for different target
		and distractor colors.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix

	keywords:
		traceParams:
			desc:	The pupil-trace parameters.
			type:	dict
	"""

	Plot.new(Plot.xl)
	i = 1
	for clrClsTarget in colorClasses:
		for clrClsDist in colorClasses:
			_dm = dm.select('clrClsTarget == "%s"' % clrClsTarget)
			_dm = _dm.select('clrClsDist == "%s"' % clrClsDist)
			plt.subplot(3, 3, i)
			plt.title('Target: %s, Dist: %s (N=%d)' \
				% (clrClsTarget, clrClsDist, len(_dm)))
			pupilTracePlot(_dm, subplot=True)
			i += 1
	Plot.save('pupilTraceColorClass')

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

	if exp == 'exp1':
		pm = PivotMatrix(dm, ['subject_nr'], ['subject_nr'], dv='correct')
		pm._print('Accuracy')
		pm.save('output/correct.csv')
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

def attentionStats(dm):

	assert(exp == 'exp2')
	_dm = dm.select('trialType == "attention"')
	_dmCor = _dm
	R = RBridge.R()
	R.load(_dmCor)
	lm = R.lmer('response_time ~ attMatch + (1+attMatch|subject_nr)')
	print(lm)
	lm = R.lmer('response_time ~ attMatch*clrClsTarget + (1+attMatch|subject_nr)')
	print(lm)
	lm = R.lmer('response_time ~ attMatch*clrClsTarget*clrClsDist + (1+attMatch|subject_nr)')
	print(lm)
