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
	
	text = lines[i]
	text = str(text)
	text.replace(',', '')
	text.replace(' ', '')
	
	print('searching ', text, ' in Instagram')
	subprocess.call(['python3', 'crawler_routine.py', text])
	
f.close()