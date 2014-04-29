#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
This file is part of OpenSesame Git Demo.

OpenSesame Git Demo is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame Git Demo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame Git Demo.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import git
import tarfile
import time

# The name of the source script and file pool
scriptName = u'P0014.1 [Pupil size and working memory].opensesame'
poolFolder = u'__pool__'
# The export names. We include the latest commit hash and time in the file name.
exportFolder = u'export'
exportName = u'P0014.1 Pupil size and working memory [#%s %s].opensesame.tar.gz' % (
	unicode(git.Repo(u'.').head.commit)[:10], time.strftime(u'%c'))
# Create the export folder if it doesn't exist yet
if not os.path.exists(exportFolder):
	os.makedirs(exportFolder)
print(u'Exporting to %s ...' % os.path.join(exportFolder, exportName))
# Create a new .opensesame.tar.gz file and add the script and file pool. The
# script has to be named `script.opensesame` and the file-pool folder has to be
# named `pool`.
tf = tarfile.open(os.path.join(exportFolder, exportName), u'w:gz')
print(u'Adding script.opensesame')
tf.add(scriptName, u'script.opensesame')
print(u'Adding file pool')
tf.add(poolFolder, u'pool')
tf.close()
print(u'Done!')
