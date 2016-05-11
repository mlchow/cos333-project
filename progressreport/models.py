import psycopg2, re
grade_regex = re.compile("(A|B|C|D|F|P)(\+|-)?")
regex = re.compile('\'|\"')
#regex2 = re.compile('\( ([^\)]*,) ([^\)]*,) ([^\)]*) \)')

# Receives a list of majors (maj) and list of certificates (certs) as input
# Returns a dictionary with major/certificate names as keys and, as values, dictionaries consisting of the 
# number of pdfs allowed in that major or certificate, the total number of courses required, and the number of courses needed in each track
def get_major_cert_requirements(maj,certs):
    maj_to_needs = {}

    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return None
    curr = conn.cursor()
    for m in maj:
        mini = {}

        curr.execute("SELECT track_reqs FROM majors WHERE name ='"+m+"';")
        reqs = curr.fetchone()
        if reqs == None:
            continue
        reqs = reqs[0]

        curr.execute("SELECT num_pdfs_allowed FROM majors WHERE name ='"+m+"';")
        pdfs = curr.fetchone()[0]

        curr.execute("SELECT total_num_courses_needed FROM majors WHERE name ='"+m+"';")
        total = curr.fetchone()[0]

        mini['pdfs'] = int(pdfs)
        mini['total'] = int(total)

        req = {}

        for r in reqs:
            try:
                req[r[0]] = int(r[1])
            except:
                continue

        mini['reqs'] = req

        maj_to_needs[m] = mini

    for m in certs:
        mini = {}

        curr.execute("SELECT track_reqs FROM certificates WHERE name ='"+m+"';")
        reqs = curr.fetchone()
        if reqs == None:
            continue
        reqs = reqs[0]

        curr.execute("SELECT num_pdfs_allowed FROM certificates WHERE name ='"+m+"';")
        pdfs = curr.fetchone()[0]

        curr.execute("SELECT total_num_courses_needed FROM certificates WHERE name ='"+m+"';")
        total = curr.fetchone()[0]

        mini['pdfs'] = int(pdfs)
        mini['total'] = int(total)

        req = {}

        for r in reqs:
            req[r[0]] = int(r[1])

        mini['reqs'] = req

        maj_to_needs[m] = mini

    curr.close()
    conn.close()

    return maj_to_needs

#def delete_account(netid):
#    try:
#        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
#    except:
#        return None
#    curr = conn.cursor()
#    curr.execute("DELETE FROM users WHERE netid = '"+netid+"';")
#    conn.commit()
#    curr.close()
#    conn.close()

# Receives a student's netid
# Returns a list with the student's name, degree type, major, and number of pdfs completed
def get_student_info(netid):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return None
    curr = conn.cursor()

    curr.execute("SELECT name FROM users WHERE netid = '"+netid+"';")
    name = curr.fetchone()
    if name != None:
        name = name[0]

    curr.execute("SELECT degree FROM users WHERE netid = '"+netid+"';")
    deg = curr.fetchone()
    if deg != None:
        deg = deg[0]

    curr.execute("SELECT major FROM users WHERE netid = '"+netid+"';")
    maj = curr.fetchone()
    if maj != None:
        maj = maj[0]

    curr.execute("SELECT num_pdfs FROM users WHERE netid = '"+netid+"';")
    pdfs = curr.fetchone()
    if pdfs != None:
        pdfs = pdfs[0]
    else:
        pdfs = 0

    curr.close()
    conn.close()

    return [name,deg,maj,pdfs]

