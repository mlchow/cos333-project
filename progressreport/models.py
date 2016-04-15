#from views import app
import psycopg2, re
regex = re.compile('\'|\"')
#regex2 = re.compile('\( ([^\)]*,) ([^\)]*,) ([^\)]*) \)')

def search_users(netid):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return "Connection issue"
    curr = conn.cursor()
    curr.execute("SELECT netid FROM users WHERE netid = '"+netid+"';")
    netid = curr.fetchone()
    if netid != None:
        netid = netid[0]
    curr.close()
    conn.close()
    return netid

def add_user(studentinfo,netid, flag):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return None
    curr = conn.cursor()
    if len(studentinfo) != 5:
        curr.close()
        conn.close()
        return None
    nettry = search_users(netid)
    # reset progress
    if nettry != None and flag == True:
        name = studentinfo[0]
        degree = studentinfo[1]
        major = studentinfo[2]
        courses = str(studentinfo[3])
        courses = courses.replace("[","{")
        courses = courses.replace("]","}")
        num_pdfs = int(studentinfo[4]) # number of selected pdfs
        interested_majors, interested_certificates = get_major_certificate_interests(netid)
        if interested_majors == None:
            interested_majors = "{}"
        else:
            interested_majors = str(interested_majors)
            interested_majors = interested_majors.replace("[","{")
            interested_majors = interested_majors.replace("]","}")
        if interested_certificates == None:
            interested_certificates = "{}"
        else:
            interested_certificates = str(interested_certificates)
            interested_certificates = interested_certificates.replace("[","{")
            interested_certificates = interested_certificates.replace("]","}")
        fulfilled = "{}"
        fulfilledcerts = "{}"
        curr.execute("DELETE FROM users WHERE netid ='"+netid+"';")
        conn.commit()
        curr.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(netid,degree,major,interested_majors,interested_certificates,courses,num_pdfs,name,fulfilled,fulfilledcerts))
        conn.commit()
    # new user
    if nettry == None:
        name = studentinfo[0]
        degree = studentinfo[1]
        major = studentinfo[2]
        courses = str(studentinfo[3])
        courses = courses.replace("[","{")
        courses = courses.replace("]","}")
        num_pdfs = int(studentinfo[4]) # number of selected pdfs
        interested_majors = "{}"
        interested_certificates = "{}"
        fulfilled = "{}"
        fulfilledcerts = "{}"
        curr.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(netid,degree,major,interested_majors,interested_certificates,courses,num_pdfs,name,fulfilled,fulfilledcerts))
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
    curr.execute("SELECT fulfilled FROM users WHERE netid ='"+netid+"';")
    progress_so_far = curr.fetchone()
    #print progress_so_far
    if progress_so_far != None and progress_so_far[0] != None and len(progress_so_far[0]) >= 1:
        #print progress_so_far
        curr.close()
        conn.close()
        return progress_so_far[0]
    curr.execute("SELECT courses FROM users WHERE netid = '"+netid+"';")
    courses = curr.fetchone()
    if courses == None:
        curr.close()
        conn.close()
        return None
    courses = courses[0]
    progress = []
    progress_to_save = []
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
        #curr.execute("UPDATE users SET fulfilled = %s::text[] || %s::text[][] WHERE name = %s;",(,,netid))
        if len(el) >= 1:
            progress_to_save.append((course,grade,el))
        #save_progress(netid,progress)
    if len(progress_to_save) >= 1:
        ret = save_progress(netid,progress_to_save)
    else:
        ret = None
    #print progress
    curr.close()
    conn.close()
    return ret
    #else:
        #progress = []
        #for tup in re.finditer(regex2,prog):
           # print tup.group(1)
            #print tup.group(2)
           # print tup.group(3)
            #progress.append(tup.group(1,2,3))
       # print progress
       # return progress

