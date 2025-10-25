from datetime import datetime, date, timedelta
import time
import functools
import numpy
import sys
import hashlib
import pandas
import importlib
import inspect

def roundup(nn,dp=2):
	rounded = round(nn,dp)
	if(rounded>=nn):
		return rounded
	else:
		return rounded+pow(10,-dp)
	
def rounddown(nn,dp=2):
	rounded = round(nn,dp)
	if(rounded<=nn):
		return rounded
	else:
		return rounded-pow(10,-dp)
	
def extractvalues(src_map, key_vec):
	return { key:src_map[key] for key in key_vec if(key in src_map) }

def extractvalues_noskip(src_map, key_vec, defval=None):
	return { key:src_map.get(key,defval) for key in key_vec }

# --
# --
# --
def inrange(it,*,lt=None,le=None,gt=None,ge=None):
	left_cond = None
	right_cond = None
	# --
	# -- 'it' is either ndarray or pandas type
	# --
	if(ge is not None):
		left_cond = ge <= it
	if(gt is not None):
		left_cond = gt < it
	if(le is not None):
		right_cond = it <= le
	if(lt is not None):
		right_cond = it < lt
	return left_cond & right_cond

def inrange_q(it,*,lt=None,le=None,gt=None,ge=None):
	if(lt is not None):
		lt = it.quantile(lt)
	if(le is not None):
		le = it.quantile(le)
	if(gt is not None):
		gt = it.quantile(gt)
	if(ge is not None):
		ge = it.quantile(ge)
	return inrange(it,lt=lt,le=le,gt=gt,ge=ge)

def is_none(val):
	return val is None

def is_not_none(val):
	return val is not None

def default_val(val,defval,cmp=is_not_none):
	if(cmp(val)):
		return val
	return repl 

def apply_func(val,func,cmp=is_none):
	if(cmp(val)):
		return None
	return func(val)

def date_only(dt):
	return apply_func(dt,datetime.date)

def if_else(cond,true_val,false_val):
	if(cond):
		return true_val
	else:
		return false_val

# --
# --
# --
def today():
	return date.today()

def days_between(dt_s, dt_b):
	difference = dt_b - dt_s
	return difference.days

def days_away(dt, days):
	return dt + timedelta(days=days)

# --
# -- str: python str
# -- dt: python datetime
# -- dt64: numpy datetime64
# -- ts: pandas.Timestamp
# --
def str_to_dt(val,fmt='%Y-%m-%d'):
	try:
		return datetime.strptime(val, fmt)
	except TypeError as err:
		print(type(val),val)
		print(err)
		return str(val)

def str_to_dt64(val):
	try:
		return numpy.datetime64(val)
	except TypeError as err:
		print(type(val),val)
		print(err)
		return str(val)

def str_to_ts(val):
	try:
		return pandas.Timestamp(ts_input=val)
	except TypeError as err:
		print(type(val),val)
		print(err)
		return str(val)
# --
def dt_to_str(val,delimiter='-'):
	try:
		return val.strftime('%Y{0}%m{0}%d'.format(delimiter))
	except TypeError as err:
		print(type(val),val)
		print(err)
		return str(val)

def dt_to_dt64(val):
	try:
		return numpy.datetime64(val)
	except TypeError as err:
		print(type(val),val)
		print(err)
		return str(val)

def dt_to_ts(val):
	try:
		return pandas.Timestamp(ts_input=val)
	except TypeError as err:
		print(type(val),val)
		print(err)
		return str(val)
# --
def dt64_to_str(val,delimiter='-'):
	try:
		# --
		# -- datetime_as_string use '-' as delimiter
		# --
		return numpy.datetime_as_string(val, unit='D').replace('-',delimiter)
	except TypeError as err:
		print(type(val),val)
		print(err)
		return str(val)

def dt64_to_dt(val):
	try:
		# ts = (val - numpy.datetime64('1970-01-01T00:00:00Z')) / numpy.timedelta64(1, 's')
		# return datetime(int(ts)) # dropping the micro seconds
		return str_to_dt( dt64_to_str(val) )
	except TypeError as err:
		print(type(val),val)
		print(err)
		return str(val)

def dt64_to_ts(val):
	pass

def ts_to_str(val):
	pass

def ts_to_dt(val):
	pass

def ts_to_dt64(val):
	pass

