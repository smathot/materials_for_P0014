# Experimental resources for P0014.1+2

Copyright 2015 Sebastiaan Mathôt, Elle Van Heusden, and Stefan Van der Stigchel

- <s.mathot@cogsci.nl>
- <http://www.cogsci.nl/smathot>

# About this repository

This repository contains materials to accompany the following manuscript:

Mathôt, S., Van Heusden, E., Van der Stigchel. (in prep.) *Attending and inhibiting stimuli that match the contents of visual working memory: Evidence
from eye movements and pupillometry*.

# Folder structure

- `exp1` containts the analysis and experiment file for Experiment 1
- `exp2` containts the analysis and experiment file for Experiment 2.
	- *Note:* During testing, Exp. 2 was divided into two separate sessions of 27 practice trials and 81 experimental trials. The experiment included here is the original one-session version, which is otherwise identical.
- `crossexperimental` contains the analysis for the crossexperimental analysis
- `manuscript` the manuscript source files
- `misc` the color coordinates and JASP source file used for the Bayesian analyses.

# Dependencies

- OpenSesame 2.9.X for the experiments
	- http://osdoc.cogsci.nl/
- JASP for the analysis
	- https://jasp-stats.org/
- exparser for the analysis
	- https://github.com/smathot/exparser
- yamldoc for automatic validation of the analysis functions
	- https://github.com/smathot/python-yamldoc
- Python 2.7 and the standard scipy stack (numpy, matplotlib, etc.)

# Running the analysis

1. Convert all `exp[X]/data/edf/*.edf` to `.asc` files using the `edf2asc` tool provided by SR Research.
2. Move the `.asc` files to `crossexperimental/data/exp[X]/*.asc`.
3. Open a terminal in `crossexperimental/data`
4. Run `python analyze.py @full --clear-cache`

This will produce a lot of output in the terminal, most of which is not terribly important. The main results will be written to two automatically created subfolders: `plot` and `output`

# License

- Analysis and experimental code are released under a [GNU General Public License 3](https://www.gnu.org/copyleft/gpl.html).
- Data and text are released under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
