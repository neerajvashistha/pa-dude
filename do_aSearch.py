import json,base64,threading,time,urllib,HTMLParser

def uscape(text):
		try:
			return HTMLParser.HTMLParser().unescape(text)
		except:
			return text	

def do_a_search(text): 
	try:
		q = '+'.join([text])
		data = urllib.urlopen("http://api.duckduckgo.com/?q="+q+"&format=json&pretty=1&no_redirect=1").read()
		result = json.loads(data)
		if not (result["RelatedTopics"][0]["Text"]==""):
			print "hi"
			return str(uscape("Lets Seee.... \n" + (result["AbstractText"]).encode('utf8')))
		else:
			return "Hmmmmm, Nothing to say"	
	except Exception as e:
		return e
print(do_a_search("Java language"))