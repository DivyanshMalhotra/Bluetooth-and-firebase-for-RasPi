import pyrebase
import platform
import os

import glob

import time

#import RPi.GPIO as GPIO

from bluetooth import *
config={
    "apiKey": "apiKey",
    "authDomain": "appff-793ad.firebaseio.com",
    "databaseURL": "https://appff-793ad.firebaseio.com/",
    "storageBucket": "appff-793ad.appspot.com"
}
firebase =pyrebase.initialize_app(config)
db=firebase.database()

def uploadMess(tuSun,yeSun):
    db.child(tuSun).update(yeSun)
def getMAC(interface):
  # Return the MAC address of interface
  try:
    str = open('/sys/class/net/' + interface + '/address').read()
  except:
    str = "00:00:00:00:00:00"
  return str[0:17]
def stream_handler(message):
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}


os.system('modprobe w1-gpio')

os.system('modprobe w1-therm')




server_sock=BluetoothSocket( RFCOMM )

server_sock.bind(("",PORT_ANY))

server_sock.listen(1)



port = server_sock.getsockname()[1]



uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"



advertise_service( server_sock, "AquaPiServer",

                   service_id = uuid,

                   service_classes = [ uuid, SERIAL_PORT_CLASS ],

                   profiles = [ SERIAL_PORT_PROFILE ], 

#                   protocols = [ OBEX_UUID ] 

                    )
#ting = bytes(open('/sys/class/net/eth0/address').read())
ting=getMAC('eth0')

print(ting)
my_stream = db.child("database1").child(ting).child("Message").stream(stream_handler)
while True:          

        print ("Waiting for connection on RFCOMM channel %d" % port)



        client_sock, client_info = server_sock.accept()

        print ("Accepted connection from ", client_info)

        data1=''
        forQuit=''
        data=''
        while 1:
                try:

                        Data = client_sock.recv(1024)
                        if len(Data) == 0: break
                        i=0
                        if(Data[i] is 'l'):
                                #print("inside")
                                Lat=""
                                i=i+1
                                while(Data[i] is not 'L'):
                                        Lat=Lat+Data[i]
                                        i=i+1
                                #print(Lat)
                                Long=""
                                i=i+1
                                while(Data[i] is not 'a'):
                                        Long=Long+Data[i]
                                        i=i+1
                                #print(Long)
                                Alt=""
                                i=i+1
                                while(Data[i] is not 's'):
                                        Alt=Alt+Data[i]
                                        i=i+1
                                #print(Alt)
                                Speed=""
                                i=i+1
                                while(Data[i] is not 'n'):
                                        Speed=Speed+Data[i]
                                        i=i+1
                                        #print(Speed)
                                #print(Speed)
                        dataone=({'Lat':Lat,'Long':Long,'Alt':Alt,'Speed':Speed})
                        db.child("database1").child(ting).child("Location").update(dataone)       
                        print("Lat:"+Lat+" Long:"+Long+" Alt:"+Alt+" Speed:"+Speed +"\n")





                except IOError:
                        pass

                except KeyboardInterrupt:
                        print "disconnected"

                        client_sock.close()
                        server_sock.close()
                        print "all done"
                        
                        break
                data1=data
                '''
                myMess=db.child("database1").child(ting).child("Messages").get()
                if(myMess.val()==None):
                        print("NO data")
                else:
                        for alerts in myMess.each():
                                print(alerts.key())
                                print(alerts.val())
                                print("\n")

                '''
'''
data={'kiryu':"Shining Finger"}
db.child("database1").child("kenkaneki").update(data)
myMess=db.child("database1").child("kenkaneki").get()
if(myMess.val()==None):
    print("NO data")
else:
    for alerts in myMess.each():
        print(alerts.key())
        print(alerts.val())
        print("\n")
'''
