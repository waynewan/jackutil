from datetime import datetime, date
import functools
import numpy
import sys
import hashlib
import pandas

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
	return datetime.strptime(val, '%Y-%m-%d')

def str_to_dt64(val):
	return numpy.datetime64(val)

def str_to_ts(val):
	return pandas.Timestamp(ts_input=val)
# --
def dt_to_str(val):
	return val.strftime('%Y-%m-%d')

def dt_to_dt64(val):
	return numpy.datetime64(val)

def dt_to_ts(val):
	return pandas.Timestamp(ts_input=val)
# --
def dt64_to_str(val):
	return numpy.datetime_as_string(val, unit='D')

def dt64_to_dt(val):
	ts = (val - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
	return datetime.datetime(ts)

def dt64_to_ts(val):
	pass
# --
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
	converter = make_callable( m_name=__name__, f_name=f"{from_type}_to_{to_type}" )
	return converter(from_val)

@functools.lru_cache(maxsize=200)
def make_callable(f_name,m_name=None):
	if(m_name is not None):
		return getattr( sys.modules[ m_name ], f_name )
	names = f_name.split('.')
	if(len(names)==1):
		return getattr( sys.modules[ '__main__' ], f_name )
	else:
		m_name = '.'.join(names[:-1])
		f_name = names[-1]
		return getattr( sys.modules[ m_name ], f_name )
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