# Receives a student's netid
# Returns a list of tuples of recommended courses where each tuple is in the form (name_of_course,list_of_all_tracks_it_fulfills,list_of_all_majors_it_fulfills,weight_of_recommendation)
def suggestcourses(netid):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return None
    curr = conn.cursor()

    # GET INTERESTED MAJORS AND CERTIFICATES

    curr.execute("SELECT interested_majors FROM users WHERE netid = '"+netid+"';")
    intmajors = curr.fetchone()
    if intmajors != None:
        intmajors = intmajors[0]
    curr.execute("SELECT interested_certificates FROM users WHERE netid = '"+netid+"';")
    intcerts = curr.fetchone()
    if intcerts != None:
        intcerts = intcerts[0]

    # GET COURSES THAT FULFILL THINGS IN MAJORS/CERTIFICATES

    potential_maj_courses = []
    if intmajors != None:
        for maj in intmajors:
            curr.execute("SELECT coursetrack FROM majors_to_courses WHERE name = '"+maj+"';")
            nec = curr.fetchone()
            if nec != None:
                if type(nec[0][0]) == list:
                    for el in nec[0]:
                        potential_maj_courses.append((maj,el))
                else:
                    potential_maj_courses.append((maj,nec[0]))
                
    potential_cert_courses = []
    if intcerts != None:
        for maj in intcerts:
            curr.execute("SELECT coursetrack FROM certificates_to_courses WHERE name = '"+maj+"';")
            nec = curr.fetchone()
            if nec != None:
                if type(nec[0][0]) == list:
                    for el in nec[0]:
                        potential_cert_courses.append((maj,el))
                else:
                    potential_cert_courses.append((maj,nec[0]))

    # GET FULFILLED COURSES IN MAJORS / CERTIFICATES
    curr.execute("SELECT fulfilled FROM users WHERE netid = '"+netid+"';")
    maj = curr.fetchone()
    if maj == None:
        fulfilledmajors = []
    else:
        fulfilledmajors = maj[0]
    curr.execute("SELECT fulfilledcerts FROM users WHERE netid = '"+netid+"';")
    maj = curr.fetchone()
    if maj == None:
        fulfilledcerts = []
    else:
        fulfilledcerts = maj[0]
    # combine
    allfulfilledcourses = fulfilledmajors+fulfilledcerts
    fulfilledcourses = []
    trackinfo = []
    for f in allfulfilledcourses:
        fulfilledcourses.append(f[0]) # just the course name
        trackinfo.append((f[2],f[3]))

    # SORT / REMOVE COURSES THAT HAVE ALREADY BEEN TAKEN OR ARE NOT 6 characters / THEN WEIGHT BY HOW MANY TIMES APPEARS / IF PREREQUISITE

    potential_courses = sorted((potential_maj_courses+potential_cert_courses),key=lambda majtra: (majtra[1][0],majtra[0],majtra[1][1]))
    new_potential_courses = []
    lst_course = ""
    lst_track = ""
    lst_maj = ""
    count = 1
    alltracks = []
    allmaj = []

    # GET MAJOR/CERTIFICATES REQUIREMENTS (IF EXIST IN DB) / DELETE IF FULFILLED / ADD ADDITIONAL WEIGHTING, then sort by that

    total_maj_reqs_needed = {}
    if intmajors != None:
        for maj in intmajors:
            curr.execute("SELECT track_reqs FROM majors WHERE name = '"+maj+"';")
            nec = curr.fetchone()
            mini = []
            if nec != None:
                if type(nec[0]) == list:
                    for t in nec[0]:
                        mini.append(t)
                else:
                    mini.append(nec[0])
                total_maj_reqs_needed[maj] = mini

    total_cert_reqs_needed = {}
    if intcerts != None:
        for maj in intcerts:
            curr.execute("SELECT track_reqs FROM certificates WHERE name = '"+maj+"';")
            nec = curr.fetchone()
            mini = []
            if nec != None:
                if type(nec[0]) == list:
                    for t in nec[0]:
                        mini.append(t)
                else:
                    mini.append(nec[0])
                total_cert_reqs_needed[maj] = mini

    # eliminate already completed progress
    for maj,track in trackinfo:
        tracks = []
        mes = 0
        if maj in total_maj_reqs_needed:
            tracks = total_maj_reqs_needed[maj]
            mes = 1
        if maj in total_cert_reqs_needed:
            tracks = total_cert_reqs_needed[maj]
            mes = 2
        i = -1
        for j,x in enumerate(tracks):
            if track == x[0]:
                i = j
        if i >= 0:
            spec = tracks[i]
            del tracks[i]
            if int(spec[1]) > 0:
                tracks.append((spec[0],int(spec[1])-1,spec[2]))
            else:
                tracks.append((spec[0],int(spec[1]),spec[2]))
            if mes == 1:
                total_maj_reqs_needed[maj] = tracks
            if mes == 2:
                total_cert_reqs_needed[maj] = tracks

    for maj,coursetrack in potential_courses:
        tracks = []
        if maj in total_maj_reqs_needed:
            tracks = total_maj_reqs_needed[maj]
        if maj in total_cert_reqs_needed:
            tracks = total_cert_reqs_needed[maj]
        #print tracks
        course = coursetrack[0]
        if len(course) != 6:
            #pos = course
            #pos_cnt = len(coursetrack[1])
            #maj_ps = maj
            continue
        track = coursetrack[1]
        if course not in fulfilledcourses:
            #print maj,course,track
            #if course[0:3] == pos and maj == maj_ps:
                #print course[0:3], pos
                #count = count + pos_cnt/2
            for trak in tracks:
                #print trak[0],course[3]
                #print course[3]
                #print trak[0]
                if trak[0] == track or (len(trak) >= 1 and trak[0].isdigit() and course[3].isdigit() and int(trak[0]) <= int(course[3])):
                    #print maj,coursetrack,"plus"
                    count = count + int(trak[1])
                    if maj not in allmaj:
                        allmaj.append(maj)
                    if track not in alltracks:
                        alltracks.append(track)
            if course == lst_course and maj == lst_maj and track == lst_track:
                #count = count + 1
                continue
            elif course == lst_course:
                allmaj.append(maj)
                alltracks.append(track)
                count = count + 1
                if maj != lst_maj:
                    count = count + 1
                # weight prerequisites higher
                if track == "prerequisite":
                    count = count + 0.5
            else:
                new_potential_courses.append((lst_course,alltracks,allmaj,count))
                lst_course = course
                lst_track = track
                lst_maj = maj
                count = 1
                alltracks = []
                allmaj = []

    new_potential_courses = sorted(new_potential_courses,key=lambda cs: cs[3],reverse=True)

    curr.close()
    conn.close()
    if len(new_potential_courses) >= 5:
        return new_potential_courses[0:5]
    else:
        return new_potential_courses

