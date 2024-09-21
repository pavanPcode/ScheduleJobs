from Dal import db_utilitys,queries
from flask import Flask,request,jsonify
from utilitys import check_intervals,check_failed_interval
import threading

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
        print('completed')
        return {'error': "", "status": True,'data':data}
    except  Exception as e:
        return {'error':str(e),"status":False}


if __name__ == "__main__":
    app.run()
