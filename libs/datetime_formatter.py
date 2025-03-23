from datetime import datetime
import logging 

# Converts a datetime string into another format
# example:
#     datetime_str: "2025-03-21T13:13:20.006980-07:00"
#     old_format: "%Y-%m-%dT%H:%M:%S.%f%z"
#     new_tz: pytz.timezone('US/Eastern')
#     new_format: "%A %b %d at %I %p %Z" (ex: Friday Mar 21 at 04 PM EDT)
def format_datetime(datetime_str, old_format, new_tz, new_format):
    datetime_dt = datetime.strptime(datetime_str, old_format) # string to datetime
    datetime_eastern = datetime_dt.astimezone(new_tz)
    datetime_formatted = datetime_eastern.strftime(new_format) # format datetime
    return datetime_formatted
