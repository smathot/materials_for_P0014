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

	assert(trialType == 'memory' or exp == 'exp2')
	if exp in ['exp2', 'expX']:
		dm = dm.select('trialType == "%s"' % trialType)
	tk.plotTraceContrast(dm, q1, q2, color1=orange[1], color2=blue[1],
		label1='Probe on bright side (N=%d)' % len(dm.select(q1)),
		label2='Probe on dark side (N=%d)' % len(dm.select(q2)),
		model=model, winSize=winSize, cacheId='lmerTrace%s' % suffix,
		minSmp=200, **traceParams)
	if not subplot:
		Plot.save('pupilTracePlot%s' % suffix, show=show)

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
def pupilTracePlotRT(dm, traceParams=defaultTraceParams):

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

	dm = dm.select('correct == 1')
	dm = dm.addField('_rt', dtype=float)
	dm = dm.addField('rtx', dtype=float)
	dm = dm.calcPerc('response_time', '_rt', keys=['subject_nr'], nBin=2)
	dm['_rt'] /= 50
	dm['rtx'] = dm['_rt']
	print(dm.collapse(['_rt'], 'response_time'))
	for i, _rt in [(1, 0), (2, 1)]:
		_dm = dm.select('_rt == %d' % _rt)
		plt.subplot(2, 1, i)
		plt.title('RT = %d (N=%d)' % (_rt, len(_dm)))
		pupilTracePlot(_dm, subplot=True, model=model,
			suffix='.lmer.rt%s' % _rt)
	Plot.save('pupilTraceRT')
	_model = 'targetLum*rtx + (1+rtx+targetLum|subject_nr)'
	_dm = dm.select('trialType == "memory"')
	mm = tk.mixedModelTrace(_dm, _model, winSize=winSize,
		cacheId='.lmer.rtGrand', **defaultTraceParams)
	tk.statsTrace(mm)

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
		pupilTracePlot(_dm, subplot=True, model=model,
			suffix='.lmer.correct%s' % correct)
	Plot.save('pupilTraceCorrect')
	_model = 'targetLum*correct + (1+correct+targetLum|subject_nr)'
	_dm = dm.select('trialType == "memory"')
	mm = tk.mixedModelTrace(_dm, _model, winSize=winSize,
		cacheId='.lmer.correctGrand', **defaultTraceParams)
	tk.statsTrace(mm)

@validate
def pupilTracePlotExp(dm, traceParams=defaultTraceParams):

	"""
	desc:
		Plots the pupil trace during the retention interval, separately for cue-
		on-bright and cue-on-dark trials, and separately for Exp 1 and 2.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix

	keywords:
		traceParams:
			desc:	The pupil-trace parameters.
			type:	dict
	"""

	assert(exp == 'expX')
	# First create separate plots for the two experiments
	Plot.new(size=(10,5))
	plt.subplots_adjust(wspace=0)
	i = 1
	for _exp in ['exp1', 'exp2']:
		_dm = dm.select('exp == "%s"' % _exp)
		plt.subplot(1, 2, i); i+= 1
		plt.ylim(.91, 1.01)
		plt.xticks(range(0, 4001, 1000))
		if _exp == 'exp2':
			plt.gca().yaxis.set_ticklabels([])
			plt.title('b) Experiment 2')
		else:
			plt.ylabel('Pupil size (norm.)')
			plt.title('a) Experiment 1')
		plt.xlabel('Time since cue offset (ms)')
		plt.axhline(1, linestyle=':', color='black')
		pupilTracePlot(_dm, subplot=True, model=model, suffix='.lmer.%s' % _exp)
		plt.legend(frameon=False, loc='lower right')
	Plot.save('pupilTraceExp')
	# Create one overall plot
	Plot.new(size=(4,4))
	plt.title('b) Pupil-size trace across both experiments')
	pupilTracePlot(dm, subplot=True, model=model, suffix='.lmer.expGrand')
	plt.ylim(.91, 1.01)
	plt.xticks(range(0, 4001, 1000))
	plt.ylabel('Pupil size (norm.)')
	plt.xlabel('Time since cue offset (ms)')
	plt.axhline(1, linestyle=':', color='black')
	plt.legend(frameon=False, loc='lower right')	
	Plot.save('pupilTraceExp.grand')

@validate
def pupilTracePlotCue(dm, traceParams=defaultTraceParams):

	"""
	desc:
		Plots the pupil trace during the retention interval, separately for cue-
		on-bright and cue-on-dark trials, and separately for cue 1 and 2.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix

	keywords:
		traceParams:
			desc:	The pupil-trace parameters.
			type:	dict
	"""

	assert(exp == 'expX')
	# First create separate plots for the two experiments
	Plot.new(size=(10,5))
	plt.subplots_adjust(wspace=0)
	i = 1
	for memCue in [1, 2]:
		_dm = dm.select('memCue == %d' % memCue)
		plt.subplot(1, 2, i); i+= 1
		plt.ylim(.91, 1.01)
		plt.xticks(range(0, 4001, 1000))
		if memCue == 2:
			plt.gca().yaxis.set_ticklabels([])
			plt.title('b) Remember second')
		else:
			plt.ylabel('Pupil size (norm.)')
			plt.title('a) Remember first')
		plt.xlabel('Time since cue offset (ms)')
		plt.axhline(1, linestyle=':', color='black')
		pupilTracePlot(_dm, subplot=True, model=model,
			suffix='.lmer.cue%d' % memCue)
		plt.legend(frameon=False, loc='lower right')
	Plot.save('pupilTraceCue')

@validate
def pupilTracePlotColorClass(dm, suffix='', traceParams=defaultTraceParams):

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

	dm = dm.select('trialType == "memory"')
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
	Plot.save('pupilTraceColorClass'+suffix)

