import os,psycopg2,urlparse
from flask import Flask, request, redirect, url_for
from flask import render_template
import CASClient
from controller import parse_transcript, show_progress, old_show_progress, get_major_by_courses, get_major_by_gpa
from models import search_users, add_user, get_progress, get_progress_certificates, save_major_and_certificate_interests, get_major_certificate_interests, get_course_value
import CASClient
from werkzeug.contrib.cache import SimpleCache
import json

app = Flask(__name__)

cache = SimpleCache()

#form = cgi.FieldStorage()

#from progressreport import app

C = CASClient.CASClient()
os.environ["HTTP_HOST"] = 'progressreport.herokuapp.com'
os.environ['REQUEST_URI'] = '/welcome.html'

#netid = "" # bad security but useful for now

@app.route("/")
def start():
    loginpage = C.Authenticate1()
    return redirect(loginpage)
    # return render_template('index_bs.html')

#@app.route("/",methods=["GET"])
#def restart():
 #   if request.method == 'GET':
  #      ticket_from_cas = request.GET['ticket']
   #     # RETURNS "yes NETID"
    #    netid = C.Authenticate2(ticket_from_cas)
    #return render_template('templates/index.html',netid)

@app.route("/viewcourse",methods=["POST"])
def view_course():
    if request.method == 'POST':
        course = request.get_json()['coursename']
        netid = cache.get('netid')
        interested_majors,interested_certificates,others = get_course_value(netid,course)
        #print interested_majors,interested_certificates,others
        return json.dumps({'status':'OK','interested_majors':interested_majors,'interested_certificates':interested_certificates,'others':others})

@app.route("/updatetranscript",methods=["POST"])
def update_transcript():
    if request.method == 'POST':
        file = request.files['transcript']
        netid = cache.get('netid')
        #netid = "iingato"
        #cache.set('netid',netid)
        #netid = "iingato"
        #netid = request.form['netid']
        if file and netid:
            studentinfo = parse_transcript(file)
            add_user(studentinfo,netid,True)
        return json.dumps({'status':'OK'})

@app.route("/updateinterests",methods=["POST"])
def update_interests():
    if request.method == 'POST':
        majors = request.get_json()
        listofmajors = majors['majors']
        netid = cache.get('netid')
        if netid == None:
            #print "HELP"
            return json.dumps({'status':'OK'})
        save_major_and_certificate_interests(netid,listofmajors)
        #print listofmajors
        return json.dumps({'status':'OK'})
        #print majors
        #return render_template('index_bs.html')

@app.route("/welcome.html",methods=["POST","GET","HEAD"])
def upload_file():
    if request.method == 'GET' or request.method == 'HEAD':
        #ticket_from_cas = request.args.get('ticket')
        #nid = C.Authenticate2(ticket_from_cas)
        #if nid == "" or None:
            #nid = cache.get('netid')
        #if nid == "":
            #return "<html><body>Invalid netid</body></html>"
        nid = "iingato"
        cache.set('netid',nid)
        netid = search_users(nid)
        if netid:
            ret = get_progress(netid)
            ret_certs = get_progress_certificates(netid)

            majors_completed = get_major_by_courses(ret)
            majors_gpa = get_major_by_gpa(ret)
            certificates_completed = get_major_by_courses(ret_certs)
            d = {
                'netid': netid,
                'majors_completed': majors_completed,
                'majors_gpa': majors_gpa,
                'certificates_completed': certificates_completed
            }
            return render_template('success_bs.html',d=d)
    if request.method == 'POST':
        file = request.files['transcript']
        netid = cache.get('netid')
        #netid = "iingato"
        #cache.set('netid',netid)
        if netid is None:
            loginpage = C.Authenticate1()
            return redirect(loginpage)
        #netid = "iingato"
        #netid = request.form['netid']
        if file:
            studentinfo = parse_transcript(file)
            if add_user(studentinfo,netid,False) != None:
                #return render_template('success.html',netid=netid)
                ret = get_progress(netid)
                ret_certs = get_progress_certificates(netid)

                majors_completed = get_major_by_courses(ret)
                majors_gpa = get_major_by_gpa(ret)
                certificates_completed = get_major_by_courses(ret_certs)

                d = {
                    'netid': netid,
                    'majors_completed': majors_completed,
                    'majors_gpa': majors_gpa,
                    'certificates_completed': certificates_completed
                }
                return render_template('success_bs.html',d=d)

                # return "<html><body>"+old_show_progress(ret)+"</body></html>"
                #return str(ret)
                #return "<html><body>" + str(get_progress(netid)) + '</body></html>'
                #return redirect(url_for("success"))
    return render_template('index_bs.html')
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
    #port = int(os.environ['PORT'])
    #app.run(host='0.0.0.0', port=port)
    app.run(host='127.0.0.1', port=5000, debug=True)
