from params import *
import requests
import pandas as pd
from pandas import json_normalize
import psycopg2
from sqlalchemy import create_engine
import hashlib

api = api_url
token = token

def generate_userId(row):
    return str(uuid.uuid4())

def ga_data_api(token, api):
    
    response = requests.post(api, headers={"Authorization": f"Bearer {token}"}, json=body)
    data = response.json()
    # print(data)
    return data

def read_json_data(data):
    results = []
    rows = data.get('rows', [])
    for row in rows:
        raw_dimentions = row.get('dimensionValues', [])
        raw_metrics = row.get('metricValues', [])

        columns = {
        "date": raw_dimentions[0]['value'],
        "ActiveUsers": raw_metrics[0]['value'],
        "Sessions": raw_metrics[1]['value'],
        "KeyEvents": raw_metrics[4]['value'],
        "EventCount": raw_metrics[3]['value']
        }
        
        unique_string = f"{columns['date']}_{columns['ActiveUsers']}_{columns['Sessions']}_{columns['KeyEvents']}_{columns['EventCount']}"

        columns["user_id"] = hashlib.sha256(
                unique_string.encode()
            ).hexdigest()

        results.append(columns)
    # print(f"Date: {columns['date']}, Active Users: {columns['ActiveUsers']}, Sessions: {columns['Sessions']}, Key Events: {columns['KeyEvents']}, Event Count: {columns['EventCount']}")
    print(results)
    return results

def column_mapping(results):
    mapping = []

    for row in results:
        mapping.append({
            "date": row['date'],
            "activeuser": row['ActiveUsers'],
            "sessions": row['Sessions'],
            "keyevent": row['KeyEvents'],
            "eventcount": row['EventCount'],
             "user_id": row['user_id']
        })

    return mapping
    # print(mapping)

def connect_to_db():
    try:
        # Connect to db
        engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/testdb")
        print("Connection to database successful!")
        return engine
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        return None

def load_to_db(mapping):
    df = pd.DataFrame(mapping)

    engine = connect_to_db()

    existing_data = pd.read_sql(
        "SELECT user_id FROM ga_data",
        engine
    )

    if not existing_data.empty:
        df = df[
            ~df['user_id'].isin(existing_data['user_id'])
        ]

    if df.empty:
        print("No new rows to insert after deduplication.")
        engine.dispose()
        return

    df.to_sql(
        'ga_data',
        engine,
        if_exists='append',
        index=False
    )

    print(f"{len(df)} new rows inserted.")
    engine.dispose()

def main():
    api_data = ga_data_api(token, api)
    results = read_json_data(api_data)
    # print(flattened_data)
    mapping = column_mapping(results)
    query = load_to_db(mapping)

if __name__ == "__main__":
    main()