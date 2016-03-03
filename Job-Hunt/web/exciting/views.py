 # -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template,jsonify,request
import re
import xlrd

from exciting import app


@app.route('/hello/')
@app.route('/hello/<name>')
def hello_world(name = None):
    return render_template('hello.html', name=name)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search',methods=['GET'])
def search(result = None):
	return render_template('result.html')

@app.route('/job', methods=['GET'])
def job():
	return render_template('job.html')

