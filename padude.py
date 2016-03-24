import telepot, time
from nltk.chat.iesha import iesha_chatbot
import phrase_extract as phe
import service_prov_db_handle as db_handle
import sys
import telepot, time
from geopy.geocoders import Nominatim
import otp_sms
import re,time
from goto import with_goto
import pickle
import os
import sillybot,serv_decrp,search

is_chatting = False
location_area=False
#number=False

@with_goto
def handle(msg):
    content_type,chat_type,chat_id = telepot.glance(msg)
    #print content_type, chat_type, chat_id
    if content_type is 'text':
        global is_chatting
        number=""
        global location_area
        chat_id = msg['chat']['id']
        command = msg['text']
        print 'Got command: %s' % command
        if command == '/hello' and not is_chatting:
            bot.sendMessage(chat_id, 'Hello, how are you?')
        elif command == '/chat':
            if os.path.isfile(str(chat_id)+".txt"):
                dumpinfo(chat_id)
                os.remove(str(chat_id)+".txt")
            is_chatting = True
            location_area=False
            bot.sendMessage(chat_id, 'Hello there, how may i help you?')
        elif command == '/stopchat':
            is_chatting = False
            bot.sendMessage(chat_id, 'Bye Bye. take care!')
        elif not command.startswith('/') and is_chatting:
            dump(chat_id,command)
            phraseExtracted = phe.extract_phrase(command)
            dump(chat_id,phraseExtracted)
            if phraseExtracted:
                print phraseExtracted
                testValue,some_list,some_list,index = serv_decrp.match_serv_menu(phraseExtracted[0].encode('ascii','ignore'))
            else:
                testValue = False
            if len(phraseExtracted)==0 or testValue is False:
                xs = command.strip()
                if xs.isdigit() and len(str(xs))==10:
                    number = str(xs)
                    goto .checkno
                else:
                    xs = command
                    print "AIML resp>"
                    res = sillybot.responds(command,chat_id)
                    if not res:
                        print "WEB Resp>"
                        res = "Exploring web\n"+search.do_a_search(command)
                    dump(chat_id,res)
                    bot.sendMessage(chat_id,res)
                    goto .exit
            if len(phraseExtracted)!=0 or testValue is True:
                someFunctoStoreValue(phraseExtracted,"phraseExtracted",chat_id)
                someFunctoStoreValue(command,"command",chat_id)
            if not location_area:
                print(location_area)
                bot.sendMessage(chat_id,"Provide us with your location")
                label .loction_acc
                phraseExtracted=someFunctoFetchValue("phraseExtracted",chat_id)
                command=someFunctoFetchValue("command",chat_id)
            if len(phraseExtracted)!=0 and location_area:
            	print phraseExtracted,command,location_area
            	#print (db_handle.queryCollection(phraseExtracted,command,loc_area))
                #if db_handle.queryCollection(phraseExtracted,command,loc_area)[0] == "Did you mean":
                #bot.sendMessage(chat_id, db_handle.queryCollection(phraseExtracted,command,loc_area))
                print db_handle.queryCollection(phraseExtracted,command,loc_area)
                if db_handle.queryCollection(phraseExtracted,command,loc_area)[0] == "Item/Service not avail":
                    dump(chat_id,"Sorry, Item/Service is not availiable")
                    bot.sendMessage(chat_id, "Sorry, Item/Service is not availiable")
                    os.remove(str(chat_id)+".txt")
                    goto .exit
                    print "exiting chat error service NA"
                elif isinstance(db_handle.queryCollection(phraseExtracted,command,loc_area),basestring):
                    bot.sendMessage(chat_id, db_handle.queryCollection(phraseExtracted,command,loc_area))
                    goto .exit
                
                bot.sendMessage(chat_id,"Provide us your phone no, shortly we will be sending an OTP for verifying your identity")
                goto .exit
                label .dispResult
                phraseExtracted=someFunctoFetchValue("phraseExtracted",chat_id)
                command=someFunctoFetchValue("command",chat_id)
                loc_area=someFunctoFetchValue("loc_area",chat_id)
                Cust_phone = someFunctoFetchValue("cust_phone",chat_id)
                #print Cust_phone
                location = someFunctoFetchValue("cust_location",chat_id)
                Cust_location = ",".join(location.split(",")[1:4])
                #print phraseExtracted,command,loc_area

                intrmList = db_handle.queryCollection(phraseExtracted,command,loc_area)
                strop = ""
                for i in range(len(intrmList)):
                    for k,v in intrmList[i].items():
                        strop += str(k)+ " : "+str(v) +"\n"
                serv_prov_phone = re.findall("phone : ([0-9]{10})",strop)
                requirement = "CUST_PH: "+Cust_phone+"\n"+"SRV/ITM: "+",".join(phraseExtracted)+"\n"+"ADD: "+Cust_location
                #print serv_prov_phone,requirement
                for ser_phon in serv_prov_phone:
                    otp_sms.sendsmses(ser_phon,requirement)
                bot.sendMessage(chat_id,strop)
                dumpinfo(chat_id)
                label .checkno
            if len(number)!=0:
                phn_number = number
                someFunctoStoreValue(phn_number,"cust_phone",chat_id)
                otp_sms.get_otp(phn_number,chat_id)
                bot.sendMessage(chat_id, 'Please type "/otp" and enter the 6-digit OTP you have recieved. For e.g. /otp 123456')
                label .exit
                
        elif command.startswith('/otp') and is_chatting:
            print "Recieved OTP"
            if otp_sms.valid_otp(int(re.match(r'/otp (\S+)', command).group(1)),chat_id) is True:
                print "isValid OTP"
                bot.sendMessage(chat_id, 'Your number has been verified, you will be contacted by the service provider shortly')
                goto .dispResult
            else:
                print "isNOTValid OTP"
            	bot.sendMessage(chat_id, "Try again, send us your number again.")
        elif command.startswith('/search'):
            print "searching web" 
            term_to_search = command[8:]
            res = "Exploring web\n"+search.do_a_search(term_to_search)
            bot.sendMessage(chat_id,res)

        else:
            pass
    elif content_type is 'location':
        loc = msg['location']
        loc_list = loc.values()
        loc_list_lat , loc_list_long = loc_list[0] , loc_list[1]
        loc_str = str(loc_list_lat) + ',' + str(loc_list_long)

        geolocator = Nominatim()
        location = geolocator.reverse(loc_str,timeout=10)
        #location_area = str(str(location).split(",")[-5])
        someFunctoStoreValue(str(location),"cust_location",chat_id)
        location_list = str(location).split(',')
        max_index = len(location_list) - 1
        location_area = location_list[max_index - 4]
        print 'Location is %s' % location_area
        loc_area = location_area.lower().strip()
        someFunctoStoreValue(loc_area,"loc_area",chat_id)
        location_area = True
        goto .loction_acc

