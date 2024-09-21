from Dal import db_utilitys,queries
from utilitys import failure_message,apis_call



def send_failurenotify_mail():
    url = 'https://notifyservisesrc.azurewebsites.net/notify/sendmail'
    query = queries.getfailedNotifyData
    result = db_utilitys.get_data_from_db(query)
    if result['status']:
        for i in result['data']:

            event_data = failure_message.build_failure_message(i)

            data = {
                "superid": 41112,
                "toaddr": "pavan@perennialcode.in",
                "message": event_data,
                "subject": f"API triggers Failure  more than {str(i['lastcalled'])} time."
            }
            apis_call.post_api(url, data)
            break