def dt_conv(from_val=None,to_type='str'):
	if(from_val is None):
		return None
	# --
	from_type = None
	if(isinstance(from_val,(datetime,date))):
		from_type = 'dt'
	elif(isinstance(from_val,(str))):
		from_type = 'str'
	elif(isinstance(from_val,(numpy.datetime64))):
		from_type = 'dt64'
	elif(isinstance(from_val,(pandas.Timestamp))):
		from_type = 'ts'
	# --
	if(from_type==to_type):
		return from_val
	# --
	converter = make_callable( m_name=__name__, f_name="{0}_to_{1}".format(from_type,to_type) )
	return converter(from_val)

# --
# --
# --
def reload_module(module_name):
	try:
		module = importlib.import_module(module_name)
		importlib.reload(module)
		print(f"Module {module_name} reloaded.")
	except ModuleNotFoundError:
		print(f"Module {module_name} not found.")

# --
# --
# --
def clear_cache():
	make_callable.cache_clear()

@functools.lru_cache(maxsize=200)
def make_callable(f_name,m_name=None):
	if(m_name is not None):
		if(m_name not in sys.modules):
			importlib.import_module(m_name)
		return getattr( sys.modules[ m_name ], f_name )
	names = f_name.split('.')
	if(len(names)==1):
		return getattr( sys.modules[ '__main__' ], f_name )
	else:
		m_name = '.'.join(names[:-1])
		f_name = names[-1]
		if(m_name not in sys.modules):
			importlib.import_module(m_name)
		return getattr( sys.modules[ m_name ], f_name )

def callable_fq_name(func):
	return ".".join([ func.__module__,func.__name__ ])
# --
# --
# --
def shortname(fname):
	keychain = fname.split('/')
	if(keychain[-1].isdigit()):
		return '/'.join(keychain[-2:])
	else:
		return keychain[-1]

def shortnames(*fnames):
	briefs = []
	for fname in fnames:
		briefs.append(shortname(fname))
	return briefs

# --
# --
# --
def rename_columns(df,cols_name):
	if(cols_name is not None):
		df.rename( columns=lambda ii:cols_name[ii],inplace=True )
	return df

# --
# -- add list2 to list1, keep order intact, eliminate dup
# !! list1 is modified
# --
def concat_lists(lst1,lst2):
	for ele in lst2:
		if(ele in lst1):
			continue
		lst1.append(ele)
	return lst1

# --
# --
# --
def retry(fn,retry=10,exceptTypes=(Exception),pause=1,rtnEx=False,silent=True,cooldown=None):
	exceptions = []
	for _ in range(0,retry):
		try:
			outcome = fn()
			if(rtnEx):
				return ( outcome, exceptions )
			else:
				return outcome
		except exceptTypes as ex:
			if(not silent):
				print(inspect.stack()[1].code_context)
				print(ex)
			exceptions.append( ex )
			if(cooldown is None):
				time.sleep(pause)
			else:
				countdown(cooldown,desc="Cooldown")
	if(rtnEx):
		return ( None, exceptions )
	else:
		raise exceptions[-1]

def countdown(seconds,desc="Countdown"):
	# --
	from tqdm.notebook import tqdm
	# --
	progress_bar = tqdm(range(seconds, 0, -1), desc=desc, unit="s", leave=False)
	for i in progress_bar:
		time.sleep(1)
	progress_bar.close()

# --
# -- Reads a file and returns its numeric content as an integer, 
# -- or None if the file is empty or non-numeric.
# --
def read_numeric_from_file(fname):
	try:
		with open(fname, 'r') as file:
			content = file.read().strip()
			if content.isdigit():
				print(f'The file {fname} found, Using value {content}.')
				return int(content)
			else:
				print(f'The file {fname} found, but cannot interpret content. Using None.')
				return None
	except FileNotFoundError:
		print(f"The file {fname} does not exist.")
		return None

# -- 
# -- Creates an empty file with the given name 'fname', 
# -- and if the file exists, empties its content.
# -- 
def create_or_empty_file(fname):
    with open(fname, 'w') as file:
        pass  # Opening the file in 'w' mode will create it if it doesn't exist, or empty it if it does.

# --
# -- Writes the current Unix timestamp to a file.
# --
def write_current_time_to_file(fname):
    # Get the current Unix timestamp
    current_time = int(time.time())
    
    # Write the timestamp to the file
    with open(fname, 'w') as file:
        file.write(str(current_time))

# --
# -- example: types_validate(base,msg="base",types=[ type([]) ],allow_none=False)
# -- must be a list(), and cannot be None; otherwise throw ValueError
# --
def types_validate(obj, types=[], msg="obj", raise_on_err=True, allow_none=True):
	if(allow_none and obj is None):
		return True
	if(type(obj) in types):
		return True
	if(raise_on_err):
		raise ValueError(f"ERR:{msg}:Only applicable to {types}, found {type(obj)}")
	return False
	