def pupilTracePlotColorClassExp(dm, suffix='', traceParams=defaultTraceParams):

	assert(exp == 'expX')
	pupilTracePlotColorClass(dm.select('exp == "exp1"'), suffix='.exp1')
	pupilTracePlotColorClass(dm.select('exp == "exp2"'), suffix='.exp2')

@validate
def pupilTracePlotIndividual(dm, traceParams=defaultTraceParams):

	"""
	desc:
		Plots the pupil-trace difference during the retention interval,
		separately for each participant.

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix

	keywords:
		traceParams:
			desc:	The pupil-trace parameters.
			type:	dict
	"""

	Plot.new(Plot.r)
	dm = dm.select('trialType == "memory"')
	i = 0
	l = []
	for _dm in dm.group('subject_nr'):
		i += 1
		print('pp%d' % i)
		x1, y1, err1 = tk.getTraceAvg(_dm.select(q1, verbose=False),
			**traceParams)
		x2, y2, err2 = tk.getTraceAvg(_dm.select(q2, verbose=False),
			**traceParams)
		# Positive effects positive
		d = y2-y1
		plt.fill_between(x1, d, color=blue[1], alpha=.1)
		l.append(d)
	for d in l:
		plt.plot(x1, d, color=blue[2], linewidth=.5)
	plt.axhline(0, color='black')
	x1, y1, err1 = tk.getTraceAvg(dm.select(q1, verbose=False),
		**traceParams)
	x2, y2, err2 = tk.getTraceAvg(dm.select(q2, verbose=False),
		**traceParams)
	# Positive effects positive
	d = y2-y1
	plt.plot(x1, d, color='black')
	plt.ylim(-.1, .1)
	plt.ylabel('Pupil-size effect')
	plt.xlabel('Time (ms)')
	Plot.save('pupilTraceIndividual')

@cachedPickle
def pupilEffect(dm, i=None, traceParams=defaultTraceParams):

	x1, y1, err1 = tk.getTraceAvg(dm.select(q1, verbose=False),
		**traceParams)
	x2, y2, err2 = tk.getTraceAvg(dm.select(q2, verbose=False),
		**traceParams)
	# Positive effects positive
	d = y2-y1
	if i is None:
		i = np.argmin(d)
	return d[i], i

def subjectDiffMatrix(dm, win=(900, 1100)):

	@cachedDataMatrix
	def getMatrix(dm):
		dm = dm.select('trialType == "memory"')
		l = [['subject_nr', 'pupil_bright', 'pupil_dark', 'pupil_diff']]
		for subject_nr, _dm in dm.walk('subject_nr'):
			print(subject_nr)
			x1, y1, err1 = tk.getTraceAvg(_dm.select(q1, verbose=False),
				**defaultTraceParams)
			x2, y2, err2 = tk.getTraceAvg(_dm.select(q2, verbose=False),
				**defaultTraceParams)
			l.append([
				subject_nr,
				nanmean(y1[win[0]:win[1]]),
				nanmean(y2[win[0]:win[1]]),
				nanmean(y2[win[0]:win[1]]-y1[win[0]:win[1]])
				])
		_dm = DataMatrix(l)
		_dm.save('output/peakEffect.csv')
		_dm.sort('pupil_diff')
		return _dm
	_dm = getMatrix(dm, cacheId='subjectDiffMatrix')
	Plot.new(size=(4,4))
	plt.title('a) Individual-participant data')
	plt.axhline(0, color='black')
	x = np.arange(0, len(_dm))-.5
	for i, y in enumerate(_dm['pupil_diff']):
		if y > 0:
			color = green[1]
		else:
			color = red[1]
		plt.bar(x[i], y, width=1., color=color)
	plt.xticks(range(0, 30, 1), [1]+['']*8+[10]+['']*9+[20]+['']*9+[30])
	plt.xlim(-1, 30)
	plt.ylim(-.1, .05)
	plt.yticks([-.1, -.05, 0, .05])
	plt.xlabel('Participant')
	plt.ylabel('Pupil-size difference (dark - bright)')
	Plot.save('subjectDiffMatrix')

def sortedHeatmap(dm):

	dm = dm.select('trialType == "memory"')
	@cachedArray
	def getMatrix():
		a = np.zeros( (dm.count('subject_nr'), traceLen) )
		for i, _dm in enumerate(dm.group('subject_nr')):
			print(i)
			x1, y1, err1 = tk.getTraceAvg(_dm.select(q1, verbose=False),
				**defaultTraceParams)
			x2, y2, err2 = tk.getTraceAvg(_dm.select(q2, verbose=False),
				**defaultTraceParams)
			a[i] = y2-y1
		order = np.argsort(nanmedian(a[:,1000:], axis=1))
		print(order)
		a = a[order]
		return a
	a = getMatrix(cacheId='sortedHeatmap')
	for i in range(traceLen):
		a[:,i].sort()
	Plot.new(size=Plot.w)
	plt.imshow(a, aspect='auto', cmap='seismic', interpolation='none',
		vmin=-.075, vmax=.075)
	plt.colorbar()
	Plot.save('heatmap')

# def behavPupilLmer(dm):
#
# 	dm = dm.select('trialType == "memory"').select('correct == 1')
# 	m = 'targetLum*response_time + (1+targetLum+response_time|subject_nr)'
# 	dm['response_time'] /= dm['response_time'].std()
# 	mm = tk.mixedModelTrace(dm, m, winSize=250, cacheId='behavPupilLmer',
# 		**defaultTraceParams)
# 	tk.statsTrace(mm)
# 	plt.show()
