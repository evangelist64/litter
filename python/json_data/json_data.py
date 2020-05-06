import json
import os

with open('ddd.txt','r') as f:
	json_str = f.read()

str = json.loads(json_str)
for key in str:
	print key
	print str[key]
