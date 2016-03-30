import pdfquery, re

grade_regex = re.compile("\s(A|B|C|D|F|P)(\+|-)?\s")
#import views
#import models

# must unencrypt transcript before using
# instructions we can give to user: http://smallbusiness.chron.com/remove-encryption-pdf-file-44390.html
# or http://www.pcworld.com/article/2873665/how-to-remove-encryption-from-a-pdf-file.html

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
        grade = ""
    else:
        grade,pm = s_obj[-1:][0]
        grade = grade+pm
    ret.append(dep)
    ret.append(num)
    ret.append(grade)
    #ret.append(dis_req)
    return ret

def parse_transcript(transcript):
    student = {}
    # we should search for student in our database first and update
    try:
        pdf = pdfquery.PDFQuery(transcript)
    except:
        return render_template('index.html')
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
    student['name'] =  name[i_name+1:]
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
