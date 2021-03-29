import itertools as itt
import copy 
from .containerutil import projectContainer

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
	def __read_variation(self): return self.__variations
	variations = property(__read_variation,None,None)
	# --
	# --
	# --
	def all_configurations(self):
		all_specs = []
		for path_val_map in self.all_variations():
			base_spec = self.__basespec
			base_spec = copy.deepcopy(self.__basespec)
			final_spec = projectContainer(base_spec,path_val_map)
			all_specs.append(final_spec)
		return all_specs 

	def all_variations(self):
		# --
		# --
		# --
		def _expand_tuple_keyval(key,val):
			if(isinstance(key,tuple)):
				expanded = { k:v for k,v in zip(key,val)}
				return expanded.items()
			return [ (key,val) ]
		# --
		# --
		# --
		test_val_lst = list(self.__variations.values())
		test_keys = self.__variations.keys()
		tests = list( itt.product(*test_val_lst))
		paired_tests = []
		for tuple_test in tests:
			test = { k:v for k,v in zip(test_keys,tuple_test)}
			test = { kk:vv for k,v in test.items() for kk,vv in _expand_tuple_keyval(k,v)}
			paired_tests.append(test)
		return paired_tests

	def keys(self):
		# --
		# --
		# --
		def _expand_tuple_key(key):
			if(isinstance(key,tuple)):
				return key
			return [ key ]
		# --
		# --
		# --
		return [ kk for k in self.__variations.keys() for kk in _expand_tuple_key(k) ]

