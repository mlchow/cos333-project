# Under MIT License

import pdfquery
import xml.etree.ElementTree as ET

#import cgi
#form = cgi.FieldStorage()
#file = form.getvalue('transcript')
#print transcript

# must unencrypt transcript before using
# instructions we can give to user: http://smallbusiness.chron.com/remove-encryption-pdf-file-44390.html
# or http://www.pcworld.com/article/2873665/how-to-remove-encryption-from-a-pdf-file.html

student = {}
# we should search for student in our database first and update

pdf = pdfquery.PDFQuery('transcript_un.pdf')
pdf.load(0) # arg(s) are the pages to consider
label = pdf.pq('LTTextLineHorizontal:contains("Name: ")')
name = label.text()
label = pdf.pq('LTTextLineHorizontal:contains("Program: ")')
degree = label.text()
label = pdf.pq('LTTextLineHorizontal:contains("Plan: ")')
major = label.text()
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
label = pdf.pq('LTTextLineHorizontal:contains("SPF")')
for lab in label("LTTextLineHorizontal"):                                      
    top_corner = float(lab.attrib['y0'])
    bottom_corner = float(lab.attrib['y1'])
    clas = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (0, top_corner, 620, bottom_corner)).text()
    if clas[3] == " ":
        courses.append(clas)
#print clas
student['courses'] = courses
#print student
