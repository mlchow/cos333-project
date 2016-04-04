from progressreport import app

import os,psycopg2,urlparse
from flask import Flask, request, redirect
from flask import render_template
import CASClient
from controller import parse_transcript

C = CASClient.CASClient()
#os.environ["HTTP_HOST"] = 'progressreport.herokuapp.com'
os.environ["HTTP_HOST"] = 'localhost:5000'
os.environ['REQUEST_URI'] = '/'

@app.route("/")
def start():
    netid = C.Authenticate()
    if len(netid) > 10:
        return redirect(netid)
    # #return '<html><body>' + netid + '</body></html>'
    return render_template('index_bs.html',netid)

@app.route("/",methods=["POST"])
def upload_file():
    if request.method == 'POST':
        file = request.files['transcript']
        if file:
            return parse_transcript(file)
        return render_template('index_bs.html')
