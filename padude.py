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
            is_chatting = True
            bot.sendMessage(chat_id, 'Hello there, how may i help you?')
        elif command == '/stopchat':
            is_chatting = False
            bot.sendMessage(chat_id, 'Bye Bye. take care!')
        elif not command.startswith('/') and is_chatting:
            phraseExtracted = phe.extract_phrase(command)
            if len(phraseExtracted)!=0:
                someFunctoStoreValue(phraseExtracted,"phraseExtracted")
                someFunctoStoreValue(command,"command")
            if len(phraseExtracted)==0:
                xs = command.strip()
                if xs.isdigit() and len(str(xs))==10:
                    number = str(xs)
                    goto .checkno
                else:
                    xs = command
                    bot.sendMessage(chat_id,"please clarify your need.")
            if not location_area:
                #location_area = True
                bot.sendMessage(chat_id,"Provide us with your location")
                label .loction_acc
                phraseExtracted=someFunctoFetchValue("phraseExtracted")
                command=someFunctoFetchValue("command")
            if len(phraseExtracted)!=0 and location_area:
                if db_handle.queryCollection(phraseExtracted,command,loc_area)[0] == "Did you mean":
                    bot.sendMessage(chat_id, db_handle.queryCollection(phraseExtracted,command,loc_area))
                print db_handle.queryCollection(phraseExtracted,command,loc_area)

                bot.sendMessage(chat_id,"Provide us your phone no, shortly we will be sending an OTP for verifying your identity")
                goto .checkno
                label .dispResult
                phraseExtracted=someFunctoFetchValue("phraseExtracted")
                command=someFunctoFetchValue("command")
                loc_area=someFunctoFetchValue("loc_area")
                print phraseExtracted,command,loc_area

                intrmList = db_handle.queryCollection(phraseExtracted,command,loc_area)
                strop = ""
                for i in range(len(intrmList)):
                    for k,v in intrmList[i].items():
                        strop += str(k)+ " : "+str(v) +"\n"
                bot.sendMessage(chat_id,strop)
                label .checkno
            if len(number)!=0:
                phn_number = number
                otp_sms.get_otp(phn_number,chat_id)
                bot.sendMessage(chat_id, 'Please type "/otp" and enter the 6-digit OTP you have recieved. For e.g. /otp 123456')

        elif command == re.match(r'/otp (\S+)', command).group() and is_chatting:
            print "got it"
            if otp_sms.valid_otp(int(re.match(r'/otp (\S+)', command).group(1)),chat_id) is True:
                print "hi"
                bot.sendMessage(chat_id, 'Your number has been verified, you will be contacted by the service provider shortly')
                goto .dispResult
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
        location_list = str(location).split(',')
        max_index = len(location_list) - 1
        location_area = location_list[max_index - 4]
        print 'Location is %s' % location_area
        loc_area = location_area.lower().strip()
        someFunctoStoreValue(loc_area,"loc_area")
        location_area = True
        goto .loction_acc

def someFunctoStoreValue(somevalue,key):
    valueToFile = str(key)+":"+str(somevalue)+"\n"
    f = open("filename.txt", 'a')
    f.write(valueToFile)
    f.close()
def someFunctoFetchValue(key):
    lis = []
    hand = open('filename.txt')
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
# Create a bot object with API key
bot = telepot.Bot('168791394:AAG39PL1_5IUGmZnbUv6pAOqKBQqXtyKWzo')

# Attach a function to notifyOnMessage call back
bot.notifyOnMessage(handle)

# Listen to the messages
while 1:
 time.sleep(10)