def get_progress_certificates(netid):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return None
    curr = conn.cursor()
    curr.execute("SELECT fulfilledcerts FROM users WHERE netid ='"+netid+"';")
    progress_so_far = curr.fetchone()
    #print "in"
    #print progress_so_far
    if progress_so_far != None and progress_so_far[0] != None and len(progress_so_far[0]) >= 1:
        #print progress_so_far
        curr.close()
        conn.close()
        return progress_so_far[0]
    curr.execute("SELECT courses FROM users WHERE netid = '"+netid+"';")
    courses = curr.fetchone()
    if courses == None:
        curr.close()
        conn.close()
        return None
    courses = courses[0]
    progress = []
    progress_to_save = []
    #print courses
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
        curr.execute("SELECT certificate_area FROM courses WHERE name ~ '"+pattern+"';")
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
        #print course,grade,el
        #curr.execute("UPDATE users SET fulfilled = %s::text[] || %s::text[][] WHERE name = %s;",(,,netid))
        if len(el) >= 1:
            progress_to_save.append((course,grade,el))
        #save_progress(netid,progress)
    if len(progress_to_save) >= 1:
        ret = save_progress_certificates(netid,progress_to_save)
    else:
        ret = None
    #print progress
    curr.close()
    conn.close()
    return ret
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
    new_progress = []
    for course,grade,el in progress:
        #print grade
        for maj, track in el:
            new_progress.append([course,grade,maj,track])
    ret = new_progress
    new_progress = str(new_progress)
    new_progress = regex.sub("",new_progress)
    new_progress = new_progress.replace("[","{")
    new_progress = new_progress.replace("]","}")
    #print new_progress
    #new_progress = "{{COS126,A-,AST,recommended},{COS126,A-,COS,prerequisite}}"
    curr.execute("UPDATE users SET fulfilled = %s::text[][] WHERE netid = %s;", (new_progress,netid))
    conn.commit()
    curr.close()
    conn.close()
    return ret

def save_progress_certificates(netid,progress):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return
    curr = conn.cursor()
    new_progress = []
    for course,grade,el in progress:
        #print grade
        for maj, track in el:
            new_progress.append([course,grade,maj,track])
    ret = new_progress
    new_progress = str(new_progress)
    new_progress = regex.sub("",new_progress)
    new_progress = new_progress.replace("[","{")
    new_progress = new_progress.replace("]","}")
    #print new_progress
    #new_progress = "{{COS126,A-,AST,recommended},{COS126,A-,COS,prerequisite}}"
    curr.execute("UPDATE users SET fulfilledcerts = %s::text[][] WHERE netid = %s;", (new_progress,netid))
    conn.commit()
    curr.close()
    conn.close()
    return ret

def get_major_certificate_interests(netid):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return None
    curr = conn.cursor()
    curr.execute("SELECT interested_majors FROM users WHERE netid = '"+netid+"';")
    intmajors = curr.fetchone()
    curr.execute("SELECT interested_certificates FROM users WHERE netid = '"+netid+"';")
    intcerts = curr.fetchone()
    if intmajors == None and intcerts == None:
        return None
    if intmajors != None:
        intmajors = intmajors[0]
    if intcerts != None:
        intcerts = intcerts[0]
    return (intmajors,intcerts)

def save_major_and_certificate_interests(netid,majcert):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return
    curr = conn.cursor()
    curr.execute("SELECT name FROM majors_to_courses;")
    majindb = list(curr.fetchall())
    curr.execute("SELECT name FROM certificates_to_courses;")
    certindb = list(curr.fetchall())
    majors = []
    certificates = []
    #print majorsindb
    #print certsindb
    majorsindb = []
    certsindb = []
    for ma in majindb:
        ma = ma[0]
        ma = regex.sub("",ma)
        majorsindb.append(ma)
    for ma in certindb:
        ma = ma[0]
        ma = regex.sub("",ma)
        certsindb.append(ma)
    #print majorsindb
    #print certsindb
    for el in majcert:
        el = str(el)
        el = regex.sub("",el)
        #print el
        if el in majorsindb:
            majors.append(el)
        else:
            certificates.append(el)
    majors = str(majors)
    majors = regex.sub("",majors)
    majors = majors.replace("[","{")
    majors = majors.replace("]","}")
    certificates = str(certificates)
    certificates = regex.sub("",certificates)
    certificates = certificates.replace("[","{")
    certificates = certificates.replace("]","}")
    curr.execute("UPDATE users SET interested_majors = %s::text[] WHERE netid = %s;", (majors,netid))
    conn.commit()
    curr.execute("UPDATE users SET interested_certificates = %s::text[] WHERE netid = %s;", (certificates,netid))
    conn.commit()
    curr.close()

