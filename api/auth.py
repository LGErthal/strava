import json
import requests
import os
from dotenv import load_dotenv
import database.create_db as db

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = 'http://localhost/'

request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                  f'&response_type=code&redirect_uri={redirect_uri}' \
                  f'&approval_prompt=force' \
                  f'&scope=profile:read_all,activity:read_all'

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"



def request_code():
      print('Copy this URL in your web-browser:', request_url)
      print('Authorize the app and copy and paste below the generated code! The code is in the URL!!!!!')
      code = input('Insert the code from the url: ')

      return code


def request_access_token(user_code):
    token = requests.post(url=auth_url,
        data={'client_id': client_id,
              'client_secret': client_secret,
              'code': user_code,
              'grant_type': 'authorization_code'})
      
    strava_token = token.json()
    access_token = token.json()['access_token']

    print("Access Token = {}\n".format(access_token))

    with open('data/strava_token.json', 'w') as outfile:
        json.dump(strava_token, outfile)

    if strava_token:
        db.create_db_from_json(strava_token, 'user_tokens')
        
    return access_token


def get_activities(access_token):
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}
    activities = requests.get(activites_url, headers=header, params=param).json()
    
    with open('data/user_activities.json', 'w') as outfile:
        json.dump(activities, outfile)

    if activities:
        dataset = db.create_db_from_json(activities, 'user_activities')

    return dataset


#def refresh_token():
#    refresh_url = 'https://www.strava.com/api/v3/oauth/token'
#    token_json_path = os.getenv('TOKEN_JSON_PATH')
#
#    # Check if the JSON file exists
#    if os.path.exists(token_json_path):
#        # Read refresh token from the JSON file
#        with open(token_json_path, 'r') as file:
#            data = json.load(file)
#            refresh_token = data.get("refresh_token")
#
#        if refresh_token:
#            # Use the refresh token to get a new access token
#            token = requests.post(url=refresh_url,
#                                  data={'client_id': client_id,
#                                        'client_secret': client_secret,
#                                        'grant_type': 'refresh_token',
#                                        'refresh_token': refresh_token})
#
#            if token.status_code == 200:
#                # Update the JSON file with the new access token
#                strava_token = token.json()
#                with open(token_json_path, 'w') as outfile:
#                    json.dump(strava_token, outfile)
#
#                # Get activities with the new access token
#                access_token = strava_token['access_token']
#                user_activities = get_activities(access_token)
#                return user_activities
#            else:
#                print("Failed to refresh token. Reauthorizing...")
#        else:
#            print("No refresh token found in the JSON file. Reauthorizing...")
#    else:
#        print("Token JSON file not found. Reauthorizing...")
#
#    # If reaching here, either the refresh failed or no refresh token was found
#    # Reauthorize, request a new token, and get activities
#    user_code = request_code()
#    access_token = request_token(user_code)
#    user_activities = get_activities(access_token)
#
#    return user_activities


#def refresh_token():
#      refresh_url = 'https://www.strava.com/api/v3/oauth/token'
#      
#      # Parse the JSON data
#      with open('/home/erthal/Desktop/Workspace/strava/data/strava_token.json', 'r') as file:
#            data = json.load(file)
#
#      # Access the value of the refresh_token field
#      refresh_token = data["refresh_token"]
#
#      # Print the result
#      print("Refresh Token:", refresh_token)
#
#      token = requests.post(url=refresh_url,
#                            data={'client_id': client_id,
#                            'client_secret': client_secret,
#                            'grant_type': 'refresh_token',
#                            'refresh_token': refresh_token})
#
#      strava_token = token.json()
#
#      with open('data/strava_token.json', 'w') as outfile:
#            json.dump(strava_token, outfile)
#