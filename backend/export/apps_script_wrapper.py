# mostly copied from Google's example

import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from apiclient import errors

import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

mod_dir = os.path.dirname(os.path.realpath(__file__))

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/script-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = os.path.join(mod_dir, 'client_secret.json')
APPLICATION_NAME = 'Order Dump Job'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_dir = os.path.join(mod_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'script-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def call(script_id, func, params):
    """Shows basic usage of the Apps Script Execution API.

    Creates a Apps Script Execution API service object and uses it to call an
    Apps Script function to print out a list of folders in the user's root
    directory.
    """
    # Authorize and create a service object.
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('script', 'v1', http=http)

    # Create an execution request object.
    request = {"function": func, "parameters": params}

    try:
        # Make the API request.
        # pylint: disable=no-member
        response = service.scripts().run(body=request,
                scriptId=script_id).execute()

        if 'error' in response:
            # The API executed, but the script returned an error.

            # Extract the first (and only) set of error details. The values of
            # this object are the script's 'errorMessage' and 'errorType', and
            # an list of stack trace elements.
            error = response['error']['details'][0]
            print("Script error message: {0}".format(error['errorMessage']))

            if 'scriptStackTraceElements' in error:
                # There may not be a stacktrace if the script didn't start
                # executing.
                print("Script error stacktrace:")
                for trace in error['scriptStackTraceElements']:
                    print("\t{0}: {1}".format(trace['function'],
                        trace['lineNumber']))
        else:
            return response

    except errors.HttpError as e:
        # The API encountered a problem before the script started executing.
        print(e.content)

