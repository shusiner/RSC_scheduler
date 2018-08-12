import datetime
from calendar import monthrange



a = []
dt = datetime.date.today()
e = dt + datetime.timedelta(1)
a.append(e)
a.append(e)
print(a)

print((dt-e).days>=0)

yr = datetime.datetime.now().date().year
mth = datetime.datetime.now().date().month

dt2 = monthrange(yr, mth)[1]
print(dt2)

dt3 = datetime.date(yr,mth,1)
print(dt3)
