from flask import render_template, flash, redirect, url_for
from config import api_key, url
from app import app
from app.forms import InputForm
import urllib.request
import json
import re
import operator

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/irisapp', methods=['GET', 'POST'])
def irisapp():
    form = InputForm()
    if form.validate_on_submit():
        data = {"Inputs": {"input1":[{'Sepal-Length': form.sepallength.data,
                                      'Sepal-Width': form.sepalwidth.data,
                                      'Petal-Length': form.petallength.data,
                                      'Petal-width': form.petalwidth.data,
                                      'Class': "Iris-setosa",
                                      'Class-Type': "1",}]},"GlobalParameters":  {}}

        body = str.encode(json.dumps(data))
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)
            result = response.read()
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(json.loads(error.read().decode("utf8", 'ignore')))

        text = result.decode("utf-8").split(',')

        probs = {"Iris-Setosa":float(text[6].split('"')[5]),
                 "Iris-Versicolor":float(text[7].split('"')[5]),\
                 "Iris-Virginica":float(text[8].split('"')[5])}

        print(probs)
        print("Predicted Iris type:",max(probs.items(), key=operator.itemgetter(1))[0])

        flash("Predicted Iris type: {}".format(max(probs.items(), key=operator.itemgetter(1))[0]), 'prediction')

        for flowertype in probs:
            flash("{} probability: {}".format(flowertype,probs[flowertype]), 'probability')

        return redirect(url_for('irisapp'))
    return render_template('iris-app.html', title='Sign In', form=form)