# Receives a net id and course name
# Returns a tuple of the majors and certificates the course helps fulfill in the form (majors on user's board, certificates on user's board, other majors/certificates)
def get_course_value(netid,course):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return (None,None,None)
    curr = conn.cursor()
    curr.execute("SELECT interested_majors FROM users WHERE netid = '"+netid+"';")
    intmajors = curr.fetchone()
    if intmajors != None:
        intmajors = intmajors[0]
    curr.execute("SELECT interested_certificates FROM users WHERE netid = '"+netid+"';")
    intcerts = curr.fetchone()
    if intcerts != None:
        intcerts = intcerts[0]
    pattern = "("+course[0:4]+"$)|("+course[0:5]+"$)|("+course[0:6]+"$)|("+course+")"
    pattern = regex.sub("",pattern)
    el = []
    curr.execute("SELECT major_area FROM courses WHERE name ~ '"+pattern+"';")
    try:
        major_areas = curr.fetchall()
    except:
        return (None,None,None)
    for tup in major_areas:
        if major_areas == None:
            continue
        #for major_areas in curr:
        if len(major_areas) < 1 or len(major_areas[0]) < 1 or (type(major_areas[0]) == tuple and len(major_areas[0][0]) < 1):
            continue
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
                    if len(el2) > 0 and type(el2[0]) == list:
                        for el3 in list(el2):
                            el.append(el3)
                    else:
                        el.append(el2)
    curr.execute("SELECT certificate_area FROM courses WHERE name ~ '"+pattern+"';")
    try:
        major_areas = curr.fetchall()
    except:
        return (None,None,None)
    for tup in major_areas:
        if major_areas == None:
            continue
        if len(major_areas) < 1 or len(major_areas[0]) < 1 or (type(major_areas[0]) == tuple and len(major_areas[0][0]) < 1):
            continue
        if type(major_areas[0]) == list:
            for it in majors_areas:
                el.append(it)
        elif type(major_areas[0]) == str and len(major_areas) == 2:
            el.append(major_areas)
        else:
            for em in list(major_areas):
                el2 = em
                for el2 in list(em):
                    if type(el2[0]) == list:
                        for el3 in list(el2):
                            el.append(el3)
                    else:
                        el.append(el2)
        # REMOVE DUPLICATES
    n_el = []
    for e in el:
        if len(e) >= 2:
            n_el.append(e)
    el = sorted(n_el,key=lambda majtra: (majtra[0], majtra[1]))
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
    curr.close()
    conn.close()
    inmaj = []
    incer = []
    els = []
    for e,t in el:
        if intmajors != None and e not in intmajors and intcerts != None and e not in intcerts and e not in els:
            els.append(e)
            continue
        if intmajors != None and e in intmajors and e not in inmaj:
            inmaj.append(e)
        if intcerts != None and e in intcerts and e not in incer:
            incer.append(e)
    return (inmaj,incer,els)
    
