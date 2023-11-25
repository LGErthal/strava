import api.auth as auth
import database.create_db as db
import os
from dotenv import load_dotenv
import json

## First request the authorization for the user
user_code = auth.request_code()

## After authorization, we need to request all the token access
user_access_token = auth.request_access_token(user_code)

## We then need to get all the user's activities
user_activities = auth.get_activities(user_access_token)

