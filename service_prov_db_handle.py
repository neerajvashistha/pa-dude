import json
import pymongo
import serv_decrp,sillybot
import phrase_extract
from pymongo import MongoClient
import re
import ast,math
from collections import defaultdict

def main():
	load_JSON_into_Collection("services.json","service_type")

	#loc_serv_list = queryServNameLocation(qryd_serv_prvd_list,"Khadi Machine")

	#print(loc_serv_list)
	#alist1 = queryServName("food","chinese")
	#phraseExtracted = someFunctoFetchValue("phraseExtracted")
	#print phraseExtracted
	#phraseExtracted = ['manchurian','rice']
	#command="Haa got you"
	#print command
	#phraseExtracted = phrase_extract.extract_phrase(command)
	#loc_area="katraj"
	#print(queryCollection(phraseExtracted,command,loc_area))
	#intrmList = []
	#intrmList = queryCollection(phraseExtracted,command,loc_area)
	#strop = ""
	#for i in range(len(intrmList)):
	#	for k,v in intrmList[i].items():
	#		strop += str(k)+ " : "+str(v) +"\n"
	#print strop
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
		index = 3
		for document in cursor:
			alist = document.get(JSONobj_key1)[0].get("serv_prvd")
		#for i in range(len(alist)):
		#	for key,value in alist[i].items():
		#		print key," : ", value

		return alist
	except Exception as e:
		print("Error has occurred", e)


def queryServNameLocation(alist, location,index_dict):
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
		uniloc_serv_list=[]
		price =0
		for i in alist:
			#print i
			for k,v in i.items():
				if v == location.lower():
					loc_serv_list.append(str(i))#stringify the list for the purpose of finding unique list.
		#print "\nhi",loc_serv_list
		uniloc_serv_list = unique(loc_serv_list)
		#print index_dict
		#print uniloc_serv_list
		compPriceList = []
		priceList = []
		if len(loc_serv_list) !=0:
			for serv_ty,index in index_dict.items():
				for i in range(len(uniloc_serv_list)):
					for key, value in uniloc_serv_list[i].items():
						if value == serv_ty:
							priceList.append(lowFucn(uniloc_serv_list[i],index))

			#print priceList
			temp = priceList[0].get("serv_type")	
			#print temp
			lowPri = 9999				
			for i in range(len(priceList)):
				typz = priceList[i].get("serv_type")
				#print typz
				if typz in priceList[i].values():
					price = priceList[i].get("price")
					if price is u"-999":
						priceList[i]['price']="Req"
						blist.append(priceList[i])
					if price<lowPri and temp == typz:
						lowPri = price
						blist.append(priceList[i])
					else:
						lowPri=9999
					temp = typz
			for i in range(len(blist)):
				blist[i].pop("serv_type")

			
		if len(uniloc_serv_list) == 0 or len(blist) == 0:
			someLst = []
			for i in alist:
				someLst.append(str(i))# as unique() takes list have strings form dict only 
			uniqueList = unique(someLst)
			#print uniqueList
			for serv_ty,index in index_dict.items():
				for i in range(len(uniqueList)):
					for key, value in uniqueList[i].items():
						if value == serv_ty:
							priceList.append(lowFucn(uniqueList[i],index))

			#print "hi",priceList
			temp = priceList[0].get("serv_type")	
			#print temp
			lowPri = 9999				
			for i in range(len(priceList)):
				typz = priceList[i].get("serv_type")
				#print typz
				if typz in priceList[i].values():
					price = priceList[i].get("price")
					if price is u"9999":
						priceList[i]['price']="Req"
						blist.append(priceList[i])
					if price<lowPri and temp == typz:
						lowPri = price
						blist.append(priceList[i])
					else:
						lowPri=9999
					temp = typz
			for i in range(len(blist)):
				blist[i].pop("serv_type")
		if len(blist)==0:
			blist = ["Item/Service not avail"]

		return [blist[0]]

	#return loc_serv_list
	except Exception as e:
		print("Error has occurred", e)

def lowFucn(adict,alist):
	price=0
	for key,value in adict.items():
		if key =="menuprice":
			#print value[alist[0]]
			for i in range(len(alist)):
				if value[alist[i]]!=0:
					price+=value[alist[i]]
				else:
					price = u"9999"
			adict.pop("menuprice")
			adict['price'] = price
	return adict

def unique(seq):
    seen = set()
    seen_add = seen.add
    alist = [x for x in seq if not (x in seen or seen_add(x))]
    #print type(alist)
    uniqueList = []
    for i in range(len(alist)):
			uniqueList.append(ast.literal_eval(alist[i]))
    return uniqueList

def queryCollection(itemList,query,location):
	'''
	param @itemList, item could be any item decribed in serv_decrp like manchurian, or monitor or chinese

	return serv_prvd_list, which could be a list of servie providers, or menu list
	'''
	i=0
	serv_prvd_list = []
	serv_prvd_list1 = []
	index_dict = defaultdict(list)
	if len(itemList) !=0:
		for item in itemList:
			#fetch values from serv_decrp.py for an inquired <item>.
			boolItemExist,servItem,servDecrp,indexForMenuprice= serv_decrp.match_serv_menu(item)#change func match_serv_menu
			#boolItemExist,servItem,servDecrp could be <true/false>,<food>,<chinese> or<true/false>,<chinese>,<menulist> or none.
			if (boolItemExist is False):
				#sillybot.load()
				stri = sillybot.responds(query)
				return stri
				#return str("Did you mean "+" ".join(phrase_extract.extract_phrase(query)))

			if (boolItemExist is True):
				if isinstance(servDecrp, basestring):
					#print "\nhe",serv_prvd_list1,indexForMenuprice
					serv_prvd_list1 += queryServName(servItem,servDecrp)#change func queryServName
					#serv_prvd_list1=[]
					#print serv_prvd_list
					index_dict[servDecrp].append(indexForMenuprice)

				elif isinstance(servDecrp, list):
					serv_prvd_list = servDecrp
			
		#print serv_prvd_list1
		#print [index_dict]
		serv_prvd_list = queryServNameLocation(serv_prvd_list1,location,index_dict)
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

client = MongoClient("mongodb://192.168.203.130:27027")
db = client.test

load_JSON_into_Collection("services.json","service_type")

if __name__ == "__main__":
	client = MongoClient("mongodb://192.168.203.130:27027")
	db = client.test
	main()
	db.close
