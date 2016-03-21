import json,base64,threading,time,urllib,HTMLParser
#import unirest

def uscape(text):
		try:
			return HTMLParser.HTMLParser().unescape(text)
		except:
			return text	

def do_a_search(text): 
	try:
		q = '+'.join([text])
		url = "http://api.duckduckgo.com/?q="+q+"&format=json&pretty=1&no_redirect=1"
		#print url
		data = urllib.urlopen(url).read()
		result = json.loads(data)
		if result["AbstractText"]:
			return (result["AbstractText"]).encode('utf8')
		elif result["RelatedTopics"]:
			return result["RelatedTopics"][0]["Text"].encode('utf8')
		else:
			return "Hmmmmm, Nothing to say"
	except Exception as e:
		return e

#print(do_a_search("captain america"))