from flask import Flask, request
import sys

import pip
from Insurance.util.util import read_yaml_file, write_yaml_file
from matplotlib.style import context
from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os, sys
from IPython.display import HTML
import json
from Insurance.config.configuration import Configuration
from Insurance.constant import CONFIG_DIR, get_current_time_stamp
from Insurance.pipeline.pipeline import Pipeline
from Insurance.entity.Insurance_predictor import InsurancePredictor, InsuranceData
from flask import send_file, abort, render_template
from wtforms import Form ,SelectField, FileField, SubmitField
from pandas import read_csv, Series
from flask import (
    Flask,
    request,
    render_template_string,
    render_template,
    url_for,
    redirect
)

ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "Insurance"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)


from Insurance.logger import get_log_dataframe

Insurance_DATA_KEY = "Insurance_data"
Insurance_VALUE_KEY = "Insurance_value"

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


@app.route('/train', methods=['GET', 'POST'])
def train():
    res_str =''
    res_str = '''
                Contact No : {},\n
                Email ID : {},\n 
            '''.format("(231) 959-4915", "insuranceinfo@gmail.com")
    return render_template('header.html',res_str)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    context = {
        Insurance_DATA_KEY: None,
        Insurance_VALUE_KEY: None
    }

    if request.method == 'POST':
        age = int(request.form['age'])
        sex = request.form['sex']
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        smoker = request.form['smoker']
        region = request.form['region']
        

        Insurance_data = InsuranceData(age = age,
                                       sex = sex,
                                       bmi = bmi,
                                       children = children,
                                       smoker = smoker,
                                       region = region)                                   
        Insurance_df = Insurance_data.get_Insurance_input_data_frame()
        Insurance_predictor = InsurancePredictor(model_dir=MODEL_DIR)
        Insurance_value = Insurance_predictor.predict(X=Insurance_df)

        context = {
            Insurance_DATA_KEY: Insurance_data.get_Insurance_data_as_dict(),
            
            Insurance_VALUE_KEY: Insurance_value,

        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


@app.route("/bulk_predict", methods=['GET', 'POST'])
def bulk_predict():
    context = {
        Insurance_DATA_KEY: None,
        Insurance_VALUE_KEY: None
    }

    if request.method == 'POST':
        f = request.files['file']
        df = read_csv(f)
        df = df.drop(columns=['expenses'],axis=1)
        Insurance_predictor = InsurancePredictor(model_dir=MODEL_DIR)
        Insurance_bulk_pred_value = Insurance_predictor.bulk_predict(X=df)

        context = {
            Insurance_DATA_KEY: HTML(df.to_html(classes='data')),
            
            Insurance_VALUE_KEY: Insurance_bulk_pred_value,
        }

        return render_template('bulk_pred.html', context=context)
    return render_template("bulk_pred.html", context=context)




if __name__ == "__main__":
    app.run(debug = True)