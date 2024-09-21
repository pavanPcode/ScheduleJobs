from datetime import datetime, timedelta

def get_datetime_info(dt):
    # Create a dictionary with the relevant date and time components
    return {
        "year": dt.year,
        "month": dt.month,
        "day": dt.day,
        "hours": dt.hour,
        "minutes": dt.minute,
        "seconds": dt.second,
        "dayname": dt.strftime("%A")  # Get the name of the day like Monday, Wednesday
    }

# # Example datetime
# dt = datetime(2024, 9, 19, 11, 46, 23, 610000)
#
# # Get the dictionary of datetime information
# datetime_info = get_datetime_info(dt)
# print(datetime_info)



def compare_dates(date1, date2):
    # Compare days and hours
    month_match = date1.month == date2.month  # Checks if the month is the same
    day_match = date1.day == date2.day  # Checks if the day is the same
    hour_match = date1.hour == date2.hour  # Checks if the hour is the same
    dayname= date1.strftime("%A") ==  date2.strftime("%A") # Get the name of the day like Monday, Wednesday
    # Return the results
    return {'day_match':day_match, 'hour_match':hour_match,"dayname":dayname,"month_match":month_match}


# # Example usage
# date1 = datetime(2024, 9, 19, 11, 46, 23, 610000)
# date2 = datetime(2024, 9, 19, 11, 30, 0, 0)
#
# print( compare_dates(date1, date2))



def get_date_info(dt):
    # Create a dictionary with the relevant date and time components
    return {
        "year": dt.year,
        "month": dt.month,
        "day": dt.day,
        "dayname": dt.strftime("%A")  # Get the name of the day like Monday, Wednesday
    }

def get_time_info(dt):
    # Create a dictionary with the relevant date and time components
    return {
        "hours": dt.hour,
        "minutes": dt.minute,
        "seconds": dt.second,
    }


def get_timedelta(interval, value):
    if interval == 'daily':
        return timedelta(days=value)
    elif interval == 'weekly':
        return timedelta(weeks=value)
    elif interval == 'monthly':
        return timedelta(days=value * 30)  # Approximation
    elif interval == 'yearly':
        return timedelta(days=value * 365)  # Approximation
    elif interval == 'hourly':
        return timedelta(hours=value)
    elif interval == 'minute':
        return timedelta(minutes=value)