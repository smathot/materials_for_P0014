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

def gazeDev(dm, suffix=''):

	_model = 'maxGazeDev ~ probePosTarget + (1+probePosTarget|subject_nr)'

	# Gaze error must be smaller than maximum displacement of stabilizer.
	print('Overall:')
	_dm = dm.select('trialType == "memory"')
	pm = PivotMatrix(_dm, ['probePosTarget'], ['subject_nr'], dv='maxGazeDev')
	print(pm)
	pm.save('output/gazeDev%s.csv' % suffix)
	if exp != 'expX':
		return
	Plot.new(size=(10,5))
	plt.subplots_adjust(wspace=0)
	for i, _exp in enumerate(('exp1', 'exp2')):
		__dm = _dm.select('exp == "%s"' % _exp)
		RBridge.R().load(__dm)
		lm = RBridge.R().lmer(_model)
		print(lm)
		lm.save('output/lmer.%s.gazeDev%s.csv' % (_exp, suffix))
		plt.subplot(1,2,i+1)
		plt.xlabel('Maximum gaze deviation (deg.)')
		ecc = 7.3
		if _exp == 'exp2':
			ecc *= .95
			plt.gca().yaxis.set_ticklabels([])
			plt.title('b) Experiment 2')
		else:
			plt.ylabel('Frequency (norm.)')
			plt.title('a) Experiment 1')
		plt.xticks([-256, 0, 256], [
			'Distractor probe\n-%.1f' % ecc,
			'Center\n0',
			'Memory-match probe\n%.1f' % ecc])
		__dm['maxGazeDev'][__dm.where('probePosTarget == "left"')] *= -1
		plt.xlim(-400, 400)
		plt.axvspan(-170, 170, color=gray[1], zorder=-1000)
		plt.axvline(0, linestyle=':', color='black')
		plt.axvline(-256, linestyle=':', color='black')
		plt.axvline(256, linestyle=':', color='black')
		y, edges = np.histogram(__dm['maxGazeDev'], bins=50, range=(-400, 400))
		y.dtype = float
		y /= y.max()
		x = .5*edges[1:]+.5*edges[:-1]
		plt.fill_between(x, y, color=blue[1])
	Plot.save('maxGazeDev%s' % suffix)
