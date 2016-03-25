import os,psycopg2,urlparse
from flask import Flask, request, redirect
from flask import render_template
import CASClient
from controller import parse_transcript

app = Flask(__name__)

C = CASClient.CASClient()
os.environ["HTTP_HOST"] = 'progressreport.herokuapp.com'
os.environ['REQUEST_URI'] = '/'

@app.route("/")
def start():
    netid = C.Authenticate()
    if len(netid) > 10:
        return redirect(netid)
    #return '<html><body>' + netid + '</body></html>'
    return render_template('index.html',netid)

@app.route("/",methods=["POST"])
def upload_file():
    if request.method == 'POST':
        file = request.files['transcript']
        if file:
            return parse_transcript(file)
        return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ['PORT'])
    app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=5000)
