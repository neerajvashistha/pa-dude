import phrase_extract as phe
def someFunctoStoreValue(somevalue,key):
	valueToFile = str(key)+":"+str(somevalue)+"\n"
	f = open("filename.txt", 'a')
	f.write(valueToFile) 
def someFunctoFetchValue(key):
	import re
	hand = open('filename.txt')
	for line in hand:
	    line = line.rstrip()
	    #print line
	    if re.search(key, line) :
	    	print type(line)
	    	if isinstance(line, basestring):
	    		print "hi"
	    		if '[u' in line:
	    			return phe.extract_phrase(line),type(phe.extract_phrase(line))
	    		else:
	    			return line.split(":")[1],type(line.split(":")[1])
	    	if isinstance(line, list):
	    		print "hello"
	    		l = re.findall(':\S+', line)
	    		return re.findall('[a-zA-Z0-9]\S*[a-zA-Z0-9]',str(l))[0],type(re.findall('[a-zA-Z0-9]\S*[a-zA-Z0-9]',str(l))[0])


phraseExtracted=someFunctoFetchValue("phraseExtracted")
command=someFunctoFetchValue("command")
loc_area=someFunctoFetchValue("loc_area")
print phraseExtracted,command,loc_area