import telepot, time
from nltk.chat.iesha import iesha_chatbot
import phrase_extract
import service_prov_db_handle
import sys
import telepot, time
from geopy.geocoders import Nominatim


is_chatting = False

def handle(msg):
    content_type,chat_type,chat_id = telepot.glance(msg)
    #print content_type, chat_type, chat_id
    if content_type is 'text':
        global is_chatting
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
            bot.sendMessage(chat_id, service_prov_db_handle.queryCollection(phrase_extract.extract_phrase(command),command))
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
