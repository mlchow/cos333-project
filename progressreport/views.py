import os,psycopg2,urlparse
from flask import Flask, request, redirect, url_for
from flask import render_template
import CASClient
from controller import parse_transcript
from models import search_users, add_user, get_progress

app = Flask(__name__)

#from progressreport import app

#C = CASClient.CASClient()
#os.environ["HTTP_HOST"] = 'progressreport.herokuapp.com'
#os.environ['REQUEST_URI'] = '/'
#netid = "" # bad security but useful for now

@app.route("/")
def start():
    #loginpage = C.Authenticate1()
    #if len(netid) > 15:
    #return redirect(loginpage)
    #return '<html><body>' + netid + '</body></html>'
    return render_template('index.html')

#@app.route("/",methods=["GET"])
#def restart():
 #   if request.method == 'GET':
  #      ticket_from_cas = request.GET['ticket']
   #     # RETURNS "yes NETID"
    #    netid = C.Authenticate2(ticket_from_cas)
    #return render_template('templates/index.html',netid)

@app.route("/",methods=["POST"])
def upload_file():
    if request.method == 'POST':
        file = request.files['transcript']
        netid = request.form['netid']
        if file:
            studentinfo = parse_transcript(file)
            if add_user(studentinfo,netid) != None:
                #return render_template('success.html',netid=netid)
                return "<html><body>" + str(get_progress(netid)) + '</body></html>'
                #return redirect(url_for("success"))
        return render_template('index.html')
        #str(get_progress(netid)) + '</body></html>'

#@app.route("/see_progress",)
#def see_progress(netid):
    #if request.method == 'GET':
        #return "<html><body>" + str(get_progress(netid)) + '</body></html>'

#@app.route("/success",methods=["GET"])
#def success(netid):
    #if request.method == 'GET':
     #   return redirect(url_for(("see_progress"netid)))
    #return render_template('success.html',netid=netid)

if __name__ == "__main__":
    port = int(os.environ['PORT'])
    app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=5000, debug=True)
