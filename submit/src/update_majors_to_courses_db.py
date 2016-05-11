# open db connection
# read in lines from std in
# parse as course,m or c standing for major or certificate,major,area type
# add to courses database (if already there v if not there) - should check if major area already there

# COURSE MUST BE IN FORM 3Letterdep3digits (no spaces)

# WILL JUST UPDATE WITH DUPLICATES _ BE AWARE _ ASSIGN MAJORS

import psycopg2, fileinput,re

regex = re.compile('\'|\"')

conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
curr = conn.cursor()

lines = fileinput.input()

for line in lines:
    if line == "":
        continue
    comps = line.split(",")
    if len(comps) != 4:
        continue
    new_major = []
    course = comps[0]
    area = comps[2]
    typ = comps[3].rstrip("\n")
    new_major.append(course)
    new_major.append(typ)
    new_major = str(new_major)
    new_major = new_major.replace("[","{")
    new_major = new_major.replace("]","}")
    new_major = regex.sub("",new_major)
    if comps[1] == 'c':
        curr.execute("SELECT coursetrack FROM certificates_to_courses WHERE name = '"+area+"';")
        major_area = curr.fetchone()
        if major_area != None:
            major_area = major_area[0]
            major_area = str(major_area)
            major_area = major_area.replace("[","{")
            major_area = major_area.replace("]","}")
            major_area = regex.sub("",major_area)
            print major_area
            if major_area[1] != "{" and len(major_area) > 2:
                major_area = "{" + major_area + "}"
            print major_area, new_major
            curr.execute("UPDATE certificates_to_courses SET coursetrack = %s::text[] || %s::text[][] WHERE name = %s;",(new_major,major_area,area))
            #if major_area[0] == list:
                #major_area = major_area[0]
            #curr.execute("array_append(%s,%s);",(major_area,new_major))
            #major_area = curr.fetchone()
            #print major_area
            conn.commit()
           # major_area = major_area[0] # a list of majors
           # empty_list = []
           # if len(major_area) < 1:
           #     continue
           # if major_area[0] != list:
            #    empty_list.append(major_area)
            #    major_area = empty_list
            #if new_major not in major_area:
             #   major_area.append(new_major)
             #   major_area = str(major_area)
             #   major_area = major_area.replace("[","{")
             #   major_area = major_area.replace("]","}")
             #   major_area = regex.sub("",major_area)
             #   print major_area
              #  curr.execute("UPDATE courses SET major_area = %s WHERE name = %s;",(major_area,course))
             #   conn.commit()
        else:
            #empty_list = []
            #empty_list.append(new_major)
            #major_area = empty_list
            #major_area = str(major_area)
            major_area = new_major
            #major_area = regex.sub("",major_area)
            print major_area
            curr.execute("INSERT INTO certificates_to_courses VALUES (%s,%s)",(area,major_area))
            conn.commit()
    # if major
    if comps[1] == 'm':
        curr.execute("SELECT coursetrack FROM majors_to_courses WHERE name = '"+area+"';")
        major_area = curr.fetchone()
        if major_area != None:
            major_area = major_area[0]
            major_area = str(major_area)
            major_area = major_area.replace("[","{")
            major_area = major_area.replace("]","}")
            major_area = regex.sub("",major_area)
            print major_area
            if major_area[1] != "{" and len(major_area) > 2:
                major_area = "{" + major_area + "}"
            print major_area, new_major
            curr.execute("UPDATE majors_to_courses SET coursetrack = %s::text[] || %s::text[][] WHERE name = %s;",(new_major,major_area,area))
            #if major_area[0] == list:
                #major_area = major_area[0]
            #curr.execute("array_append(%s,%s);",(major_area,new_major))
            #major_area = curr.fetchone()
            #print major_area
            conn.commit()
           # major_area = major_area[0] # a list of majors
           # empty_list = []
           # if len(major_area) < 1:
           #     continue
           # if major_area[0] != list:
            #    empty_list.append(major_area)
            #    major_area = empty_list
            #if new_major not in major_area:
             #   major_area.append(new_major)
             #   major_area = str(major_area)
             #   major_area = major_area.replace("[","{")
             #   major_area = major_area.replace("]","}")
             #   major_area = regex.sub("",major_area)
             #   print major_area
              #  curr.execute("UPDATE courses SET major_area = %s WHERE name = %s;",(major_area,course))
             #   conn.commit()
        else:
            #empty_list = []
            #empty_list.append(new_major)
            #major_area = empty_list
            #major_area = str(major_area)
            major_area = new_major
            #major_area = regex.sub("",major_area)
            print major_area
            curr.execute("INSERT INTO majors_to_courses VALUES (%s,%s)",(area,major_area))
            conn.commit()

curr.close()
conn.close()