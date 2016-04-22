import pdfquery, re #, string

grade_regex = re.compile("\s(A|B|C|D|F|P)(\+|-)?\s")
#regex = re.compile('[%s]' % re.escape(string.punctuation))
regex = re.compile('\'|\"')
#import views
#import models

# must unencrypt transcript before using
# instructions we can give to user: http://smallbusiness.chron.com/remove-encryption-pdf-file-44390.html
# or http://www.pcworld.com/article/2873665/how-to-remove-encryption-from-a-pdf-file.html

def convert_grade_to_numeric_GPA(grade):
    if grade == "A":
        return 4.0
    elif grade == "A-":
        return 3.7
    elif grade == "B+":
        return 3.3
    elif grade == "B":
        return 3.0
    elif grade == "B-":
        return 2.7
    elif grade == "C+":
        return 2.3
    elif grade == "C":
        return 2.0
    elif grade == "C-":
        return 1.7
    elif grade == "D":
        return 1.0
    else:
        return 0.0

# get all eligible majors; 
# def getMajors(progress):
#     # code
#     return None

# returns majors and data in order of number of courses completed.
def get_major_by_courses(progress):
    progress_dictionary = show_progress(progress)
    # sort by major_gpa
    by_courses = []

    while len(progress_dictionary) > 0:
        most = 0
        best_item = None
        for key,val in progress_dictionary.iteritems():
            if progress_dictionary[key]['num_courses'] > most:
                most = progress_dictionary[key]['num_courses']
                best_item = (key,progress_dictionary[key])
        if most <= 0:
            break
        by_courses.append(best_item)
        del progress_dictionary[best_item[0]]

    return by_courses

# returns majors and data by major GPA.
def get_major_by_gpa(progress):
    progress_dictionary = show_progress(progress)
    # sort by major_gpa
    by_major = []

    while len(progress_dictionary) > 0:
        highest = 0
        best_item = []
        for key,val in progress_dictionary.iteritems():
            if progress_dictionary[key]['grade'] > highest:
                highest = progress_dictionary[key]['grade']
                best_item = (key,progress_dictionary[key])
        if highest <= 0:
            break
        by_major.append(best_item)
        del progress_dictionary[best_item[0]]

    return by_major

def old_show_progress(progress):
    progress_dictionary = {}
    for course in progress:
        name,grade,reqs = course
        name = regex.sub('',name)
        grade = regex.sub('',grade)
        if len(reqs) < 1:
            continue
        if type(reqs[0]) != list:
            major = reqs[0]
            track = reqs[1]
            major = regex.sub('',major)
            track = regex.sub('',track)
            #print major, track
            if major in progress_dictionary:
                major_dict = progress_dictionary[major]
                if track in major_dict:
                    track_list = major_dict[track]
                    track_list.append((name,grade))
                else:
                    track_list = [(name,grade)]
                progress_dictionary[major][track] = track_list
            else:
                major_dict = {}
                major_dict[track] = [(name,grade)]
                progress_dictionary[major] = major_dict
                progress_dictionary[major]['grade'] = 0.0
            if grade != "P" or grade != "":
                curr_grade_total = progress_dictionary[major]['grade']
                progress_dictionary[major]['grade']=curr_grade_total+convert_grade_to_numeric_GPA(grade)
        else:
            for req in reqs:
                major = req[0]
                track = req[1]
                major = regex.sub('',major)
                track = regex.sub('',track)
                if major in progress_dictionary:
                    major_dict = progress_dictionary[major]
                    if track in major_dict:
                        track_list = major_dict[track]
                        track_list.append((name,grade))
                    else:
                        track_list = [(name,grade)]
                    progress_dictionary[major][track] = track_list
                else:
                    major_dict = {}
                    major_dict[track] = [(name,grade)]
                    progress_dictionary[major] = major_dict
                    progress_dictionary[major]['grade'] = 0.0
                if grade != "P" or grade != "":
                    curr_grade_total = progress_dictionary[major]['grade']
                    progress_dictionary[major]['grade']=curr_grade_total+convert_grade_to_numeric_GPA(grade)
    #print progress_dictionary

    htmltoshow = ""
    for key,value in progress_dictionary.iteritems():
        htmltoshow = htmltoshow + key + "<br />"
        count_courses = 0
        for key2,value2 in value.iteritems():
            if type(value2) == list:
                htmltoshow = htmltoshow + key2 + "<br />"
                for tup in value2:
                    name,grade = tup
                    if grade != "P" and grade != "":
                        count_courses = count_courses+1
                    htmltoshow = htmltoshow + name + " " + grade + "<br />"
        if count_courses > 0:
            major_gpa = progress_dictionary[key]['grade'] / count_courses
        else:
            major_gpa = "Unknown"
        htmltoshow = htmltoshow + "Major GPA: " + str(major_gpa) + "<br /><br />"
    return htmltoshow

