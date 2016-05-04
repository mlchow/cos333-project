import os,psycopg2,urlparse,re
from flask import Flask, request, redirect, url_for, session
from flask import render_template
import CASClient
from controller import parse_transcript, show_progress, old_show_progress, get_major_by_courses, get_major_by_gpa, parse_manual_courses
from models import search_users, add_user, get_progress, get_progress_certificates, save_major_and_certificate_interests, get_major_certificate_interests, get_course_value, suggestcourses, get_student_info, update_just_transcript, get_major_cert_requirements, delete_progress, add_major_specific_manual_progress
import CASClient
import json

app = Flask(__name__)

C = CASClient.CASClient()
os.environ["HTTP_HOST"] = 'progressreport.herokuapp.com'
os.environ['REQUEST_URI'] = '/welcome.html'

app.secret_key = "3#bC$Zx#XoKb@#xB7Dozl}sj7"

def validateInput(inp):
    if re.match("^[A-Z0-9\s,\+-]*$",inp,re.IGNORECASE) == None:
        return False
    else:
        return True

@app.route("/")
def start():
    loginpage = C.Authenticate1()
    return redirect(loginpage)
    # return render_template('index_bs.html')

@app.route("/deletemanualprogress",methods=["POST"])
def delete_man():
    netid = session['netid']
    course = request.get_json()['course']
    major = request.get_json()['major']
    track = request.get_json()['track']
    morc = request.get_json()['type']
    delete_progress(netid,course,major,track,morc)
    return json.dumps({'status':'OK'})

@app.route("/addmajormanualprogress",methods=["POST"])
def add_maj_man():
    netid = session['netid']
    coursegrade = request.get_json()['coursegrade']
    major = request.get_json()['major']
    track = request.get_json()['track']
    morc = request.get_json()['morc']
    courses = add_major_specific_manual_progress(netid,coursegrade,major,track,morc)
    return json.dumps({'status':'OK','courses':courses})

@app.route("/logout",methods=["GET","POST"])
def end():
    session.pop('netid', None)
    logoutpage = C.Authenticate1out()
    return redirect(logoutpage)
    # return json.dumps({'status':'OK'})

#@app.route("/deleteaccount",methods=["GET","POST"])
#def deleteacc():
#    netid = session['netid']
#    delete_account(netid)
#    session.pop('netid', None)
#    logoutpage = C.Authenticate1out()
#    return redirect(logoutpage)

@app.route("/suggestcourses", methods=["POST","GET"])
def suggest_courses():
    netid = session['netid']
    return json.dumps({'status':'OK','suggested_courses': suggestcourses(netid)})

@app.route("/addmanualprogress", methods=["POST","GET"])
def add_manual_progress():
    if request.method == 'POST':
        courses = request.get_json()['courses']
        netid = session['netid']
        update_just_transcript(netid, courses)
        return json.dumps({'status':'OK'})

@app.route("/viewcourse",methods=["POST"])
def view_course():
    if request.method == 'POST':
        course = request.get_json()['coursename']
        netid = session['netid']
        interested_majors,interested_certificates,others = get_course_value(netid,course)
        return json.dumps({'status':'OK','interested_majors':interested_majors,'interested_certificates':interested_certificates,'others':others})

@app.route("/updatetranscript",methods=["POST"])
def update_transcript():
    if request.method == 'POST':
        file = request.files['transcript']
        netid = session['netid'] if 'netid' in session else None
        if file and netid:
            studentinfo = parse_transcript(file)
            if studentinfo != None:
                add_user(studentinfo,session['netid'],True)
        if studentinfo == None:
            return json.dumps({'status':'OK','correctfile':'No'})
        else:
            return json.dumps({'status':'OK','correctfile':'Yes'})

@app.route("/updateinterests",methods=["POST"])
def update_interests():
    if request.method == 'POST':
        majors = request.get_json()
        listofmajors = majors['majors']
        netid = None
        try:
            netid = session['netid']
            save_major_and_certificate_interests(netid,listofmajors)
            return json.dumps({'status':'OK'})
        except KeyError:
            return json.dumps({'status':'OK'})        

