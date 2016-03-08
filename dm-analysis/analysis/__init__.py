# coding=utf-8

import sys

if '--exp1' in sys.argv:
	exp = 'exp1'
elif '--exp2' in sys.argv:
	exp = 'exp2'
elif '--exp3' in sys.argv:
	exp = 'exp3'
elif '--expX' in sys.argv:
	exp = 'expX'
else:
	raise Exception('Please specify an experiment')
