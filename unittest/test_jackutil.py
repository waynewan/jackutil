# --
# --
# --
import jackutil.configuration as cfg

basespec = { "a": { "x": 1, "y": 99 }, "pp":456 }
var = { "a/x": [ 23, 34] , ("a/y","pp"):[ (88,12), (77,33) ]}
cfg = cfg.configuration(basespec=basespec,variations=var)
vv = cfg.all_configurations()
print(vv)
print(len(vv))

# --
# --
# --
from datetime import datetime
import jackutil.microfunc as mf

nowdt = None
print(nowdt)
print( mf.date_only(nowdt) )

nowdt = datetime.utcnow()
print(nowdt)
print( mf.date_only(nowdt) )

# --
# --
# --
from jackutil import microfunc as mf
dt_str = '2021-01-03'
dt_dt = mf.dt_conv(dt_str, 'dt')
print(type(dt_dt), dt_dt)

dt_dt = mf.dt_conv(dt_str, 'dt64')
print(type(dt_dt), dt_dt)

dt_dt = mf.dt_conv(dt_str, 'ts')
print(type(dt_dt), dt_dt)

dt_dt = mf.dt_conv(dt_str, 'str')
print(type(dt_dt), dt_dt)

# --
# --
# --
from jackutil import auditedvalue
import pprint
v1 = auditedvalue.AuditedValue()
v1.setvalue(33,date=datetime.utcnow(),msg="first value")
v1.setvalue(99,date=datetime.utcnow(),msg="second value")
pprint.pprint(v1.audit)
pprint.pprint(v1)
