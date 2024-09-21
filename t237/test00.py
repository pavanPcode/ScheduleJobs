from utilitys import apis_call,datetime_info
from Dal import db_utilitys
from datetime import datetime, timedelta
from flask import Flask

app = Flask(__name__)

def callApi_update_time(api_url,schedule_id,current_time):
    res = apis_call.call_api(api_url)
    # res_in_text = f"{str(res[f'status'])} - {res['data']}"
    db_utilitys.update_last_called(schedule_id, current_time, res['data'], res['status_code'], res[f'status'])
    return res

def find_interval(schedule):
    schedule_id = schedule['id']
    api_url = schedule['processurl']
    start_datetime = schedule['startdatetime']
    end_datetime = schedule['enddatetime']
    interval = schedule['interval']
    interval_value = schedule['intervalvalue']
    last_called = schedule['lastcalled']

    current_time = datetime.now()
    #print(api_url,start_datetime,type(start_datetime),end_datetime,interval,interval_value,current_time)

    #comapre start datetime and current and return in dict
    compare_dates = datetime_info.compare_dates(start_datetime, current_time)

    if interval == 'minute':
        print('minute')
        if last_called == None:
            callApi_update_time(api_url, schedule_id, current_time)
        else:
            end_check = last_called + timedelta(minutes=interval_value)
            # Check if current_time is within the start_time and end_time range
            if not (last_called <= current_time <= end_check):
                callApi_update_time(api_url, schedule_id, current_time)

    elif interval == 'hourly':
        if last_called == None:
            callApi_update_time(api_url, schedule_id, current_time)
        else:
            end_check = last_called + timedelta(hours=interval_value)
            #print(last_called,end_check,"kjda")
            # Check if current_time is within the start_time and end_time range
            if not (last_called <= current_time <= end_check):
                callApi_update_time(api_url, schedule_id, current_time)

    elif interval == 'daily':
        if last_called == None:
            if compare_dates['hour_match']:
                callApi_update_time(api_url,schedule_id,current_time)
        else:
            end_check = last_called + timedelta(days=interval_value)
            if not (last_called <= current_time <= end_check):
                if compare_dates['hour_match']:
                    callApi_update_time(api_url, schedule_id, current_time)

    elif interval == 'weekly':
        if last_called == None:
            if compare_dates['dayname'] and compare_dates['hour_match']:
                callApi_update_time(api_url, schedule_id, current_time)
        else:
            end_check = last_called + timedelta(weeks=interval_value)
            if not (last_called <= current_time <= end_check):
                if compare_dates['dayname'] and compare_dates['hour_match']:
                    callApi_update_time(api_url, schedule_id, current_time)


    elif interval == 'monthly':
        if last_called == None:
            if compare_dates['day_match'] and compare_dates['hour_match']:
                callApi_update_time(api_url, schedule_id, current_time)
        else:
            end_check = last_called + timedelta(days=interval_value * 28)
            if not (last_called <= current_time <= end_check):
                if compare_dates['day_match'] and compare_dates['hour_match']:
                    callApi_update_time(api_url, schedule_id, current_time)

    elif interval == 'yearly':
        if last_called == None:
            if compare_dates['day_match'] and compare_dates['hour_match'] and compare_dates['month_match']:
                callApi_update_time(api_url, schedule_id, current_time)
        else:
            end_check = last_called + timedelta(days=interval_value * 365)
            if not (last_called <= current_time <= end_check):
                if compare_dates['day_match'] and compare_dates['hour_match'] and compare_dates['month_match']:
                    callApi_update_time(api_url, schedule_id, current_time)




def get_dbdata():
    try:
#     query = """SELECT id,superid,processurl,startdatetime,interval,intervalvalue,lastcalled,enddatetime FROM [dbo].[Jobs1] WHERE StartDateTime <= GETDATE()
# AND (EndDateTime >= GETDATE() OR EndDateTime IS NULL) and IsActive = 1 ;"""
        query = """SELECT jb.id,jb.superid,jb.processurl,jb.startdatetime,jb.interval,jb.intervalvalue,jb.enddatetime,MAX(al.lastcalled) AS lastcalled
FROM [dbo].[Jobs1] jb
left JOIN [dbo].[APILogs] al ON al.JobsId = jb.Id
WHERE jb.StartDateTime <= GETDATE() 
AND (jb.EndDateTime >= GETDATE() OR jb.EndDateTime IS NULL) and jb.IsActive = 1 
GROUP BY jb.id,jb.superid,jb.processurl,jb.startdatetime,jb.interval,jb.intervalvalue,jb.enddatetime
ORDER BY LastCalled DESC;"""

        result = db_utilitys.get_data_from_db(query)
        for schedule in result['data']:
            find_interval(schedule)
    except Exception as e:
        print(f"Error updating last_called: {e}")


@app.route('/')
def index():
    try:
        get_dbdata()
        return {'error': "", "status": True}
    except  Exception as e:
        return {'error':str(e),"status":False}

#if __name__ == "__main__":
app.run(debug=True)

