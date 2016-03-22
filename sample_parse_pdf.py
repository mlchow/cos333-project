import pdfquery
import xml.etree.ElementTree as ET
# must unencrypt transcript before using
# instructions we can give to user: http://smallbusiness.chron.com/remove-encryption-pdf-file-44390.html
# or http://www.pcworld.com/article/2873665/how-to-remove-encryption-from-a-pdf-file.html
pdf = pdfquery.PDFQuery('transcript_un.pdf')
pdf.load() # arg 0 = just first page
label = pdf.pq('LTTextLineHorizontal:contains("Name: ")')
name = label.text()
label = pdf.pq('LTTextLineHorizontal:contains("Program: ")')
degree = label.text()
label = pdf.pq('LTTextLineHorizontal:contains("Plan: ")')
major = label.text()
print name,degree,major 
label = pdf.pq('LTTextLineHorizontal:contains("GRD")')
for lab in label("LTTextLineHorizontal"):
    #print label("LTTextLineHorizontal")
    top_corner = float(lab.attrib['y0'])
    bottom_corner = float(lab.attrib['y1']) 
    clas = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (0, top_corner, 620, bottom_corner)).text()
    print clas
#print label.text()
#root = ET.fromstring(label)
#for clas in root.findall("."):
#    print 1
#classes = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner, top_corner, right_corner, bottom_corner)).text()
label = pdf.pq('LTTextLineHorizontal:contains("PDF")')
for lab in label("LTTextLineHorizontal"):
    #print label("LTTextLineHorizontal")                                      
    top_corner = float(lab.attrib['y0'])
    bottom_corner = float(lab.attrib['y1'])
    clas = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (0, top_corner, 620, bottom_corner)).text()
    print clas
#print label.text()
label = pdf.pq('LTTextLineHorizontal:contains("SPF")')
for lab in label("LTTextLineHorizontal"):
    #print label("LTTextLineHorizontal")                                      
    top_corner = float(lab.attrib['y0'])
    bottom_corner = float(lab.attrib['y1'])
    clas = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (0, top_corner, 620, bottom_corner)).text()
    print clas
#print label.text()
#pdf.tree.write('transcript_xml', pretty_print=True)
#label1 = pdf.pq('LTTextLineHorizontal:contains("Basis")')
#label2 = pdf.pq('LTTextLineHorizontal:contains("Course")')
#label3 = pdf.pq('LTTextLineHorizontal:contains("Area")')
#label4 = pdf.pq('LTTextLineHorizontal:contains("2013-2014 Spring")')
#left_corner = float(label2.attr('x0'))
#right_corner = float(label3.attr('x1'))
#top_corner = float(label1.attr('y0'))
#bottom_corner = float(label4.attr('y1'))
#classes = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner, top_corner, right_corner, bottom_corner)).text()  
#print classes
#print label
#label = pdf.pq('LTTextLineHorizontal:contains("COS")')
#print label
# if next line course is blank assume title part of previous course
#left_corner = float(label.attr('x0'))
#bottom_corner = float(label.attr('y0'))
#right_corner = float(label.attr('x1'))
#top_corner = float(label.attr('y1'))
# print left_corner
#print left_corner
#print bottom_corner
#print right_corner
#print top_corner
#print label
#name = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner, top_corner, right_corner, bottom_corner)).text()
#print pdf.pq(':contains("Your first name and initial")')[0].text()
#print name
# pdf.tree.write('transcript_un.pdf', pretty_print=True)
