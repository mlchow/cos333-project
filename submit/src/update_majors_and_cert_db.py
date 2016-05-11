# open db connection
# read in lines from std in

# form is majororcertificatename,m_or_c,track (if none put general),number_courses_needed,can_be_substituted by/additional info, etc[opt] - any_dcount stands for any does and is double countable
# OVERALL,majororcertificatename,m_or_c,total_num_coursesneeded,num_pdfs_allowed

import psycopg2, fileinput,re

regex = re.compile('\'|\"')

conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
curr = conn.cursor()

lines = fileinput.input()

for line in lines:
    if line == "":
        continue
    comps = line.split(",")
    if len(comps) < 4:
      continue
    if len(comps) == 5 and comps[0] == "OVERALL":
        name = comps[1]
        total = comps[3]
        pdfs = comps[4]
        if comps[2] == "m":
            curr.execute("UPDATE majors SET total_num_courses_needed = %s WHERE name = %s;",(total,name))
            conn.commit()
            curr.execute("UPDATE majors SET num_pdfs_allowed = %s WHERE name = %s;",(pdfs,name))
            conn.commit()
        else:
            curr.execute("UPDATE certificates SET total_num_courses_needed = %s WHERE name = %s;",(total,name))
            conn.commit()
            curr.execute("UPDATE certificates SET num_pdfs_allowed = %s WHERE name = %s;",(pdfs,name))
            conn.commit()
        continue
    name = comps[0]
    track = comps[2]
    num_courses_need = comps[3].rstrip("\n")
    if len(comps) == 5:
      substitute = comps[4].rstrip("\n")
    else:
      substitute = "none"
    new_track_req = []
    new_track_req.append(track)
    new_track_req.append(num_courses_need)
    new_track_req.append(substitute)
    new_track_req = str(new_track_req)
    new_track_req = new_track_req.replace("[","{")
    new_track_req = new_track_req.replace("]","}")
    new_track_req = regex.sub("",new_track_req)
    if comps[1] == 'c':
        curr.execute("SELECT track_reqs FROM certificates WHERE name = '"+name+"';")
        reqs = curr.fetchone()
        if reqs != None:
            reqs = reqs[0]
            reqs = str(reqs)
            reqs = reqs.replace("[","{")
            reqs = reqs.replace("]","}")
            reqs = regex.sub("",reqs)
            #print reqs
            if reqs[1] != "{" and len(reqs) > 2:
                reqs = "{" + reqs + "}"
            #print reqs, new_major
            curr.execute("UPDATE certificates SET track_reqs = %s::text[] || %s::text[][] WHERE name = %s;",(new_track_req,reqs,name))
            #if reqs[0] == list:
                #reqs = reqs[0]
            #curr.execute("array_append(%s,%s);",(reqs,new_major))
            #reqs = curr.fetchone()
            #print reqs
            conn.commit()
           # reqs = reqs[0] # a list of majors
           # empty_list = []
           # if len(reqs) < 1:
           #     continue
           # if reqs[0] != list:
            #    empty_list.append(reqs)
            #    reqs = empty_list
            #if new_major not in reqs:
             #   reqs.append(new_major)
             #   reqs = str(reqs)
             #   reqs = reqs.replace("[","{")
             #   reqs = reqs.replace("]","}")
             #   reqs = regex.sub("",reqs)
             #   print reqs
              #  curr.execute("UPDATE courses SET reqs = %s WHERE name = %s;",(reqs,course))
             #   conn.commit()
        else:
            #empty_list = []
            #empty_list.append(new_major)
            #reqs = empty_list
            #reqs = str(reqs)
            reqs = new_track_req
            #reqs = regex.sub("",reqs)
            #print reqs
            curr.execute("INSERT INTO certificates VALUES (%s,%s,%s,%s)",(name,reqs,0,0))
            conn.commit()
    # if major
    if comps[1] == 'm':
        curr.execute("SELECT track_reqs FROM majors WHERE name = '"+name+"';")
        reqs = curr.fetchone()
        if reqs != None:
            reqs = reqs[0]
            reqs = str(reqs)
            reqs = reqs.replace("[","{")
            reqs = reqs.replace("]","}")
            reqs = regex.sub("",reqs)
            #print reqs
            if reqs[1] != "{" and len(reqs) > 2:
                reqs = "{" + reqs + "}"
            #print reqs, new_major
            curr.execute("UPDATE majors SET track_reqs = %s::text[] || %s::text[][] WHERE name = %s;",(new_track_req,reqs,name))
            #if reqs[0] == list:
                #reqs = reqs[0]
            #curr.execute("array_append(%s,%s);",(reqs,new_major))
            #reqs = curr.fetchone()
            #print reqs
            conn.commit()
           # reqs = reqs[0] # a list of majors
           # empty_list = []
           # if len(reqs) < 1:
           #     continue
           # if reqs[0] != list:
            #    empty_list.append(reqs)
            #    reqs = empty_list
            #if new_major not in reqs:
             #   reqs.append(new_major)
             #   reqs = str(reqs)
             #   reqs = reqs.replace("[","{")
             #   reqs = reqs.replace("]","}")
             #   reqs = regex.sub("",reqs)
             #   print reqs
              #  curr.execute("UPDATE courses SET reqs = %s WHERE name = %s;",(reqs,course))
             #   conn.commit()
        else:
            #empty_list = []
            #empty_list.append(new_major)
            #reqs = empty_list
            #reqs = str(reqs)
            reqs = new_track_req
            #reqs = regex.sub("",reqs)
            #print reqs
            curr.execute("INSERT INTO majors VALUES (%s,%s,%s,%s)",(name,reqs,0,0))
            conn.commit()

curr.close()
conn.close()