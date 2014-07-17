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

	if 'no' in dm.unique('practice'):
		dm = dm.select('practice == "no"')
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

	pm = PivotMatrix(dm, ['subject_nr'], ['subject_nr'], dv='correct',
		func='size')
	pm._print('N')

@validate
def pupilTracePlot(dm, traceParams=defaultTraceParams, suffix=''):

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
	"""

	dmBright = dm.select('targetLum == "bright"')
	dmDark = dm.select('targetLum == "dark"')
	xBright, yBright, errBright = tk.getTraceAvg(dmBright, **traceParams)
	xDark, yDark, errDark = tk.getTraceAvg(dmDark, **traceParams)
	Plot.new()
	plt.plot(yBright, color=brightColor)
	plt.plot(yDark, color=darkColor)
	Plot.save('pupilTracePlot%s' % suffix, show=show)

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

	pm = PivotMatrix(dm, ['subject_nr'], ['subject_nr'], dv='correct')
	pm._print('Accuracy')
	pm.save('output/correct.csv')
	pm = PivotMatrix(dm, ['subject_nr'], ['subject_nr'], dv='response_time')
	pm._print('Response times')
	pm.save('output/response_time.csv')
