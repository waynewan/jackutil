from datetime import datetime, date
import functools
import numpy
import sys
import hashlib
import pandas
import importlib

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

# --
# -- str: python str
# -- dt: python datetime
# -- dt64: numpy datetime64
# -- ts: pandas.Timestamp
# --
def str_to_dt(val):
	try:
		return datetime.strptime(val, '%Y-%m-%d')
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
def dt64_to_str(val):
	try:
		return numpy.datetime_as_string(val, unit='D')
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

