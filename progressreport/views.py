import os,psycopg2,urlparse
from flask import Flask, request, redirect
from flask import render_template
import CASClient
from controller import parse_transcript

from progressreport import app

C = CASClient.CASClient()
os.environ["HTTP_HOST"] = 'progressreport.herokuapp.com'
os.environ['REQUEST_URI'] = '/'

@app.route("/")
def start():
    loginpage = C.Authenticate1()
    #if len(netid) > 15:
    return redirect(loginpage)
    #return '<html><body>' + netid + '</body></html>'
    #return render_template('index.html',netid)

@app.route("/",methods=["GET"])
def restart():
    if request.method == 'GET':
        ticket_from_cas = request.GET['ticket']
        netid = C.Authenticate2(ticket_from_cas)
    return render_template('templates/index.html',netid)

@app.route("/",methods=["POST"])
def upload_file():
    if request.method == 'POST':
        file = request.files['transcript']
        if file:
            return parse_transcript(file)
        return render_template('templates/index.html')

if __name__ == "__main__":
    port = int(os.environ['PORT'])
    app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=5000)
