#from views import app
import psycopg2, re
regex = re.compile('\'|\"')
#regex2 = re.compile('\( ([^\)]*,) ([^\)]*,) ([^\)]*) \)')

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
    # if user's progress is stored and does not need to be updated
    #curr.execute("SELECT fulfilled FROM users WHERE netid = '"+netid+"';")
    #prog = curr.fetchone()
    #prog = prog[0]
    #if prog == None or prog == []:
        # if user's progress is not already stored or needs to be updated
    curr.execute("SELECT courses FROM users WHERE netid = '"+netid+"';")
    courses = curr.fetchone()
    if courses == None:
        curr.close()
        conn.close()
        return None
    courses = courses[0]
    progress = []
    for courseinfo in courses:
            #print courseinfo
        course = courseinfo[0]
        grade = courseinfo[1]
        #curr.execute("SELECT major_area FROM courses WHERE name = "+course+";")
        #major_areas = curr.fetchone()
        #if major_areas != None:
            #major_areas = major_areas[0]
            #progress.append((course,grade,major_areas))
        pattern = "("+course[0:4]+"$)|("+course[0:5]+"$)|("+course[0:6]+"$)|("+course+")"
        pattern = regex.sub("",pattern)
        curr.execute("SELECT major_area FROM courses WHERE name ~ '"+pattern+"';")
        #curr.execute("SELECT major_area FROM courses WHERE name = "+course+";")
        #major_areas = curr.fetchone()
        #print major_areas
        try:
            major_areas = curr.fetchall()
        except:
            continue
        el = []
        #print major_areas
        for tup in major_areas:
            if major_areas == None:
                continue
        #for major_areas in curr:
            if len(major_areas) < 1 or len(major_areas[0]) < 1 or (type(major_areas[0]) == tuple and len(major_areas[0][0]) < 1):
                continue
            #print major_areas[0]
            #print course
            #print major_areas
            #print major_areas[0]
            if type(major_areas[0]) == list:
                for it in majors_areas:
                    el.append(it)
            elif type(major_areas[0]) == str and len(major_areas) == 2:
                el.append(major_areas)
            else:
                for em in list(major_areas):
                    el2 = em
                    for el2 in list(em):
                        #print el
                        if type(el2[0]) == list:
                            for el3 in list(el2):
                                #print el3
                                el.append(el3)
                        else:
                            #print el2
                            el.append(el2)
                        #if len(el) >= 1 and type(el[0]) == list:
                        #print major_areas
        # REMOVE DUPLICATES
        el = sorted(el,key=lambda majtra: (majtra[0], majtra[1]))
        prevmaj = ""
        prevtrack = ""
        indices_to_del = []
        already_deleted = 0
        for i,val in enumerate(el):
            if prevmaj == val[0] and prevtrack == val[1]:
                indices_to_del.append(i-already_deleted)
                already_deleted = already_deleted+1
                continue
            prevmaj = val[0]
            prevtrack = val[1]
        for index in indices_to_del:
            del el[index]
        progress.append((course,grade,el))
        #save_progress(netid,progress)
    #print progress
    curr.close()
    conn.close()
    return progress
    #else:
        #progress = []
        #for tup in re.finditer(regex2,prog):
           # print tup.group(1)
            #print tup.group(2)
           # print tup.group(3)
            #progress.append(tup.group(1,2,3))
       # print progress
       # return progress


def save_progress(netid,progress):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return
    curr = conn.cursor()
    progress = str(progress)
    progress = regex.sub("",progress)
    curr.execute("UPDATE users SET fulfilled = %s WHERE netid = %s;", (progress,netid))
    conn.commit()
    curr.close()
    conn.close()

