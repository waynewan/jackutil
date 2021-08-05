import pandas as pd

class AuditedValue:
	def __init__(self,defval=None):
		self.__defval = defval
		self.__value = None
		self.__date = None
		self.__msg = None
		self.__audit = []

	def hasvalue(self):
		return 0<len(self.__audit)

	def getaudit(self):
		return self.__audit
	audit = property(getaudit,None,None,"audit trail")

	def getvalue(self,meta=False):
		if(meta):
			if(self.hasvalue()):
				return (self.__value,self.__date,self.__msg)
			else:
				return (self.__defval,None,None)
		else:
			if(self.hasvalue()):
				return self.__value
			else:
				return self.__defval
	def setvalue(self,value,date=None,msg=None):
		if(hasattr(value,'__iter__')):
			value,date,msg = value
		self.__value = value
		self.__date = date
		self.__msg = msg
		self.__audit.append( (value,date,msg) )
	def delvalue(self):
		self.__audit.pop()
		if(len(self.__audit)==0):
			self.__value=None
		else:
			self.__value=self.__audit[-1][0]
	value = property(getvalue,setvalue,delvalue,"audited variable")

	def to_dataframe(self,prefix=None,marker=None,ts_as_index=True,limit=-1):
		if(prefix is None):
			prefix = ""
		elif(prefix[-1] !='_'):
			prefix = prefix + '_'
		sl = slice(None,None,None)
		if(limit>0):
			sl = slice(0,limit,1)
		df = pd.DataFrame(self.getaudit()[sl], columns=[prefix+'value',prefix+'ts',prefix+'note'])
		if(marker is not None):
			df[prefix+'type'] = marker
			if(ts_as_index):
				df = df.set_index([prefix+'ts',prefix+'type'])
			return df
		if(ts_as_index):
			df = df.set_index(prefix+'ts')
		return df

	def __str__(self):
		if(self.hasvalue()):
			return str(self.audit[-1])
		return str(self.__defval)

	def __repr__(self):
		return self.__str__()
