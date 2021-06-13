import os
from avsyncinator.app import logger

DATADIR = 'data' + os.sep
Log = logger.Logger.get_instance()
Log.output_function = lambda msg: None