def late_show_progress(progress):
    progress_dictionary = {}
    for course in progress:
        name,grade,reqs = course
        name = regex.sub('',name)
        grade = regex.sub('',grade)
        if len(reqs) < 1:
            continue
        if type(reqs[0]) != list:
            major = reqs[0]
            track = reqs[1]
            major = regex.sub('',major)
            track = regex.sub('',track)
            #print major, track
            if major in progress_dictionary:
                major_dict = progress_dictionary[major]
                if track in major_dict:
                    track_list = major_dict[track]
                    track_list.append((name,grade))
                else:
                    track_list = [(name,grade)]
                progress_dictionary[major][track] = track_list
            else:
                major_dict = {}
                major_dict[track] = [(name,grade)]
                progress_dictionary[major] = major_dict
                progress_dictionary[major]['grade'] = 0.0
            if grade != "P" and grade != "" and grade != "None":
                curr_grade_total = progress_dictionary[major]['grade']
                progress_dictionary[major]['grade']=curr_grade_total+convert_grade_to_numeric_GPA(grade)
        else:
            for req in reqs:
                major = req[0]
                track = req[1]
                major = regex.sub('',major)
                track = regex.sub('',track)
                if major in progress_dictionary:
                    major_dict = progress_dictionary[major]
                    if track in major_dict:
                        track_list = major_dict[track]
                        track_list.append((name,grade))
                    else:
                        track_list = [(name,grade)]
                    progress_dictionary[major][track] = track_list
                else:
                    major_dict = {}
                    major_dict[track] = [(name,grade)]
                    progress_dictionary[major] = major_dict
                    progress_dictionary[major]['grade'] = 0.0
                if grade != "P" and grade != "" and grade != "None":
                    curr_grade_total = progress_dictionary[major]['grade']
                    progress_dictionary[major]['grade']=curr_grade_total+convert_grade_to_numeric_GPA(grade)
    # print progress_dictionary
    
    for key,val in progress_dictionary.iteritems():
        # just get the major GPA and append to the major item
        count_courses = 0
        for key2,val2 in val.iteritems():
            if type(val2) == list:
                for tup in val2:
                    name,grade = tup
                    if grade != "P" and grade != "" and grade != "None":
                        count_courses += 1
        if count_courses > 0:
            major_gpa = progress_dictionary[key]['grade'] / count_courses
            progress_dictionary[key]['grade'] = "%.2f" % major_gpa
        else:
            progress_dictionary[key]['grade'] = 'Unknown'
        progress_dictionary[key]['num_courses'] = count_courses
    return progress_dictionary

def show_progress(progress):
    progress_dictionary = {}
    if progress == None:
        return progress_dictionary
    for course in progress:
        name = course[0]
        grade = course[1]
        major = course[2]
        track = course[3]
        name = regex.sub('',name)
        grade = regex.sub('',grade)
        if major in progress_dictionary:
            major_dict = progress_dictionary[major]
            if track in major_dict:
                track_list = major_dict[track]
                track_list.append((name,grade))
            else:
                track_list = [(name,grade)]
            progress_dictionary[major][track] = track_list
        else:
            major_dict = {}
            major_dict[track] = [(name,grade)]
            progress_dictionary[major] = major_dict
            progress_dictionary[major]['grade'] = 0.0
        if grade != "P" and grade != "" and grade != "None":
            curr_grade_total = progress_dictionary[major]['grade']
            progress_dictionary[major]['grade']=curr_grade_total+convert_grade_to_numeric_GPA(grade)
    # print progress_dictionary
    for key,val in progress_dictionary.iteritems():
        # just get the major GPA and append to the major item
        count_courses = 0
        for key2,val2 in val.iteritems():
            if type(val2) == list:
                for tup in val2:
                    name,grade = tup
                    if grade != "P" and grade != "" and grade != "None":
                        count_courses += 1
        if count_courses > 0:
            major_gpa = progress_dictionary[key]['grade'] / count_courses
            progress_dictionary[key]['grade'] = "%.2f" % major_gpa
        else:
            progress_dictionary[key]['grade'] = 'Unknown'
        progress_dictionary[key]['num_courses'] = count_courses
    return progress_dictionary

