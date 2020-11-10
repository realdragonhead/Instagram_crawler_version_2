import subprocess
import sys
import csv
import shlex
import io

keyword_file = sys.argv[1]
i = 1

f = io.open(keyword_file, 'r', encoding='utf-8')
lines = f.readlines()

for line in lines:
	print(line)
	keyword_list = lines[i].split(",")

	for keyword in keyword_list:
		text = str(keyword)
		text.replace(' ', '')
		text.replace(',', '')

		if (keyword == ''):
			continue
	
		print('searching ', text, ' in Instagram')
		subprocess.call(['python3', 'cralwer_routine.py', text])
	
f.close()
