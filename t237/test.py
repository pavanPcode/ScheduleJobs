from datetime import datetime, timedelta
from Dal import db_utilitys
from utilitys.apis_call import call_api

def should_call_api(schedule):
    now = datetime.now()
    interval = schedule.get('interval')
    interval_value = schedule.get('interval_value')
    start_datetime = schedule.get('start_datetime')
    print(start_datetime,'start_datetime')
    if start_datetime:
        # Ensure start_datetime is a datetime object
        if isinstance(start_datetime, str):
            start_datetime = datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S')

        # Check if the current time is past the start time
        if now >= start_datetime:
            print('now', now, 'start_datetime', start_datetime,now >= start_datetime)
            elapsed_time = now - start_datetime
            print('get_timedelta',get_timedelta(interval, interval_value))
            next_call = start_datetime + get_timedelta(interval, interval_value)
            print(next_call,'next_call')
            while next_call <= now:
                next_call += get_timedelta(interval, interval_value)
            return now >= next_call
    return False


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


def main():
    query = """SELECT * FROM api_schedules order by id desc"""
    result = db_utilitys.get_data_from_db(query)

    if result['status']:
        schedules = result['data']
        for schedule in schedules:
            result_data =  should_call_api(schedule)
            print(result_data)
            if result_data:
                call_api(schedule['api_url'])
            break
    else:
        print(f"Error fetching schedules: {result['error']}")


if __name__ == "__main__":
    main()
