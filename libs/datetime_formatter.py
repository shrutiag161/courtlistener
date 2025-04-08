from datetime import datetime
import logging 

# Converts a datetime string into a date
# If no timezone is given then local time will be used by default
# dt_str_format example: "%Y-%m-%dT%H:%M:%S.%f%z"
def str_to_dt(dt_str, dt_str_format, timezone = None):
    dt = datetime.strptime(dt_str, dt_str_format) # string to datetime
    return dt.astimezone(timezone) # convert datetime to new timezone

# Convert a datetime to a formatted string in a specific format
# new_format example: "%A %b %d at %I %p %Z" (Friday Mar 21 at 04 PM EDT)
def format_dt(dt:datetime, new_format):
    return dt.strftime(new_format) 
