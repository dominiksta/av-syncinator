from .. import dirsetup
from .logger import Logger

Logger.get_instance().output_function = print

dirsetup()