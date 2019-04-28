import speech
import time

# Open words file for reading
f = open('words.txt','r')

# Open progress file for writing
p = open('progress.txt','w')

# List to store words
list = []

# Populate list with words from file
f.readline()
#print(f)
for line in f:
	#print(line)
	list.append(line)

i=0
while (1):
	speech.say(list[i])
	time.sleep(1)
	print(list[i])
	time.sleep(1)
	i = int(i) + int(1)
