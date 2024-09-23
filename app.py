from Dal import db_utilitys,queries
from flask import Flask,request,jsonify
from utilitys import check_intervals,check_failed_interval
import threading
from datetime import datetime, time
app = Flask(__name__)


@app.route('/')
def index1():
    return "services are up",200

def get_dbdata(device_id):
    try:
        query = queries.getactivejobs.format(device_id)
        result = db_utilitys.get_data_from_db(query)
        for schedule in result['data']:
            #check_intervals.find_interval(schedule)
            # Start a new thread for each interval check
            threading.Thread(target=check_intervals.find_interval, args=(schedule,)).start()
    except Exception as e:
        return {'error': str(e), "status": False}

@app.route('/getScheduleJobs')
def getScheduleJobs():
    super_id = request.args.get('superid')
    if super_id == None or super_id == '':
        super_id = "superid"
    quary = queries.getScheduleJobsqr.format(super_id)
    data = db_utilitys.get_data_from_db(quary)
    return jsonify(data),200


@app.route('/check_failed_interval')
def check_for_notifi():
    check_failed_interval.send_failurenotify_mail()
    return jsonify({"status":True}),200



@app.route('/run_active_interval')
def index():
    try:
        device_id = request.args.get('deviceid')
        # Check if device_id is provided and is a valid integer
        if device_id is None or not device_id.isdigit():
            return jsonify({'status':False,"error": "device_id is required and must be a non-empty integer."}), 400
        data = get_dbdata(device_id)
        return {'error': "", "status": True,'data':data}
    except  Exception as e:
        return {'error':str(e),"status":False}



@app.route('/addJob', methods=['POST'])
def add_job():
    # Get the data from the POST request
    data = request.get_json()
    try:
        # Required fields
        superid = data.get('SuperId')
        interval = data.get('Interval')
        failedattempts = data.get('FailedAttemptstoNotify')
        deviceid = data.get('DeviceId')
        notify = data.get('Notify')

        # Convert notify to integer and validate
        if notify in [0, 1]:
            notify = int(notify)  # Ensure it's either 0 or 1
        else:
            return {'error': 'notify must be 0 or 1', 'status': False}

        if superid is None or not isinstance(superid, int):
            return {'error': 'superid not int or missing', 'status': False}
        if interval is None or not isinstance(interval, int):
            return {'error': 'interval not int or missing', 'status': False}
        if failedattempts is None or not isinstance(failedattempts, int):
            return {'error': 'failedattempts not int or missing', 'status': False}
        if deviceid is None or not isinstance(deviceid, int):
            return {'error': 'deviceid not int or missing', 'status': False}

        processurl = str(data.get('ProcessUrl'))
        startdate = datetime.strptime(data.get('StartDate'), '%Y-%m-%d').date()
        starttime = datetime.strptime(data.get('StartTime'), '%H:%M:%S').time()
        endtime = datetime.strptime(data.get('EndTime'), '%H:%M:%S').time()
        intervaltype = data.get('IntervalType')
        timeoutsec = int(data.get('TimeOutSec'))
        notes = data.get('Notes', '')
        createdby = int(data.get('CreatedBy')) if data.get('CreatedBy') else None


        qr = queries.insert_ScheduleJobs_query.format(superid, processurl, startdate, starttime, endtime, intervaltype,
            interval,  timeoutsec, notes,createdby, deviceid, notify, failedattempts)
        result = db_utilitys.update_record_db(qr)
        return result

    except ValueError as ve:
        return {'error': f'ValueError: {str(ve)}', 'status': False}
    except KeyError as ke:
        return {'error': f'Missing field: {str(ke)}', 'status': False}
    except Exception as e:
        return {'error': str(e), 'status': False}


if __name__ == "__main__":
    app.run(debug=True)
