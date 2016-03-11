#!/usr/bin/env python3
# coding=utf-8

from datamatrix import dispatch
from analysis import parse, pupil, gaze, main, behavior, corr
import analysis

dm = dispatch.waterfall(
	(parse.eyelink_parser, 'data-%s' % analysis.exp, {'exp' : analysis.exp}),
	(main.preprocess, 'preprocess-%s' % analysis.exp, {})
	)
dispatch.dispatch(dm, modules=[pupil, gaze, main, behavior, corr])
