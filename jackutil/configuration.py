import copy 
from .containerutil import projectContainer,containerKeys,containerVariations

# --
# --
# --
class configuration:
	def __init__(self,*,basespec,variations):
		self.__basespec = basespec
		self.__variations = variations
	# --
	# --
	# --
	def __read_basespec(self): return self.__basespec
	basespec = property(__read_basespec,None,None)
	def __read_variations(self): return self.__variations
	variations = property(__read_variations,None,None)
	# --
	# !! do not use yield, because unlikely to have large # of configuration
	# --
	def all_configurations(self,*,auto_expand=False):
		all_specs = []
		for path_val_map in self.all_variations():
			base_spec = self.__basespec
			base_spec = copy.deepcopy(self.__basespec)
			final_spec = projectContainer(base_spec,path_val_map,auto_expand)
			all_specs.append(final_spec)
		return all_specs 

	def all_variations(self):
		return containerVariations(self.__variations)

	def keys(self):
		return containerKeys(self.__variations)
