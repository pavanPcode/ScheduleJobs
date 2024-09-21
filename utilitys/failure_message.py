def build_failure_message(event_data):
    message = f"""
    <html>
    <body>
        <p>Dear Team,</p>

        <p>This is to inform you that an event has failed during processing. Please find the details below:</p>

        <ul>
            <li><strong>Notes:</strong> {event_data['notes']}</li>
            <li><strong>Job ID:</strong> {event_data['id']}</li>
            <li><strong>Super ID:</strong> {event_data['superid']}</li>
            <li><strong>Process URL:</strong> <a href="{event_data['processurl']}">{event_data['processurl']}</a></li>
            <li><strong>Interval Type:</strong> {event_data['intervaltype']}</li>
            <li><strong>Number of Failed Attempts:</strong> {event_data['lastcalled']}</li>
            <li><strong>Device ID:</strong> {event_data['DeviceId']}</li>
            <li><strong>API Response:</strong> {event_data['ApiResponce']}</li>
        </ul>

        <p>The system has been configured to notify you after {event_data['FailedAttemptstoNotify']} failed attempt(s). Kindly investigate the issue at your earliest convenience.</p>

        <p>Best regards,<br>
        [Your System Name]</p>
    </body>
    </html>
    """

    return message


def build_failure_message1(event_data):
    message = f"""
    Dear Team,

    This is to inform you that an event has failed during processing. Please find the details below:
    
    - Job ID: {event_data['notes']}
    - Job ID: {event_data['notes']}
    - Supervisor ID: {event_data['superid']}
    - Process URL: {event_data['processurl']}
    - Interval Type: {event_data['intervaltype']}
    - Number of Failed Attempts: {event_data['lastcalled']}
    - Device ID: {event_data['DeviceId']}
    - API Response: {event_data['ApiResponce']}

    The system has been configured to notify you after {event_data['FailedAttemptstoNotify']} failed attempt(s). 
    Kindly investigate the issue at your earliest convenience.

    Best regards,
    [Your System Name]
    """

    return message

#
# # Example usage with the provided event data
# event_data = {
#     'id': 1,
#     'superid': 1,
#     'processurl': 'http://example.com/api/process',
#     'intervaltype': 'minute',
#     'lastcalled': 8,
#     'Notify': True,
#     'FailedAttemptstoNotify': 1,
#     'DeviceId': 500,
#     'ApiResponce': '404 Client Error: Not Found for url: http://example.com/api/process'
# }
#
# message = build_failure_message(event_data)
# print(message)
