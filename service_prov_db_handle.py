import json
import pymongo
import serv_decrp
import phrase_extract
from pymongo import MongoClient
import re
import numpy as np

def main():
	load_JSON_into_Collection("services.json","service_type")

	#loc_serv_list = queryServNameLocation(qryd_serv_prvd_list,"Khadi Machine")

	#print(loc_serv_list)
	#alist1 = queryServName("food","chinese")
	phraseExtracted = someFunctoFetchValue("phraseExtracted")
	print phraseExtracted
	command="I want Manchurian"
	loc_area="katra"
	print(queryCollection(phraseExtracted,command,loc_area))
	intrmList = queryCollection(phraseExtracted,command,loc_area)
	strop = ""
	for i in range(len(intrmList)):
		for k,v in intrmList[i].items():
			strop += str(k)+ " : "+str(v) +"\n"
	print strop
	dropCollection("services")

def someFunctoFetchValue(key):
	import re
	hand = open('filename.txt')
	for line in hand:
	    line = line.rstrip()
	    #print line
	    if re.search(key, line) :
	    	#print type(line)
	    	if isinstance(line, basestring):
	    		return phrase_extract.extract_phrase(line)
	    	if isinstance(line, list):
	    		l = re.findall(':\S+', line)
	    		return re.findall('[a-zA-Z0-9]\S*[a-zA-Z0-9]',str(l))[0]

def load_JSON_into_Collection(filename,JSONobj):
	'''
	param @filename, filename of json file, note: pathname is not validated here for now
	param @JSONobj, first JSON obj to be identified by system.

	returns NULL

	Load and insert JSON file to db.<collection>
	'''
	try:
		page = open(filename, 'r')
		parsed = json.loads(page.read())
		collection = db[filename.split('.',1)[0]]
		for item in parsed[JSONobj]:
			collection.insert(item)
	except Exception as e:
		print("Error has occurred", e)




def queryServName(JSONobj_key1,JSONobj_key2):
	'''
	param @JSONobj_key1, service type identifier
	param @JSONobj_key2, service sub type identifier

	returns a list[] with phone, serv_loc, serv_name needs iter to get dict

	returns all vendors/service providers not based on location, see also queryServName
	'''
	#cursor = db.services.find({"food.type":"chinese"},{"food.$":1,"_id":0})
	#print JSONobj_key1+".type",JSONobj_key1+".$"
	try:
		cursor = db.services.find({JSONobj_key1+".type":JSONobj_key2},{JSONobj_key1+".$":1,"_id":0})
		alist = []
		index = 3
		for document in cursor:
			alist = document.get(JSONobj_key1)[0].get("serv_prvd")
		#for i in range(len(alist)):
		#	for key,value in alist[i].items():
		#		print key," : ", value

		return alist
	except Exception as e:
		print("Error has occurred", e)


def queryServNameLocation(alist, location,index): 
	'''
	param @alist, a list with refined vendors/service providers with name, phone, loc
	param @location, str with location

	return loc_serv_list, a location based vendors/service providers,
	with name, phone, loc if @location exists, else returns @alist
	'''
	try:
		#dict = {}
		priceList=list()
		loc_serv_list =[]
		blist=[]
		for i in alist:
			#print i
			for k,v in i.items():
				if v == location.lower():
					loc_serv_list.append(i)
		if len(loc_serv_list) !=0:
			compPrice = 0;
			for i in range(len(loc_serv_list)):
				for key,value in loc_serv_list[i].items():
					if key == "menuprice":
						price = value[index]
						priceList.append(price)
						loc_serv_list[i].pop('menuprice')
				loc_serv_list[i]['price'] = price 
					#print key," : ", value

			#print priceList
			lowPri = np.min(a[np.nonzero(priceList)])
			
			for i in range(len(loc_serv_list)):
				for key,value in loc_serv_list[i].items():
					if key == "price" and value == lowPri:
						blist.append(loc_serv_list[i])
					

			return blist
		if len(loc_serv_list) == 0:
			for i in alist:
				for key,value in i.items():
					if key == "menuprice":
						price = value[index]
						i.pop('menuprice')
				i['price'] = price
			return alist
		#return loc_serv_list
	except Exception as e:
		print("Error has occurred", e)

def queryCollection(itemList,query,location):
	'''
	param @itemList, item could be any item decribed in serv_decrp like manchurian, or monitor or chinese

	return serv_prvd_list, which could be a list of servie providers, or menu list
	'''
	serv_prvd_list = []
	serv_prvd_list1 = []
	if len(itemList) !=0:
		for item in itemList:
			#fetch values from serv_decrp.py for an inquired <item>.
			boolItemExist,servItem,servDecrp,indexForMenuprice= serv_decrp.match_serv_menu(item)#change func match_serv_menu
			#boolItemExist,servItem,servDecrp could be <true/false>,<food>,<chinese> or<true/false>,<chinese>,<menulist> or none.
			if (boolItemExist is True):
				if isinstance(servDecrp, basestring):
					serv_prvd_list1 += queryServName(servItem,servDecrp)#change func queryServName
					#print serv_prvd_list1,indexForMenuprice
					serv_prvd_list = queryServNameLocation(serv_prvd_list1,location,indexForMenuprice)
					#print serv_prvd_list
				elif isinstance(servDecrp, list):
					serv_prvd_list = servDecrp
			elif (boolItemExist is False):
				serv_prvd_list = ["Did you mean", phrase_extract.extract_phrase(query)]
	else:
		serv_prvd_list = ["ok"]
	return serv_prvd_list

def dropCollection(col_name):
	'''
	param @col_name, collection name
	return NULL

	drops collection
	'''
	try:
		db.drop_collection(col_name)
	except Exception as e:
		print("Error has occurred", e)

client = MongoClient("mongodb://192.168.100.5:27027")
db = client.test

load_JSON_into_Collection("services.json","service_type")

if __name__ == "__main__":
	client = MongoClient("mongodb://192.168.100.5:27027")
	db = client.test
	main()
	db.close
