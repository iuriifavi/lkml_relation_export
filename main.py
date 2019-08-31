import os
import sys
import lkml
import json
import traceback


print ("Checking %s" % (sys.argv[1]))

files = []
joins = []

if os.path.isfile(sys.argv[1]):
	files.append(sys.argv[1])
else:
	for r, d, f in os.walk(sys.argv[1]):
		for file in f:
			if '.lkml' in file:
				files.append(os.path.join(r, file))

def parse_join(join):
	sql_on = ""
	sql_wheres = ""
	relationship = ""
	rel_from = ""
	rel_to = ""

	if 'sql_on' in join.keys():
		sql_on = join['sql_on']

	if 'sql_wheres' in join.keys():
		sql_wheres = join['sql_wheres']

	if 'relationship' in join.keys():
		relationship = join['relationship']

	joins.append('{},{},{}'.format(sql_on, sql_wheres, relationship))

def find_joins(explore):
	if 'join' in explore.keys():
				parse_join(parsed['join'])
	elif 'joins' in explore.keys():
		for join in explore['joins']:
			parse_join(join)

def parse(file):
	print('[parsing] {}'.format(f))
	try:
		with open(f, 'r') as file:
			parsed = lkml.load(file)
			if 'explore' in parsed.keys():
				find_joins(parsed['explore'])
			elif 'explores' in parsed.keys():
				for explore in parsed['explores']:
					find_joins(explore)

				
	except Exception as e:
		print('[parser error] {}'.format(f))
		print(traceback.format_exc())

# r=root, d=directories, f = files

for f in files:
    print('[found] {}'.format(f))

print ('Parsing')

for f in files:
	parse(f)

if joins:
	print ('Found')
	print('sql_on,sql_wheres,relationship')
	print ('\n'.join(joins))
else:
	print ('No Joins Found')