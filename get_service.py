import pandas as pd
import os

import sqlite3 as sql
import flask
from flask import request, jsonify
import configparser


import json
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.float_format', '{:.4f}'.format)


config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

data = pd.read_csv(os.getcwd()+"/dataset/Churn_Results.csv")

conn = sql.connect(os.getcwd()+"/dataset/churn_df.db")
data.to_sql("churn_df", conn, if_exists='replace')

#conn2 = sql.connect(os.getcwd()+"/dataset/Unique_Churn_Results.db")
data = pd.read_sql("SELECT * FROM churn_df", conn).drop(columns="index")
unique_data = pd.read_csv(os.getcwd()+"/dataset/Unique_Churn_Results.csv")

data.fillna("NA", inplace=True)
unique_data.fillna("NA", inplace=True)

def column_format(data):
    data['Random_Forest_Probability'] = data['Random_Forest_Probability'].apply(lambda x: '{:.5f}'.format(x))
    data['Calibrated_Random_Forest_Probability'] = data['Calibrated_Random_Forest_Probability'].apply(lambda x: '{:.5f}'.format(x))
    data['Naive_Bias_Probability'] = data['Naive_Bias_Probability'].apply(lambda x: '{:.5f}'.format(x))
    data['Isotonic_Calibrated_Naive_Bias_Probability'] = data['Isotonic_Calibrated_Naive_Bias_Probability'].apply(lambda x: '{:.5f}'.format(x))
    data['Sigmoid_Calibrated_Naive_Bias_Probability'] = data['Sigmoid_Calibrated_Naive_Bias_Probability'].apply(lambda x: '{:.5f}'.format(x))
    data['Churn_Score'] = data['Churn_Score'].apply(lambda x: '{:.5f}'.format(x))

    return data

data = column_format(data)
unique_data = column_format(unique_data)

df = data.to_json(orient="records")
df = json.loads(df)

df_unique = unique_data.to_json(orient="records")
df_unique = json.loads(df_unique)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/all_result', methods=['GET'])
def total_api():
    return jsonify(df[:100])

@app.route('/all_unique_result', methods=['GET'])
def total_unique_api():
    return jsonify(df_unique[:100])

@app.route('/result', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'userId' in request.args:
        userId = request.args['userId']
    else:
        return "Error: No userId field provided. Please specify an id."

    # Create an empty list for our results
    results = []
    # Loop through the data and match results that fit the requested ID.

    for id_ in range(len(df)):
        if (df[id_]["userId"] == userId):
            results.append(df[id_])

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    if len(results)<1:
        return "userId is not found", 404
    else:
        return jsonify(results)

@app.route('/unique_result', methods=['GET'])
def unique_api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'userId' in request.args:
        userId = request.args['userId']
    else:
        return "Error: No userId field provided. Please specify an id."

    # Create an empty list for our results
    results = []
    # Loop through the data and match results that fit the requested ID.

    for id_ in range(len(df_unique)):
        if (df_unique[id_]["userId"] == userId):
            results.append(df_unique[id_])

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    if len(results)<1:
        return "userId is not found", 404
    else:
        return jsonify(results)

app.run(host=config["Service"]["Host"], port=int(config["Service"]["Port"]), debug=True)


