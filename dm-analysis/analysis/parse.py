# coding=utf-8

import warnings
from analysis.constants import *
from eyelinkparser import EyeLinkParser, sample


class CustomParser(EyeLinkParser):

	def parse_phase(self, l):

		if self.current_phase in ('cue', 'retention', 'preAttProbe') \
			or 'cue' in l or 'retention' in l or 'preAttProbe' in l:
				s = sample(l)
				if s is None or s.t % DOWNSAMPLE == 0:
					EyeLinkParser.parse_phase(self, l)

	def end_phase(self):

		if len(self.ptrace) > MAXDEPTH:
			warnings.warn('Very long trace, truncating to 5000: %s (%d)' \
				% (self.current_phase, len(self.ptrace)))
			self.ptrace = self.ptrace[:MAXDEPTH]
			self.xtrace = self.xtrace[:MAXDEPTH]
			self.ytrace = self.ytrace[:MAXDEPTH]
		EyeLinkParser.end_phase(self)


@cached
def eyelink_parser(exp):

	if exp != 'expX':
		return CustomParser(folder='data/%s' % exp).dm

	exp1 = io.readpickle('.cache/gaze-data-exp1.pkl')
	exp1.task_ref1 = 'B_memory'
	exp1.task_ref2 = 'A_memory'
	exp2 = io.readpickle('.cache/gaze-data-exp2.pkl')
	exp2.task_ref1 = 'B_memory'
	exp2.task_ref2 = 'A_memory'
	exp2 = exp2.trialType == 'memory'
	exp3 = io.readpickle('.cache/gaze-data-exp3.pkl')
	exp3.exp = 'exp3'
	exp3.task_ref1 = 'A_attention'
	exp3.task_ref2 = 'B_attention'
	dm = exp1 << exp2 << exp3
	dm.pupil.depth = DEPTH_EXP3
	dm.xgaze.depth = DEPTH_EXP3
	io.writepickle(dm, '.cache/gaze-data-expX.pkl')

	from analysis import main
	exp1 = main.preprocess(None, cacheid='preprocess-exp1')
	exp1.exp = 'exp1'
	exp1.task_ref1 = 'B_memory'
	exp1.task_ref2 = 'A_memory'
	exp2 = main.preprocess(None, cacheid='preprocess-exp2')
	exp2.exp = 'exp2'
	exp2.task_ref1 = 'B_memory'
	exp2.task_ref2 = 'A_memory'
	exp2 = exp2.trialType == 'memory'
	del exp2.trialType
	exp3 = main.preprocess(None, cacheid='preprocess-exp3')
	exp3.exp = 'exp3'
	exp3.task_ref1 = 'A_attention'
	exp3.task_ref2 = 'B_attention'
	dm = exp1 << exp2 << exp3
	dm.pupil.depth = DEPTH_EXP3
	dm.xgaze.depth = DEPTH_EXP3
	return dm
