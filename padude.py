import telepot, time
from nltk.chat.iesha import iesha_chatbot
import phrase_extract
import service_prov_db_handle
import sys
import telepot, time
from geopy.geocoders import Nominatim
import otp_sms
import re

is_chatting = False
location_area=""
number=""

def handle(msg):
    content_type,chat_type,chat_id = telepot.glance(msg)
    #print content_type, chat_type, chat_id
    if content_type is 'text':
        global is_chatting
        number=""
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
            #bot.sendMessage(chat_id, iesha_chatbot.respond(command))
            print "Phrase Extracted ",phrase_extract.extract_phrase(command)
            #bot.sendMessage(chat_id, service_prov_db_handle.queryCollection(phrase_extract.extract_phrase(command),command))
            if len(phrase_extract.extract_phrase(command))==0:
                xs = command.strip()
                if xs.isdigit() and len(str(xs))==10:
                    number = str(xs)
            else:
                xs = command
                bot.sendMessage(chat_id,"please clarify your need.")

            if len(phrase_extract.extract_phrase(command))!=0:
                if service_prov_db_handle.queryCollection(phrase_extract.extract_phrase(command),command)[0] == "Did you mean":
                    bot.sendMessage(chat_id, service_prov_db_handle.queryCollection(phrase_extract.extract_phrase(command),command))
                print service_prov_db_handle.queryCollection(phrase_extract.extract_phrase(command),command)
                #while location_area=="":#
                #    bot.sendMessage(chat_id,"Provide us your location")
                bot.sendMessage(chat_id,"Provide us your phone no, shortly we will be sending an OTP for verifying your identity")
                if len(number)!=0:
                    phn_number = number
                    otp_sms.get_otp(phn_number,chat_id)
                    bot.sendMessage(chat_id, 'Please type "/otp" and enter the OTP you have recieved.')
        elif command == re.match(r'/otp (\S+)', command).group() and is_chatting:
            print "got it"
            if otp_sms.valid_otp(int(re.match(r'/otp (\S+)', command).group(1)),chat_id) is True:
                print "hi"
                bot.sendMessage(chat_id, 'Your number has been verified, you will be contacted by the service provider shortly')

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


# Create a bot object with API key
bot = telepot.Bot('168791394:AAG39PL1_5IUGmZnbUv6pAOqKBQqXtyKWzo')

# Attach a function to notifyOnMessage call back
bot.notifyOnMessage(handle)

# Listen to the messages
while 1:
 time.sleep(10)
