import json
import pymongo
import serv_decrp
import phrase_extract
from pymongo import MongoClient

def main():
	load_JSON_into_Collection("services.json","service_type")

	#loc_serv_list = queryServNameLocation(qryd_serv_prvd_list,"Khadi Machine")

	#print(loc_serv_list)

	dropCollection("services")


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
		for document in cursor:
			alist = document.get(JSONobj_key1)[0].get("serv_prvd")

		return alist
	except Exception as e:
		print("Error has occurred", e)


def queryServNameLocation(alist, location):
	'''
	param @alist, a list with refined vendors/service providers with name, phone, loc
	param @location, str with location

	return loc_serv_list, a location based vendors/service providers,
	with name, phone, loc if @location exists, else returns @alist
	'''
	try:
		#dict = {}
		loc_serv_list =[]
		for i in alist:
			#print i
			for k,v in i.items():
				if v == location.lower():
					loc_serv_list.append(i)


		if len(loc_serv_list) == 0:
			return alist

		return loc_serv_list
	except Exception as e:
		print("Error has occurred", e)

def queryCollection(itemList,query):
	'''
	param @itemList, item could be any item decribed in serv_decrp like manchurian, or monitor or chinese

	return serv_prvd_list, which could be a list of servie providers, or menu list
	'''
	serv_prvd_list = []
	if len(itemList) !=0:
		for item in itemList:
			#fetch values from serv_decrp.py for an inquired <item>.
			boolItemExist,servItem,servDecrp = serv_decrp.match_serv_menu(item)
			#boolItemExist,servItem,servDecrp could be <true/false>,<food>,<chinese> or<true/false>,<chinese>,<menulist> or none.
			if (boolItemExist is True):
				if isinstance(servDecrp, basestring):
					serv_prvd_list += queryServName(servItem,servDecrp)
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

client = MongoClient("mongodb://192.168.0.6:27027")
db = client.test

load_JSON_into_Collection("services.json","service_type")

if __name__ == "__main__":
	client = MongoClient("mongodb://192.168.0.6:27027")
	db = client.test
	main()
	db.close
