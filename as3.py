import sys

import dbus
import dbus.glib
import dbus.decorators
import gobject
import os
import re
import time
from nltk.chat.iesha import iesha_chatbot
    
# This method is execute when a message is receive
def received_im_msg(account, name, message, conversation, flags):
    global is_chatting
    print "Recieved message:" ,message
    print "account=[" + str(account) + "], name=[" + str(name) + "], message=[" + str(message) + "], conversation=[" + str(conversation) + "], flags=[" + str(flags) + "]"
    text = "%s says %s" % (name, message)
    if not conversation:
        conversation = purple.PurpleConversationNew(1, account, name)
    im = purple.PurpleConversationGetImData(conversation)
    print "im=[" + str(im) + "]"
    if message == 'hello' and not is_chatting:
         purple.PurpleConvImSend(im, 'Hello, how are you?')
    if message == '/chat':
        is_chatting = True
        purple.PurpleConvImSend(im, 'Hi I am son of Odin, people call me Thor. Who are You?')
    #send_message = raw_input("You said: ")
    send_message = "";
    send_message = iesha_chatbot.respond(message);
    purple.PurpleConvImSend(im, send_message )
    print "You said: "+send_message
    protocol = purple.PurpleAccountGetProtocolName(account)
    print "protocol = " + protocol
    #text = re.sub("<.*?>", "", text)#html2text    
  
# This method is excute when a buddy is sign on
def buddy_signed_on(buddyid):
    alias = purple.PurpleBuddyGetAlias(buddyid)
    text = "%s is online" % alias
    text=text.encode('utf-8')
    #print text

def spew(*args, **kw):
    print ""
    #print args
    #print kw

# Main

bus = dbus.SessionBus()
#bus = dbus.SystemBus()

try:
    obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
    purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")
except dbus.DBusException:
    print "Pidgin is not launched"
    sys.exit(1)

'''bus.add_signal_receiver(spew,
                        dbus_interface = "im.pidgin.purple.PurpleInterface",
                        )
'''

bus.add_signal_receiver(received_im_msg,
                        dbus_interface = "im.pidgin.purple.PurpleInterface",
                        signal_name = "ReceivedImMsg")

bus.add_signal_receiver(buddy_signed_on,
                        dbus_interface = "im.pidgin.purple.PurpleInterface",
                        signal_name = "BuddySignedOn")


print "*Waiting for a Buddy to start conversation.*"
loop = gobject.MainLoop()
loop.run()