# Receives a netid
# Returns None if the user is new and the netid if it is a returning user
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

# Receives a student's info, netid, and a flag indicating whether the user is on the login or sign up page
# Adds a new user to the database or updates an old user's information
# Returns the user's netid
def add_user(studentinfo,netid,flag):
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
        #print nettry, studentinfo[1],studentinfo[2]
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
            interested_majors = regex.sub("",interested_majors)
        if interested_certificates == None:
            interested_certificates = "{}"
        else:
            interested_certificates = str(interested_certificates)
            interested_certificates = interested_certificates.replace("[","{")
            interested_certificates = interested_certificates.replace("]","}")
            interested_certificates = regex.sub("",interested_certificates)
        fulfilled = "{}"
        fulfilledcerts = "{}"
        curr.execute("DELETE FROM users WHERE netid ='"+netid+"';")
        conn.commit()
        curr.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(netid,degree,major,interested_majors,interested_certificates,courses,num_pdfs,name,fulfilled,fulfilledcerts))
        conn.commit()
    # new user
    if nettry == None:
        #if flag == False:
        #    curr.execute("DELETE FROM users WHERE netid ='"+netid+"';")
        #    conn.commit()
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

# Receives a user's netid
# If the user's progress has not been calculated or needs to be recalculated, recalculates the progress
# Otherwise, obtains the progress list from the database
# Returns a user's major progress in a list of tuples of the form (course_name,grade,major_fulfilled,track_fulfilled)
def get_progress(netid):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return None
    curr = conn.cursor()
    curr.execute("SELECT fulfilled FROM users WHERE netid ='"+netid+"';")
    progress_so_far = curr.fetchone()
    if progress_so_far != None and progress_so_far[0] != None and len(progress_so_far[0]) >= 1:
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
        try:
            major_areas = curr.fetchall()
        except:
            continue
        el = []
        for tup in major_areas:
            if major_areas == None:
                continue
        #for major_areas in curr:
            if len(major_areas) < 1 or len(major_areas[0]) < 1 or (type(major_areas[0]) == tuple and len(major_areas[0][0]) < 1):
                continue
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
                        if len(el2) > 0 and type(el2[0]) == list:
                            for el3 in list(el2):
                                #print el3
                                el.append(el3)
                        elif len(el2) == 0 and type(el2) == list:
                            continue
                        else:
                            el.append(el2)
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