# WE CAN BUILD COURSE TO DIST REQS DYNAMICALLY
def parse_course(course):
    ret = []
    dep = course[0:3]
    num = course[4:7]
    #grade_basis = course[8:10]
    dis_req = course[-3:]
    dis_req = dis_req.strip()
    # NONE will show up as ONE be aware
    #if course[-3:] == "ONE":
        #dis_req == ""
    # Writing Seminar
    if course[-1:] == "W":
        dis_req = "W"
    s_obj = grade_regex.findall(course)
    if len(s_obj) < 1:
        grade = "None"
    else:
        grade,pm = s_obj[-1:][0]
        grade = grade+pm
    depnum = dep+num
    ret.append(depnum)
    #ret.append(num)
    ret.append(grade)
    #ret.append(dis_req)
    return ret

def parse_transcript(transcript):
    student = {}
    # we should search for student in our database first and update
    try:
        pdf = pdfquery.PDFQuery(transcript)
    except:
        return render_template('index.html') # CHANGE ERROR***
    pdf.load(0) # arg(s) are the pages to consider
    label = pdf.pq('LTTextLineHorizontal:contains("Name: ")')
    name = label.text()
    label = pdf.pq('LTTextLineHorizontal:contains("Program: ")')
    degree = label.text()
    label = pdf.pq('LTTextLineHorizontal:contains("Plan: ")')
    major = label.text() # IF NO MAJOR, THIS IS JUST EMPTY
    #print name,degree,major
    i_name = name.index(" ")
    i_degree = degree.index(" ")
    i_major = ""
    if major != "":
        i_major = major.index(" ")
    new_name = name[i_name+1:].split(",")
    student['name'] =  new_name[1].strip() + " " + new_name[0].strip()
    student['degree'] = degree[i_degree+1:]
    student['major'] = major[i_major+1:]
    courses = []
    pdf.load()
    label = pdf.pq('LTTextLineHorizontal:contains("GRD")')
    for lab in label("LTTextLineHorizontal"):
        top_corner = float(lab.attrib['y0'])
        bottom_corner = float(lab.attrib['y1']) 
        clas = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (0, top_corner, 620, bottom_corner)).text()
        if clas[3] == " ":
            courses.append(clas)
    #print clas
    label = pdf.pq('LTTextLineHorizontal:contains("PDF")')
    for lab in label("LTTextLineHorizontal"):                                     
        top_corner = float(lab.attrib['y0'])
        bottom_corner = float(lab.attrib['y1'])
        clas = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (0, top_corner, 620, bottom_corner)).text()
        if clas[3] == " ":
            courses.append(clas)
    #print clas
    count_spf = 0
    label = pdf.pq('LTTextLineHorizontal:contains("SPF")')
    for lab in label("LTTextLineHorizontal"):                             
        top_corner = float(lab.attrib['y0'])
        bottom_corner = float(lab.attrib['y1'])
        clas = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (0, top_corner, 620, bottom_corner)).text()
        if clas[3] == " ":
            count_spf = count_spf+1
            courses.append(clas)
    parsed_courses = []
    for course in courses:
        parsed_courses.append(parse_course(course))
    #print clas
    student['courses'] = parsed_courses
    #studentinfo = student['name'] + '<br />' + student['degree'] + '<br />' + student['major'] + '<br />'
    #for course in student['courses']:
    #    studentinfo = studentinfo + course + '<br />'
    studentinfo = []
    studentinfo.append(student['name'])
    studentinfo.append(student['degree'])
    studentinfo.append(student['major'])
    studentinfo.append(student['courses'])
    studentinfo.append(count_spf)
    #curr.execute("INSERT INTO Users VALUES (%s,%s,%s)",(student['name'],student['degree'],student['major']))
    #conn.commit()
    #curr.close()
    #conn.close()
    return studentinfo
    #return '<html><head><title></title></head><body><h1>Your Progress</h2>'+studentinfo+'</body></html>'
    #print student
