import datetime as dt
import time as tm

tm.time() #time today in seconds counting from the epoch
# -------------------------------------------------------------
dtnow = dt.datetime.fromtimestamp(tm.time) 
#date and time in year, month, day, hour, minute, second, millisecond
# -------------------------------------------------------------
dtnow.year, dtnow.month, dtnow.day, dtnow.hour, dtnow.minute, dtnow.second 
# returns each component of the datetime object
# -------------------------------------------------------------
delta = dt.timedelta(days=100)
#returns the desired time difference
today = dt.date.today()
#returns present day
today - delta 
# returns date of 100 days ago