# Receives a user's netid
# If the user's progress has not been calculated or needs to be recalculated, recalculates the progress
# Otherwise, obtains the progress list from the database
# Returns a user's certificate progress in a list of tuples of the form (course_name,grade,certificate_fulfilled,track_fulfilled)
def get_progress_certificates(netid):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return None
    curr = conn.cursor()
    curr.execute("SELECT fulfilledcerts FROM users WHERE netid ='"+netid+"';")
    progress_so_far = curr.fetchone()

    if progress_so_far != None and progress_so_far[0] != None and len(progress_so_far[0]) >= 1:
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
        try:
            major_areas = curr.fetchall()
        except:
            continue
        el = []
        for tup in major_areas:
            if major_areas == None:
                continue
        #for major_areas in curr:
            if len(major_areas) < 1 or len(major_areas[0]) < 1 or (type(major_areas[0]) == tuple and len(major_areas[0][0]) < 1):
                continue
            if type(major_areas[0]) == list:
                for it in majors_areas:
                    el.append(it)
            elif type(major_areas[0]) == str and len(major_areas) == 2:
                el.append(major_areas)
            else:
                for em in list(major_areas):
                    el2 = em
                    for el2 in list(em):
                        if len(el2) > 0 and type(el2[0]) == list:
                            for el3 in list(el2):
                                el.append(el3)
                        elif len(el2) == 0 and type(el2) == list:
                            continue
                        else:
                            el.append(el2)
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
        ret = save_progress_certificates(netid,progress_to_save)
    else:
        ret = None
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

# Receives a user's netid and their calculated progress list
# Saves their progress to the database
# Returns their progress list in the form of a list of tuples (course_name,grade,major_fulfilled,track_fulfilled)
def save_progress(netid,progress):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return
    curr = conn.cursor()
    new_progress = []
    for course,grade,el in progress:
        for maj, track in el:
            new_progress.append([course,grade,maj,track])
    ret = new_progress
    new_progress = str(new_progress)
    new_progress = regex.sub("",new_progress)
    new_progress = new_progress.replace("[","{")
    new_progress = new_progress.replace("]","}")
    #new_progress = "{{COS126,A-,AST,recommended},{COS126,A-,COS,prerequisite}}"
    curr.execute("UPDATE users SET fulfilled = %s::text[][] WHERE netid = %s;", (new_progress,netid))
    conn.commit()
    curr.close()
    conn.close()
    return ret

# Receives a user's netid and their calculated progress list
# Saves their progress to the database
# Returns their progress list in the form of a list of tuples (course_name,grade,certificate_fulfilled,track_fulfilled)
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
    #new_progress = "{{COS126,A-,AST,recommended},{COS126,A-,COS,prerequisite}}"
    curr.execute("UPDATE users SET fulfilledcerts = %s::text[][] WHERE netid = %s;", (new_progress,netid))
    conn.commit()
    curr.close()
    conn.close()
    return ret

# Receives a student's netid, morc (whether we are considering major or certificate progress), and the course, major, and track to be deleted from progress
# Deletes only part of a user's "progress", does not change the list of a user's courses in the database
def delete_progress(netid,course,major,track,morc):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return None
    curr = conn.cursor()
    if morc == "m":
        curr.execute("SELECT fulfilled FROM users WHERE netid = '"+netid+"';")
        ful = curr.fetchone()
    else:
        curr.execute("SELECT fulfilledcerts FROM users WHERE netid = '"+netid+"';")
        ful = curr.fetchone()
    if ful == None:
        return
    ful = ful[0]
    #print ful
    new_ful = []
    for el in ful:
        #print el[0],el[2],el[3]
        if el[0] == course and el[2] == major and el[3] == track:
            continue
        new_ful.append(el)
    new_progress = str(new_ful)
    new_progress = regex.sub("",new_progress)
    new_progress = new_progress.replace("[","{")
    new_progress = new_progress.replace("]","}")
    #print new_progress
    if morc == "m":
        curr.execute("UPDATE users SET fulfilled = %s::text[][] WHERE netid = %s;", (new_progress,netid))
    else:
        curr.execute("UPDATE users SET fulfilledcerts = %s::text[][] WHERE netid = %s;", (new_progress,netid))
    conn.commit()
    curr.close()
    conn.close()

