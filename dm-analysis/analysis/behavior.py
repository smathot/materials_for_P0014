# coding=utf-8

from analysis.constants import *


def cuing_effect(dm):

	assert(analysis.exp == 'exp3')
	glm_acc = lme4.glmer(dm, 'correct ~ congruency + (1+congruency|subject_nr)',
		family='binomial')
	print(glm_acc)
	io.writetxt(glm_acc, 'output/exp3/glmer_acc.csv')
	lm_rt = lme4.lmer(dm.correct == 1,
		'response_time ~ congruency + (1+congruency|subject_nr)')
	print(lm_rt)
	io.writetxt(lm_rt, 'output/exp3/lmer_rt.csv')

	print('Correct RTs')
	pm = ops.pivot_table(dm.correct == 1, values='response_time', index='subject_nr',
		columns='congruency')
	print(pm)
	io.writetxt(pm, 'output/exp3/pivot_rt.csv')
	print('\nAccuracy')
	print('%.2f vs %.2f' % (pm._0.mean, pm._1.mean))
	pm = ops.pivot_table(dm, values='correct', index='subject_nr',
		columns='congruency')
	print(pm)
	io.writetxt(pm, 'output/exp3/pivot_acc.csv')
	print('%.2f vs %.2f' % (pm._0.mean, pm._1.mean))

	print('Correct RTs')
	pm = ops.pivot_table(dm.correct == 1, values='response_time', index='subject_nr',
		columns=['congruency', 'memCue'])
	print(pm)
	io.writetxt(pm, 'output/exp3/pivot_rt-by-cue.csv')
	print('\nAccuracy')
	pm = ops.pivot_table(dm, values='correct', index='subject_nr',
		columns=['congruency', 'memCue'])
	print(pm)
	io.writetxt(pm, 'output/exp3/pivot_acc-by-cue.csv')
