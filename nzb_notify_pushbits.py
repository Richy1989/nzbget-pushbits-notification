import os
import sys
import requests
import json

# Exit codes used by NZBGet
POSTPROCESS_SUCCESS=93
POSTPROCESS_ERROR=94
POSTPROCESS_NONE=95

# Define headers
headers = {
    "Content-Type": "application/json"
}

#main programm
def main():
    # Check if the script is called from nzbget 15.0 or later
    if not 'NZBOP_NZBLOG' in os.environ:
        print('*** NZBGet post-processing script ***')
        print('This script is supposed to be called from nzbget (15.0 or later).')
        return

    print('[DETAIL] Script successfully started')
    sys.stdout.flush()

    required_options = ('NZBPO_ConnectionString', 'NZBPO_OnQueue', 'NZBPO_OnDownload', 'NZBPO_AppToken')
    for	optname in required_options:
        if (not optname in os.environ):
            print('[ERROR] Option %s is missing in configuration file. Please check script settings' % optname[6:])
            return

    class NotificationData:
        def __init__(self, title, body, attach):
            self.title = title
            self.body = body
            self.attach = attach
            
        def getData(self):
            # Define the request data
            data = {
                "message": self.body,
                "title": self.title
            }
            return data

    def create_added_notification():
        filename = os.environ.get('NZBNA_FILENAME')
        category = os.environ.get('NZBNA_CATEGORY')
        
        title = 'New NZB File Queued'
        body = 'NZB File: ' + filename + ' has been added to download list.\nCategory: ' + category
        attach = None

        return NotificationData(title, body, attach)

    def create_finshed_notification(state):
        filename = os.environ.get('NZBPP_NZBNAME')
        
        title = 'NZB File Finished - ' + state
        body = 'NZB Download: ' + filename + ' finished with state: ' + state
        attach = None

        return NotificationData(title, body, attach)

    def execute_notification(notification_data):
        print('[INFO] Send Notification ' + notification_data.title)
        url = os.environ.get('NZBPO_ConnectionString')
        token = os.environ.get('NZBPO_AppToken')
        
        #Create URL with token
        url_with_token = f"{url}/message?token={token}"
        print('[INFO] Send Notification to: ' + url)
        
        data = notification_data.getData()
        response = requests.post(url_with_token, headers=headers, data=json.dumps(data))
        print('[INFO] Notification Sent!\nResponse: ' + response.text)

    # Check if the script is executed from settings page with a custom command
    command = os.environ.get('NZBCP_COMMAND')
    test_mode = command == 'ConnectionTest'

    if test_mode:
        #Do the Test
        print('[INFO] Test Mode Starting:')

        onDownload = os.environ.get('NZBPO_OnDownload')
        onQueue = os.environ.get('NZBPO_OnQueue')

        print('[INFO] OnQueue Event: ' + onQueue)
        print('[INFO] OnDownload Event: ' + onDownload)
        
        notification_data = NotificationData('Testing Notification', 'This is the test to send a notification!\nWith a new Line', None)
        execute_notification(notification_data)
        print('[INFO] Test Mode Done! Exit!')

    if command != None and not test_mode:
        print('[ERROR] Invalid command ' + command)

    event = os.environ.get('NZBNA_EVENT')
    onQueue = os.environ.get('NZBPO_OnQueue')

    #When we have a OnQueue event, and actually want it: 
    if event != None and onQueue == 'yes':
        print('[INFO] Event: ' + event)

        if event == 'NZB_ADDED':
            print('[INFO] Processing NZB_Added Event')
            notification_data = create_added_notification()
            execute_notification(notification_data)
            print('[INFO] NZB_Added Processing Completed Successfully')

    #When no event, but we are called from Post Processing
    onDownload = os.environ.get('NZBPO_OnDownload')
    state_options = ('SUCCESS', 'FAILURE')
    state = os.environ.get('NZBPP_TOTALSTATUS')

    if state != None and state in state_options and onDownload == 'yes':
        print('[INFO] NZB Finsihed ' + state)
        notification_data = create_finshed_notification(state)
        execute_notification(notification_data)

#main entry point
#we make sure this cannot fail, cause we don't want the download to fail, just because the notification has a problem
if __name__ == "__main__":
    try:
        main()
    except:
        print('[ERROR] An exception occurred')
        print('[ERROR] Will finish with success, but no notification has been sent.')

    sys.exit(POSTPROCESS_SUCCESS)