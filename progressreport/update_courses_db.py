# open db connection
# read in lines from std in
# parse as course,m or c standing for major or certificate,major,area type
# add to courses database (if already there v if not there) - should check if major area already there

import psycopg2, fileinput

conn = psycopg2.connect('postgres://gordibbmgwbven:7uBEh3xUMiB5g9c9fpOcXg_Mr9@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d1c29niorsfphk')
curr = conn.cursor()

lines = fileinput.input()

for line in lines:
