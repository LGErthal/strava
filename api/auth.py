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
