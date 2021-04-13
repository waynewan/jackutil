class AuditedValue:
	def __init__(self,defval=None):
		self.__defval = defval
		self.__value = None
		self.__audit = []

	def hasvalue(self):
		return 0<len(self.__audit)

	def getaudit(self):
		return self.__audit
	audit = property(getaudit,None,None,"audit trail")

	def getvalue(self):
		if(self.hasvalue()):
			return self.__value
		else:
			return self.__defval
	def setvalue(self,value,date=None,msg=None):
		if(hasattr(value,'__iter__')):
			value,date,msg = value
		self.__value = value
		self.__audit.append( (value,date,msg) )
	def delvalue(self):
		self.__audit.pop()
		if(len(self.__audit)==0):
			self.__value=None
		else:
			self.__value=self.__audit[-1][0]
	value = property(getvalue,setvalue,delvalue,"audited variable")

	def __str__(self):
		return str(self.getvalue())

	def __repr__(self):
		return str(self.getvalue())
