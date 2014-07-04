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
from yamldoc import validate
from matplotlib import pyplot as plt

defaultTraceParams = {
	'signal'		: 'retention',
	'lock'			: 'start',
	'phase'			: 'trial',
	'baseline'		: 'cue',
	'baselineLock'	: 'end',
	'traceLen'		: 5000
	}

show = '--silent' not in sys.argv
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
	print dm.columns()
	dm = dm.select('practice == "no"')
	# Gaze error must be smaller than maximum displacement of stabilizer.
	dm = dm.select('maxGazeErr < 1024/6')
	return dm

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
