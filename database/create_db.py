import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()


def create_db_from_json(json_file, filename):

    df = pd.json_normalize(json_file)

    df.to_csv(f'{filename}.csv', index=False)

    return df