# Receives a student's netid, morc (whether we are considering major or certificate progress), and the course, major, and track to be added to progress
# Updates a user's progress, but does not change their list of courses
def add_major_specific_manual_progress(netid,coursegrade,major,track,morc):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return
    curr = conn.cursor()
    major = str(major)
    track = str(track)
    netid = str(netid)
    morc = str(morc)
    courses = str(coursegrade)
    if courses == "":
        return
    courses = courses.split(",")
    courses_and_grades = []
    for course in courses:
        course_grad = course.split(" ")
        if course_grad[0] == "" or len(course_grad) > 2:
            continue
        #print course_grad
        if len(course_grad) == 1:
            courses_and_grades.append([course_grad[0].upper(),"None",major,track])
        else:
            if len(course_grad[1]) == 3:
                courses_and_grades.append([course_grad[0].upper()+course_grad[1].upper(),"None",major,track])
            #if grade_regex.find_all(course_grad[1]) != None:
            else:
                courses_and_grades.append([course_grad[0].upper(),course_grad[1].upper(),major,track])
    org_courses = courses_and_grades
    courses_and_grades = str(courses_and_grades)
    courses_and_grades = regex.sub("",courses_and_grades)
    courses_and_grades = courses_and_grades.replace("[","{")
    courses_and_grades = courses_and_grades.replace("]","}")
    if morc == "major":
        curr.execute("SELECT fulfilled FROM users WHERE netid = '"+netid+"';")
        ful = curr.fetchone()
    else:
        curr.execute("SELECT fulfilledcerts FROM users WHERE netid = '"+netid+"';")
        ful = curr.fetchone()
    if ful == None:
        return
    ful = ful[0]
    ful = str(ful)
    ful = regex.sub("",ful)
    ful = ful.replace("[","{")
    ful = ful.replace("]","}")
    if morc == "major":
        curr.execute("UPDATE users SET fulfilled = %s::text[][] || %s::text[][] WHERE netid = %s;", (courses_and_grades,ful,netid))
    else:
        curr.execute("UPDATE users SET fulfilledcerts = %s::text[][] || %s::text[][] WHERE netid = %s;", (courses_and_grades,ful,netid))
    conn.commit()
    curr.close()
    conn.close()
    return org_courses

# Receives a user's netid and list of courses and grades to add
# Adds each course and grade (or None if it is absent) to the user's list of courses and deletes user's fulfilled/fullfilledcerts values, which will be recalcuated on reload
def update_just_transcript(netid, courses):
    try:
        conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
    except:
        return None
    curr = conn.cursor()
    curr.execute("SELECT courses FROM users WHERE netid = '"+netid+"';")
    trans = curr.fetchone()
    if trans == None:
        return
    trans = trans[0]
    trans = str(trans)
    trans = regex.sub("",trans)
    trans = trans.replace("[","{")
    trans = trans.replace("]","}")
    courses = str(courses)
    if courses == "":
        return
    courses = courses.split(",")
    courses_and_grades = []
    for course in courses:
        course_grad = course.split(" ")
        if course_grad[0] == "":
            continue
        #print course_grad
        if len(course_grad) == 1:
            courses_and_grades.append([course_grad[0].upper(),"None"])
        else:
            courses_and_grades.append([course_grad[0].upper(),course_grad[1].upper()])
    courses_and_grades = str(courses_and_grades)
    courses_and_grades = regex.sub("",courses_and_grades)
    courses_and_grades = courses_and_grades.replace("[","{")
    courses_and_grades = courses_and_grades.replace("]","}")
    curr.execute("UPDATE users SET courses = %s::text[] || %s::text[][], fulfilled = NULL, fulfilledcerts = NULL WHERE netid = %s;",(courses_and_grades,trans,netid))
    conn.commit()
    curr.close()
    conn.close()

# Receives a user's netid
# Returns their list of interested majors and certificates in a tuple or None for either field if empty
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
    #retmajors = []
    #retcerts = []
    if intmajors == None and intcerts == None:
        return None
    if intmajors != None:
        intmajors = intmajors[0]
    if intcerts != None:
        intcerts = intcerts[0]
    curr.close()
    conn.close()
    return (intmajors,intcerts)

# Receives a user's netid and a list of majors and certificates they are interested in
# Saves these majors and certificates to user's interested_majors, interested_certificates fields in the database
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
    conn.close()

