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

def subjectDiffTraces(dm, traceParams=defaultTraceParams):

	pupil = np.empty( (dm.count('groupKey'), traceParams['traceLen']),
		dtype=float)
	for i, (subject_nr, _dm) in enumerate(dm.walk('groupKey')):
		x1, y1, err1 = tk.getTraceAvg(_dm.select(q1, verbose=False),
			**traceParams)
		x2, y2, err2 = tk.getTraceAvg(_dm.select(q2, verbose=False),
			**traceParams)
		pupil[i] = y1-y2
	return pupil

def corrTrace(dm, dv='correct', traceParams=defaultTraceParams):
	dmAtt = dm.select('trialType == "attention"')
	dmMem = dm.select('trialType == "memory"')
	behav = np.empty(dmAtt.count('groupKey'), dtype=float)
	for i, (subject_nr, _dm) in enumerate(dmAtt.walk('groupKey')):
		if dv == 'response_time':
			_dm = _dm.select('correct == 1')
		match = _dm.select('attMatch == 1')[dv].mean()
		nonMatch = _dm.select('attMatch == 0')[dv].mean()
		if dv == 'correct':
			behav[i] = match-nonMatch
		else:
			behav[i] = nonMatch-match
	print(behav)
	pupil = subjectDiffTraces(dmMem, traceParams)
		# cacheId='.subjectDiffTraces')
	ar = np.empty(traceParams['traceLen'], dtype=float)
	ap = np.empty(traceParams['traceLen'], dtype=float)
	for _i in range(pupil.shape[1]):
		s, i, r, p, se = linregress(behav, pupil[:,_i])
		ar[_i] = r
		ap[_i] = p
	return ar, ap

def corrPlot(dm, traceParams=defaultTraceParams):

	dm = dm.addField('groupKey', dtype=str)
	dm['groupKey'] = dm['subject_nr']
	Plot.new(Plot.r)
	plt.xlabel('Time (ms)')
	plt.ylabel('R(pupil - behavior)')
	ar, ap = corrTrace(dm, dv='correct')
	plt.plot(ar, color=orange[1], label='accuracy')
	ar, ap = corrTrace(dm, dv='response_time')
	plt.plot(ar, color=blue[1], label='response time')
	plt.xlim(0, traceParams['traceLen'])
	plt.legend(frameon=False)
	Plot.save('corrTrace', show=show)
