#from views import app
import psycopg2

#    database=url.path[1:],
  #  user=url.username,
  #  password=url.password,
  #  host=url.hostname,
 #   port=url.port

def search_users(netid):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return "Existing User"
    curr = conn.cursor()
    netid = curr.execute("SELECT netid FROM users WHERE netid = "+netid)
    curr.close()
    conn.close()
    if netid is None:
        return "New user"
    else:
        return "Existing user"

def add_user(studentinfo):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return False
    curr = conn.cursor()
    if len(studentinfo) != 5:
        curr.close()
        conn.close()
        return False
    netid = studentinfo[0]
    if search_users(netid) == "New user":
        degree = studentinfo[1]
        major = studentinfo[2]
        courses = str(studentinfo[3])
        courses = courses.replace("[","{")
        courses = courses.replace("]","}")
        num_pdfs = int(studentinfo[4]) # number of selected pdfs
        interested_majors = "{}"
        interested_certificates = "{}"
        curr.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%d)",(netid,degree,major,interested_majors,interested_certificates,courses,num_pdfs))
        conn.commit()
    curr.close()
    conn.close()
    return False

