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

import sys
import math
from exparser import TraceKit as tk
from exparser import Plot
from exparser.TangoPalette import *
from exparser.Cache import cachedDataMatrix
from exparser.PivotMatrix import PivotMatrix
from yamldoc import validate
from matplotlib import pyplot as plt
import warnings

defaultTraceParams = {
	'signal'		: 'pupil',
	'lock'			: 'start',
	'phase'			: 'retention',
	'baseline'		: 'cue',
	'baselineLock'	: 'end',
	'traceLen'		: 5000
	}

show = '--show' in sys.argv
brightColor = orange[1]
darkColor = blue[1]
validExp = 'exp1', 'exp2' # Known experiment codes

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
	subplot=False):

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
	"""

	if exp == 'exp2':
		dm = dm.select('trialType == "memory"')
	dmBright = dm.select('targetLum == "bright"')
	dmDark = dm.select('targetLum == "dark"')
	xBright, yBright, errBright = tk.getTraceAvg(dmBright, **traceParams)
	xDark, yDark, errDark = tk.getTraceAvg(dmDark, **traceParams)
	if not subplot:
		Plot.new()
	plt.fill_between(xBright, yBright-errBright[0], yBright+errBright[0],
		color=brightColor, alpha = .25)
	plt.fill_between(xDark, yDark-errDark[0], yDark+errDark[0],
		color=darkColor, alpha = .25)
	plt.plot(yBright, color=brightColor)
	plt.plot(yDark, color=darkColor)
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
