import phrase_extract as phe
import service_prov_db_handle as db_handle
import telepot, time, sys, os, re
from geopy.geocoders import Nominatim
import otp_sms
from goto import with_goto
import serv_decrp,search, subprocess
from easyprocess import EasyProcess

is_chatting = False
location_area=False
#number=False
db_handle.start_conn(0)
db_handle.start_conn(1)

@with_goto
def handle(msg):
    content_type,chat_type,chat_id = telepot.glance(msg)
    #print content_type, chat_type, chat_id
    if content_type is 'text':
        global is_chatting
        number=""
        res=""
        global location_area
        chat_id = msg['chat']['id']
        command = msg['text']
        print 'Got command: %s' % command
        is_chatting = True
        location_area=False
        if command.startswith('who are you') or command.startswith('/start') or command.startswith('/help'):
            bot.sendMessage(chat_id, "How this works: \n1.We process your text and check for the service. \n2. We prompt you for your phone no. and location(google map). \n3.We confirm and deliver the service via OTP.... And its Done! ")
        if command.startswith('/human'):
            if not command[7:]:
                bot.sendMessage(chat_id,"Give me an input for example: /human Are you human?")
            else:
                s = EasyProcess("zenity --entry --text=' Revert Response for: "+command[7:]+"'").call(timeout=7).stdout
                #inputText = subprocess.check_output("zenity --entry --text=' Revert Response for: "+command[7:]+"' || exit 0",shell=True,timeout=None)
                if not s:
                    bot.sendMessage(chat_id,"Admin not Available")
                else:
                    bot.sendMessage(chat_id,s)
        if not command.startswith('/') and is_chatting:
            command = command.lower()
            phraseExtracted = phe.extract_phrase(command)
            for i in range(len(phraseExtracted)):
                print phraseExtracted[i]
                if 'food' in phraseExtracted[i].split(" "):
                    phraseExtracted=['cuisines']
                if 'vehicle' in phraseExtracted[i].split(" "):
                    phraseExtracted-['vehicle_repair']
                if phraseExtracted[i] in open('location.txt').read():
                    loc_area = phraseExtracted[i]
                    someFunctoStoreValue(loc_area,"loc_area",chat_id)
                    location_area = True
                    goto .loction_acc
            prevTestValue,bit=[],False
            if phraseExtracted:
                print phraseExtracted
                for i in range(len(phraseExtracted)):
                    testValue,some_list,some_list,index = serv_decrp.match_serv_menu(phraseExtracted[i].encode('ascii','ignore'))
                    prevTestValue.append(testValue)
                print testValue,some_list,some_list,index
                if True in prevTestValue:
                    if False in prevTestValue:
                        responseStr="we tried to interpret your request, you meant "+phraseExtracted[prevTestValue.index(True)]+"? but could'nt acknowledge this  "+phraseExtracted[prevTestValue.index(False)]+" try requesting without "+ phraseExtracted[prevTestValue.index(False)]
                        bot.sendMessage(chat_id,responseStr)
                        testValue,bit=False,True
            else:
                testValue = False
            if len(phraseExtracted)==0 or testValue is False:
                xs = command.strip()

                if xs.isdigit() and len(str(xs))==10:
                    number = str(xs)
                    goto .checkno
                else:
                    xs = command
                    listedcommand=command.split(" ")
                    count=1
                    possibleValidReq = "i would send me some like to order would like to have want send me what is the score do you "
                    for word in range(len(listedcommand)):
                        if listedcommand[word] in possibleValidReq:
                            count=count+1
                    print bit
                    if count>2 :
                        if bit is False:
                            print califResponse()
                            bot.sendMessage(chat_id, califResponse())
                            bit=True
                    if bit is False:
                        res = sillybot.respond(command,chat_id)
                        print "AIML resp> "+str(res)
                        if not res:
                            res = "Exploring web\n"+search.do_a_search(command)
                            print "WEB Resp> "+str(res)
                        bot.sendMessage(chat_id,res)
                    dump(chat_id,command)
                    dump(chat_id,phraseExtracted)
                    dump(chat_id,res)
                    goto .exit
            if len(phraseExtracted)!=0 and testValue is True and isinstance(some_list, list):
                #", ".join(str(e) for e in s)
                bot.sendMessage(chat_id,"\n".join(str(e).replace("`@`",'') for e in some_list))
                goto .exit
            if len(phraseExtracted)!=0 or testValue is True:
                if os.path.isfile(str(chat_id)+".txt"):
                    dumpinfo(chat_id)  
                someFunctoStoreValue(phraseExtracted,"phraseExtracted",chat_id)
                someFunctoStoreValue(command,"command",chat_id)
            if not location_area:
                print("Location is ",location_area)
                bot.sendMessage(chat_id,"Provide us with your location")
                label .loction_acc
                phraseExtracted=someFunctoFetchValue("phraseExtracted",chat_id)
                command=someFunctoFetchValue("command",chat_id)
            if len(phraseExtracted)!=0 and location_area:
                print phraseExtracted,command,location_area
                #print (db_handle.queryCollection(phraseExtracted,command,loc_area))
                #if db_handle.queryCollection(phraseExtracted,command,loc_area)[0] == "Did you mean":
                #bot.sendMessage(chat_id, db_handle.queryCollection(phraseExtracted,command,loc_area))
                #print db_handle.queryCollection(phraseExtracted,command,loc_area)
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
                #print phraseExtracted,command,loc_area,Cust_phone

                intrmList = db_handle.queryCollection(phraseExtracted,command,loc_area)
                print intrmList
                strop = ""
                for i in range(len(intrmList)):
                    for k,v in intrmList[i].items():
                        if str(v)=='9998':
                            v='NA Req SERV'
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
        elif command.startswith('/search') or command.startswith('/s') and not command.startswith('/start'):
            print "searching web" 
            if command.startswith('/search'):
                term_to_search = command[8:]
                res = "Exploring web\n"+search.do_a_search(term_to_search)
                bot.sendMessage(chat_id,res)
            elif command.startswith('/s'):
                term_to_search = command[3:]
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
        
    elif content_type is 'audio':
    	pass
    elif content_type is 'document':
    	pass
    elif content_type is 'photo':
    	pass
    elif content_type is 'sticker':
    	pass
    elif content_type is 'video':
    	pass
    elif content_type is 'voice':
    	pass
    elif content_type is 'contact':
    	pass
    elif content_type is 'venue':
    	pass
    elif content_type is 'new_chat_member':
    	pass
    elif content_type is 'left_chat_member':
    	pass

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