# Main page
@app.route("/welcome.html",methods=["POST","GET","HEAD"])
def upload_file():
    mistake = False
    if request.method == 'GET' or request.method == 'HEAD':
        ticket_from_cas = request.args.get('ticket')
        nid = C.Authenticate2(ticket_from_cas)
        if nid == "" or None:
           nid = session['netid'] if 'netid' in session else None
        if nid == "" or None:
           loginpage = C.Authenticate1()
           return redirect(loginpage)
        session['netid'] = nid
        netid = search_users(nid)
        if netid:
            info = get_student_info(netid)

            ret = get_progress(netid)
            ret_certs = get_progress_certificates(netid)

            majors_completed,doublecountcom = get_major_by_courses(ret)
            majors_gpa,doublecountgpa = get_major_by_gpa(ret)
            certificates_completed,doublecountcerts = get_major_by_courses(ret_certs)

            major_interests,certificate_interests = get_major_certificate_interests(netid)

            # get info of courses for interested majors/certificates
            majors_of_interest = []
            certificates_of_interest = []
            major_names = []
            certificate_names = []
            for maj in majors_completed:
                major_names.append(maj[0])
                if maj[0] in major_interests:
                    majors_of_interest.append(maj)
            for cert in certificates_completed:
                certificate_names.append(cert[0])
                if cert[0] in certificate_interests:
                    certificates_of_interest.append(cert)

            requirements_dictionary = get_major_cert_requirements(major_names,certificate_names)

            simple_dc = []
            for dc in doublecountcom:
                simple_dc.append(dc[0])
            for dc in doublecountgpa:
                simple_dc.append(dc[0])
            for dc in doublecountcerts:
                simple_dc.append(dc[0])

            d = {
                'netid': netid,
                'majors_completed': majors_completed,
                'majors_gpa': majors_gpa,
                'certificates_completed': certificates_completed,
                'interested_majors': majors_of_interest,
                'interested_certificates': certificates_of_interest,
                'int_majors': major_interests,
                'int_certificates': certificate_interests,
                'doublecount': simple_dc,
                'info': info,
                'reqs_dict':requirements_dictionary
            }
            return render_template('success_bs.html',d=d)
    if request.method == 'POST':
        file = request.files['transcript']
        studentname = request.form['Name']
        degree = request.form['Degree']
        major = request.form['Major']
        manualcourses = request.form['manual_courses']
        netid = session['netid'] if 'netid' in session else None
        if netid is None:
            loginpage = C.Authenticate1()
            return redirect(loginpage)
        if file:
            studentinfo = parse_transcript(file)
            if studentinfo == None:
                mistake = True 
        else:
            if not validateInput(studentname) or not validateInput(major) or not validateInput(manualcourses):
                mistake = True
                #print validateInput(studentname), validateInput(major), validateInput(manualcourses)
        if not mistake and (file or manualcourses):
            if not file and manualcourses:
                if studentname == "":
                    studentname == "Anonymous Tiger"
                course_manual_parsed = parse_manual_courses(manualcourses)
                # since we do not know how many pdfs, set to -1
                studentinfo = [studentname,degree,major,course_manual_parsed,-1]
            if add_user(studentinfo,netid,False) != None:

                info = [studentinfo[0],studentinfo[1],studentinfo[2],studentinfo[4]]

                ret = get_progress(netid)
                ret_certs = get_progress_certificates(netid)

                majors_completed,doublecountcom = get_major_by_courses(ret)
                majors_gpa,doublecountgpa = get_major_by_gpa(ret)
                certificates_completed,doublecountcerts = get_major_by_courses(ret_certs)

                major_interests,certificate_interests = get_major_certificate_interests(netid)
                
                majors_of_interest = []
                certificates_of_interest = []
                major_names = []
                certificate_names = []
                for maj in majors_completed:
                    major_names.append(maj[0])
                    if maj[0] in major_interests:
                        majors_of_interest.append(maj)
                for cert in certificates_completed:
                    certificate_names.append(cert[0])
                    if cert[0] in certificate_interests:
                        certificates_of_interest.append(cert)

                requirements_dictionary = get_major_cert_requirements(major_names,certificate_names)

                simple_dc = []
                for dc in doublecountcom:
                    simple_dc.append(dc[0])
                for dc in doublecountgpa:
                    simple_dc.append(dc[0])
                for dc in doublecountcerts:
                    simple_dc.append(dc[0])

                d = {
                    'netid': netid,
                    'majors_completed': majors_completed,
                    'majors_gpa': majors_gpa,
                    'certificates_completed': certificates_completed,
                    'interested_majors': majors_of_interest,
                    'interested_certificates': certificates_of_interest,
                    'int_majors': major_interests,
                    'int_certificates': certificate_interests,
                    'doublecount': simple_dc,
                    'info': info,
                    'reqs_dict':requirements_dictionary
                }
                return render_template('success_bs.html',d=d)
    d = { 
        'mistake':mistake
    }
    return render_template('index_bs.html',d=d)

if __name__ == "__main__":
    port = int(os.environ['PORT'])
    app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=5000, debug=True)
