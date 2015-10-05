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

	dm = dm.select('trialType == "memory"')
	behav = np.empty(dm.count('groupKey'), dtype=float)
	for i, (subject_nr, _dm) in enumerate(dm.walk('groupKey')):
		behav[i] = _dm[dv].mean()
	print(behav)
	pupil = subjectDiffTraces(dm, traceParams)
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

def splitHalfReliability(dm, N=10000):

	@cachedDataMatrix
	def pupilEffectDm(dm):
		dm = dm.select('trialType == "memory"')
		dm = dm.select('correct == 1')
		from analysis.pupil import pupilEffect
		diff, index = pupilEffect(dm, cacheId='peakEffect')
		l = [['subject_nr', 'targetLum', 'pupilSize']]
		for i in dm.range():
			subject_nr = dm['subject_nr'][i]
			targetLum = dm['targetLum'][i]
			pupilSize = tk.getTrace(dm[i], **defaultTraceParams)[index]
			if np.isnan(pupilSize):
				continue
			l.append([subject_nr, targetLum, pupilSize])
		return DataMatrix(l)

	@cachedArray
	def _a(dm):
		_dm = pupilEffectDm(dm, cacheId='pupilEffect')
		lr = []
		for run in range(N):
			l1 = []
			l2 = []
			for subject_nr, dm in _dm.walk('subject_nr'):
				dm.shuffle()
				dmWhite = dm.select(q1, verbose=False)
				dmBlack = dm.select(q2, verbose=False)
				ldmWhite = dmWhite.explode(2)
				ldmBlack = dmBlack.explode(2)
				dmWhite1 = ldmWhite[0]
				dmBlack1 = ldmBlack[0]
				d1 = dmBlack1['pupilSize'].mean() - dmWhite1['pupilSize'].mean()
				dmWhite2 = ldmWhite[1]
				dmBlack2 = ldmBlack[1]
				d2 = dmBlack2['pupilSize'].mean() - dmWhite2['pupilSize'].mean()
				l1.append(d1)
				l2.append(d2)
				# print(subject_nr, d1, d2)
			s, i, r, p, se = linregress(l1, l2)
			print('%.5d: r = %.4f, p = %.4f' % (run, r, p))
			lr.append(r)
		return np.array(lr)

	a = _a(dm, cacheId='_a')
	a = np.sort(a)
	p = 1.*np.sum(a > 0)/len(a)
	m = a.mean()
	lo = a[int(.025*len(a))]
	hi = a[int(.975*len(a))]
	s = 'M = %.2f, P(r > 0) = %.2f, 95%%: %.2f - %.2f' % (m, p, lo, hi)
	print(s)
	Plot.new(Plot.xs)
	plt.title(s)
	plt.ylabel('Frequency (N)')
	plt.xlabel('Split-half correlation (r)')
	plt.hist(a, bins=100, color='black')
	plt.xlim(-1, 1)
	plt.axvline(0, linestyle=':', color='black')
	Plot.save('splitHalfReliability')
