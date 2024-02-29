
#/usr/bin/env python
# -*- coding: utf8 -*-

import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import calendar

start_date = datetime.date.today()
end_date = start_date + timedelta(days=111)
start_month = calendar.month_abbr[int(start_date.strftime("%m"))]

print (str(start_date) + " to " + str(end_date))

months = relativedelta(end_date, start_date).months
days = relativedelta(end_date, start_date).days

print (months, "months", days, "days")

if days > 16:
    months += 1

print ("around " + str(months) + " months", "(",)

for i in range(0, months):
    print (calendar.month_abbr[int(start_date.strftime("%m"))],
    start_date = start_date + relativedelta(months=1))

print (")")