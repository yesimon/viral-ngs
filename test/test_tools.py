# Unit tests for tools/__init__.py

__author__ = "dpark@broadinstitute.org"

import tools
from tools import *
import unittest, tempfile, shutil, os, logging
import util.cmd

log = logging.getLogger(__name__)

def set_tmpDir(name):
	proposed_prefix = ['tmp']
	if name:
		proposed_prefix.append(name)
	for e in ('LSB_JOBID','LSB_JOBINDEX'):
		if e in os.environ:
			proposed_prefix.append(os.environ[e])
	tempfile.tempdir = tempfile.mkdtemp(prefix='-'.join(proposed_prefix)+'-',
		dir=util.cmd.find_tmpDir())
def destroy_tmpDir():
	shutil.rmtree(tempfile.tempdir)

class TestToolsInstallation(unittest.TestCase):
	def setUp(self):
		set_tmpDir('TestToolsInstallation')
		util.cmd.setup_logger('INFO')
	def tearDown(self):
		destroy_tmpDir()
	def testAllToolInstallers(self):
		def iter_leaf_subclasses(aClass) :
			"Iterate over subclasses at all levels that don't themselves have a subclass"
			isLeaf = True
			for subclass in aClass.__subclasses__() :
				isLeaf = False
				for leafClass in iter_leaf_subclasses(subclass) :
					yield leafClass
			if isLeaf :
				yield aClass
		'''Load every tool's default chain of install methods and try them.'''
		for tool_class in iter_leaf_subclasses(tools.Tool):
			t = tool_class()
			t.install()
			self.assertTrue(t.is_installed(), "installation of tool %s failed" % tool_class.__name__)
			log.info(".. installation of %s succeeded with installer %s" % (tool_class.__name__, t.installed_method.__class__.__name__))
			
