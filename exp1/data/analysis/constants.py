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
from exparser.DataMatrix import DataMatrix
from exparser.TangoPalette import *
from exparser.Cache import cachedDataMatrix, cachedArray, cachedPickle
from exparser.PivotMatrix import PivotMatrix
from exparser import RBridge
from yamldoc import validate
from matplotlib import pyplot as plt
from scipy.stats import linregress, nanmedian, nanmean, ttest_1samp
import warnings
import numpy as np
import os

traceLen = 5000

smoothParams = {
	'windowLen' : 31
	}

defaultTraceParams = {
	'signal'		: 'pupil',
	'lock'			: 'start',
	'phase'			: 'retention',
	'baseline'		: 'cue',
	'baselineLock'	: 'end',
	'traceLen'		: traceLen,
	'smoothParams'	: smoothParams
	}

attentionTraceParams = {
	'signal'		: 'pupil',
	'lock'			: 'start',
	'phase'			: 'preAttProbe',
	'baseline'		: 'cue',
	'baselineLock'	: 'end',
	'traceLen'		: traceLen,
	'smoothParams'	: smoothParams
	}

exp3TraceParams = defaultTraceParams.copy()
exp3TraceParams['traceLen'] = 2500

gazeParams = {
	'signal'		: 'x',
	'lock'			: 'start',
	'phase'			: 'retention',
	'traceLen'		: traceLen,
	'smoothParams'	: smoothParams
	}

show = '--show' in sys.argv
brightColor = orange[1]
darkColor = blue[1]
validExp = 'exp1', 'exp2', 'exp3', 'expX' # Known experiment codes
colorClasses = 'red', 'green', 'blue'
model = 'targetLum + (1+targetLum|subject_nr)'
gazeModel = 'probePosTarget + (1+probePosTarget|subject_nr)'
winSize = 100
q1 = 'targetLum == "bright"'
q2 = 'targetLum == "dark"'
gq1 = 'probePosTarget == "left"'
gq2 = 'probePosTarget == "right"'