def someFunctoStoreValue(somevalue,key,chat_id):
    valueToFile = str(key)+":"+str(somevalue)+"\n"
    f = open(str(chat_id)+".txt", 'a')
    f.write(valueToFile)
    f.close()
def someFunctoFetchValue(key,chat_id):
    lis = []
    hand = open(str(chat_id)+".txt")
    for line in hand:
        line = line.rstrip()
        #print line
        if re.search(key, line) :
            #print type(line)
            if isinstance(line, basestring):
                if '[u' in line:
                    return phe.extract_phrase(line)
                else:
                    return line.split(":")[1]
            if isinstance(line, list):
                l = re.findall(':\S+', line)
                lis = re.findall('[a-zA-Z0-9]\S*[a-zA-Z0-9]',str(l))[0]
    hand.close()
    return lis
def dumpinfo(chat_id):
    f = open("dump.txt","a")
    hand = open(str(chat_id)+".txt")
    f.write("[chat_id:"+str(chat_id)+"]\n")
    f.write(hand.read())
    f.write("--------------------------\n")
    os.remove(str(chat_id)+".txt")
# Create a bot object with API key

def dump(chat_id,text):
    f = open("dump.txt","a")
    f.write(str(chat_id)+" : "+str(text)+"\n")
    f.close()

bot = telepot.Bot('168791394:AAG39PL1_5IUGmZnbUv6pAOqKBQqXtyKWzo')

# Attach a function to notifyOnMessage call back
bot.notifyOnMessage(handle)

# Listen to the messages
while 1:
 time.sleep(1)
