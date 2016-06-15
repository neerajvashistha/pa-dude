import urllib2
import cookielib
#from getpass import getpass
import sys
import re
import base64
import onetimepass as otp

def sendsmses(phn_no,msg):
    username = '7066185125'
    passwd = 'deadpool227'
    message = msg
    number = phn_no
    message = "+".join(message.split(' '))

    #Logging into the SMS Site
    #initialize(phn_no,msg)

    url = 'http://site24.way2sms.com/Login1.action?'
    data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'

    #For Cookies:
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    # Adding Header detail:
    opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]

    try:
        usock = opener.open(url, data)
    except IOError:
        print "Error while logging in."
        sys.exit(1)


    jession_id = str(cj).split('~')[1].split(' ')[0]
    send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
    send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
    opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]

    try:
        sms_sent_page = opener.open(send_sms_url,send_sms_data)
    except IOError:
        print "Error while sending message"

    print "SMS has been sent."

def valid_otp(passwd,chat_id):
    my_secret = base64.b32encode(str(chat_id))
    #my_secret = 'MFRGGZDFxMZTWQ2LK'
    got_token = passwd # should be probably from some user's input
    is_valid = otp.valid_totp(token=got_token, secret=my_secret, interval_length= 300)
    return is_valid



def get_otp(Ph_number,chat_id):
    my_secret = base64.b32encode(str(chat_id))
    #my_secret = 'MFRGGZDFMZTWQ2LK'
    my_token = otp.get_totp(my_secret,interval_length = 300)
    msg = "Your One-Time-Password is "+str(my_token)+". It will be valid for 3 minutes."
    phn_no = Ph_number
    sendsmses(phn_no,str(msg))
