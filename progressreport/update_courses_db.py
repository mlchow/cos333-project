# open db connection
# read in lines from std in
# parse as course,m or c standing for major or certificate,major,area type
# add to courses database (if already there v if not there) - should check if major area already there

# COURSE MUST BE IN FORM 3Letterdep3digits (no spaces)

# WILL JUST UPDATE WITH DUPLICATES _ BE AWARE _ ASSIGN MAJORS

import psycopg2, fileinput

conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
curr = conn.cursor()

lines = fileinput.input()

for line in lines:
	comps = line.split(",")
	new_major = []
	course = comps[0]
	area = comps[2]
	typ = comps[3].rstrip("\n")
	new_major.append(area)
	new_major.append(typ)
	if comps[1] == 'c':
		curr.execute("SELECT certificate_area FROM courses WHERE name = '"+course+"';")
	    	major_area = curr.fetchone()
	    	if major_area != None:
	    		major_area = major_area[0] # a list of majors
	    		if major_area[0] != list:
    				empty_list.append(major_area)
    				major_area = empty_list
	    		if new_major not in major_area:
	    			major_area.append(new_major)
	    			major_area = str(major_area)
	        		major_area = major_area.replace("[","{")
	        		major_area = major_area.replace("]","}")
	        		curr.execute("UPDATE courses SET certificate_area = %s WHERE name = %s;",(major_area,course))
	        		conn.commit()
	        else:
	        	empty_list = []
	        	empty_list.append(new_major)
	        	major_area = empty_list
	        	major_area = str(major_area)
	        	major_area = major_area.replace("[","{")
	        	major_area = major_area.replace("]","}")
	        	curr.execute("SELECT major_area FROM courses WHERE name = '"+course+"';")
	        	maj_ar = curr.fetchone()
	        	if maj_ar != None:
	        		curr.execute("UPDATE courses SET certificate_area = %s WHERE name = %s;",(major_area,course))
	        		conn.commit()
	        	else:
	        		curr.execute("INSERT INTO courses VALUES (%s,%s,%s,%s)",(course,'{}',new_major,''))
	        		conn.commit()
	# if major
	if comps[1] == 'm':
		curr.execute("SELECT major_area FROM courses WHERE name = '"+course+"';")
    	major_area = curr.fetchone()
    	if major_area != None:
    		major_area = major_area[0] # a list of majors
    		empty_list = []
    		if major_area[0] != list:
    			empty_list.append(major_area)
    			major_area = empty_list
    		if new_major not in major_area:
    			major_area.append(new_major)
    			major_area = str(major_area)
        		major_area = major_area.replace("[","{")
        		major_area = major_area.replace("]","}")
        		#print major_area
        		curr.execute("UPDATE courses SET major_area = %s WHERE name = %s;",(major_area,course))
        		conn.commit()
        else:
        	empty_list = []
        	empty_list.append(new_major)
        	major_area = empty_list
        	major_area = str(major_area)
	        major_area = major_area.replace("[","{")
	        major_area = major_area.replace("]","}")
	        curr.execute("SELECT certificate_area FROM courses WHERE name = '"+course+"';")
	        maj_ar = curr.fetchone()
	        if maj_ar != None:
	        	curr.execute("UPDATE courses SET major_area = %s WHERE name = %s;",(major_area,course))
	        	conn.commit()
	        else:
        		curr.execute("INSERT INTO courses VALUES (%s,%s,%s,%s)",(course,new_major,'{}',''))
        		conn.commit()

curr.close()
conn.close()