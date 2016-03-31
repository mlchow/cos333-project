#from views import app
import psycopg2

def search_users(netid):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return "Existing User"
    curr = conn.cursor()
    curr.execute("SELECT netid FROM users WHERE netid = '"+netid+"';")
    netid = curr.fetchone()
    curr.close()
    conn.close()
    return netid

def add_user(studentinfo,netid):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return None
    curr = conn.cursor()
    if len(studentinfo) != 5:
        curr.close()
        conn.close()
        return None
    if search_users(netid) == None:
        name = studentinfo[0]
        degree = studentinfo[1]
        major = studentinfo[2]
        courses = str(studentinfo[3])
        courses = courses.replace("[","{")
        courses = courses.replace("]","}")
        num_pdfs = int(studentinfo[4]) # number of selected pdfs
        interested_majors = "{}"
        interested_certificates = "{}"
        curr.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s,%s);",(netid,degree,major,interested_majors,interested_certificates,courses,num_pdfs,name))
        conn.commit()
    curr.close()
    conn.close()
    return netid

def get_progress(netid):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return None
    curr = conn.cursor()
    curr.execute("SELECT courses FROM users WHERE netid = '"+netid+"';")
    courses = curr.fetchone()
    if courses == None:
        curr.close()
        conn.close()
        return None
    courses = courses[0]
    progress = []
    # for now we don't report on grade ?
    for courseinfo in courses:
        #print courseinfo
        course = courseinfo[0]
        grade = courseinfo[1]
        curr.execute("SELECT major_area FROM courses WHERE name = "+course+";")
        major_areas = curr.fetchone()
        if major_areas != None:
            major_areas = major_areas[0]
            progress.append((course,grade,major_areas))
    curr.close()
    conn.close()
    return progress