def dump(chat_id,text):
    f = open("dump.txt","a")
    f.write(str(chat_id)+" : "+str(text)+"\n")
    f.close()
def califResponse():
    response = ["Sorry, I didn't get that. Sometimes I don't get things.",
                "I don't know the answer or have what you're looking for. Being an AI bot is hard :(",
                "Being a bot and all you'd think I have the answer to all your questions. Sadly, that's not the case.",
                "404 something wrong with me",
                "I was not designed to answer that. Try asking something useful.",
                "Either you phrased the question wrong or asked the wrong question. Moving on.",
                "I did not get you, probably something short-circuited in here",
                "What did you ask, did you asked me.. oh!! sorry query me something else."]
    from random import randrange
    random_index = randrange(0,len(response))
    return response[random_index]

def timeout( p ):
    if p.poll() is None:
        print 'Error: process taking too long to complete--terminating'
        p.kill()
import aiml
sillybot = aiml.Kernel()
sillybot.loadBrain('dude.brn')
try:
    f = open('dude.cred')
except IOError:
    sys.exit(1)

bot_predicates = f.readlines()
f.close()
for bot_predicate in bot_predicates:
    key_value = bot_predicate.split('::')
    if len(key_value) == 2:
        sillybot.setBotPredicate(key_value[0], key_value[1].rstrip('\n'))

# Create a bot object with API key

#bot = telepot.Bot('168791394:AAG39PL1_5IUGmZnbUv6pAOqKBQqXtyKWzo')
bot = telepot.Bot('144088369:AAHCg6tFUOmio1uoGWM89qVG2MJVNv7rGtA')
# Attach a function to notifyOnMessage call back
bot.notifyOnMessage(handle)

# Listen to the messages
while 1:
 time.sleep(1)