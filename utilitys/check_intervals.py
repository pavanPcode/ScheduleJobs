import pytz
from utilitys import apis_call,datetime_info
from Dal import db_utilitys
from datetime import datetime
from utilitys.datetime_info import get_timedelta
from datetime import time

def callApi_update_time(api_url,schedule_id,current_time):
    res = apis_call.call_api(api_url)
    print(res)
    db_utilitys.update_last_called(schedule_id, current_time, res['data'], res['status_code'], res['status'])
    return res


def is_within_time_range(start_time, end_time, current_time):
    # If end_time is None or 00:00:00, we consider it as True (always active)
    if end_time is None or end_time == time(0, 0, 0):
        return start_time <= current_time

    # Normal check if start_time <= current_time <= end_time
    return start_time <= current_time <= end_time


def find_interval(schedule):
    try:
        schedule_id = schedule['id']
        api_url = schedule['processurl']
        start_date = schedule['startdate']
        start_time = schedule['starttime']
        end_time = schedule['endtime']
        interval = schedule['interval']
        interval_type = schedule['intervaltype']
        last_called = schedule['lastcalled']
        # Define the UTC+5:30 timezone
        ist = pytz.timezone('Asia/Kolkata')
        # Localize the current datetime to UTC+5:30
        current_datetime = datetime.now(ist).replace(tzinfo=None)
        # Get the current time in IST
        current_time = datetime.now(ist).time()

        # Combine the date and time into a datetime object
        start_datetime = datetime.combine(start_date, start_time)
        # comapre start datetime and current and return in dict
        compare_dates = datetime_info.compare_dates(start_datetime, current_datetime)

        if interval_type == 'minute' or interval_type == 'hourly':
            print(start_time <= current_time <= end_time,start_time , current_time, end_time)

            if is_within_time_range(start_time, end_time, current_time):
                if last_called == None:
                    callApi_update_time(api_url, schedule_id, current_datetime)
                else:
                    end_check = last_called + get_timedelta(interval_type,interval)
                    if not (last_called <= current_datetime <= end_check):
                        callApi_update_time(api_url, schedule_id, current_datetime)

        elif interval_type == 'daily':
            if last_called == None:
                if compare_dates['hour_match']:
                    callApi_update_time(api_url, schedule_id, current_datetime)
            else:
                end_check = last_called + get_timedelta(interval_type,interval)
                if not (last_called <= current_datetime <= end_check):
                    if compare_dates['hour_match']:
                        callApi_update_time(api_url, schedule_id, current_datetime)

        elif interval_type == 'weekly':
            if last_called == None:
                if compare_dates['dayname'] and compare_dates['hour_match']:
                    callApi_update_time(api_url, schedule_id, current_datetime)
            else:
                end_check = last_called + get_timedelta(interval_type,interval)
                if not (last_called <= current_datetime <= end_check):
                    if compare_dates['dayname'] and compare_dates['hour_match']:
                        callApi_update_time(api_url, schedule_id, current_datetime)

        elif interval_type == 'monthly':
            if last_called == None:
                if compare_dates['day_match'] and compare_dates['hour_match']:
                    callApi_update_time(api_url, schedule_id, current_datetime)
            else:
                end_check = last_called + get_timedelta(interval_type,interval)
                if not (last_called <= current_datetime <= end_check):
                    if compare_dates['day_match'] and compare_dates['hour_match']:
                        callApi_update_time(api_url, schedule_id, current_datetime)

        elif interval_type == 'yearly':
            if last_called == None:
                if compare_dates['day_match'] and compare_dates['hour_match'] and compare_dates['month_match']:
                    callApi_update_time(api_url, schedule_id, current_datetime)
            else:
                end_check = last_called + get_timedelta(interval_type,interval)
                if not (last_called <= current_datetime <= end_check):
                    if compare_dates['day_match'] and compare_dates['hour_match'] and compare_dates['month_match']:
                        callApi_update_time(api_url, schedule_id, current_datetime)
    except Exception as e:
        return {'error': str(e), "status": False}