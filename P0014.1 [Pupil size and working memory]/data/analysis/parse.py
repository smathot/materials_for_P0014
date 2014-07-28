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
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.Cache import cachedDataMatrix
import numpy as np

# Display center
xc = 512
yc = 384

class MyReader(EyelinkAscFolderReader):

	"""An experiment-specific reader to parse the EyeLink data files."""

	def initTrial(self, trialDict):

		"""
		desc:
			Performs pre-trial initialization.

		arguments:
			trialDict:
				desc:	Trial information.
				type:	dict
		"""

		trialDict['maxGazeErr'] = 0
		trialDict['stabErr'] = 0
		self.stabShift = []

	def finishTrial(self, trialDict):

		"""
		desc:
			Performs post-trial initialization.

		arguments:
			trialDict:
				desc:	Trial information.
				type:	dict
		"""

		sys.stdout.write('.')
		sys.stdout.flush()
		trialDict['meanStabShift'] = np.mean(self.stabShift)

	def parseLine(self, trialDict, l):

		"""
		desc:
			Parses a single line from the EyeLink .asc file.

		arguments:
			trialDict:
				desc:	Trial information.
				type:	dict
			l:
				desc:	A white-space-splitted line.
				type:	list
		"""

		if self.tracePhase == 'retention':
			fix = self.toFixation(l)
			if fix != None:
				trialDict['maxGazeErr'] = max(trialDict['maxGazeErr'],
					np.abs(xc-fix['x']))
			if 'stabilize' in l:
				if l[3] == 'error':
					trialDict['stabErr'] += 1
				else:
					self.stabShift.append(l[3])

@cachedDataMatrix
def getDataMatrix():
	return MyReader(blinkReconstruct=True).dataMatrix()
