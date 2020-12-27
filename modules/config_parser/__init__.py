import imp
import glob
import traceback

from os.path      import dirname, basename, isfile
from core.loggers import log
from core.utils   import is_binary_file

modules = {}

for f in glob.glob(dirname(__file__)+"/*.py"):
	name = basename(f)[:-3]
	if name != '__init__':
		modules[name] = imp.load_source(name, f)

def match(filename):
	result = []
	for name, mod in modules.items():
		if mod.match(filename):
			result.append(name)
		
	return result

def run(filename, args):
	result  = []
	disable = {}

	for name in args.disable:
		disable[name] = True

	if is_binary_file(filename):
		return result

	for name, mod in modules.items():		
		if name not in disable and mod.match(filename):
			try:
				for row in mod.run(filename):
					row['module']   = name
					row['filename'] = filename
					result.append(row)
			except Exception as e:
				log.debug("Exception while running %s against %s\n%s", name, filename, traceback.format_exc())
				pass

	return result