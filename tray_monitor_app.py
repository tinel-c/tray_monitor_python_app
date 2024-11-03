import pystray
from PIL import Image
import paramiko
import re
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import time, threading
 
image_green = Image.open("monitor_green.png")
image_red = Image.open("monitor_red.png")
image_yellow = Image.open("monitor_yellow.png")
 
publishStatusTopic = "hpServerStatus/state"
publishStatusTimeTopic = "hpServerStatus/timestamp"
powerManagementStatusTopic = "hpServerStatus/powerManagementStatus"
powerManagementRequestTopic = "hpServerStatus/powerManagement"

mqttHostName = "192.168.2.4"

def after_click(icon, query):
    if str(query) == "Start server":
        icon.notify('Starting the server!')
        icon.icon = image_yellow
        publish.single(powerManagementRequestTopic, "on", hostname=mqttHostName)
    elif str(query) == "Stop server":
        icon.notify('Stoping the server!')
        icon.icon = image_yellow
        publish.single(powerManagementRequestTopic, "off", hostname=mqttHostName)
    elif str(query) == "Exit":
        icon.stop()

def change_image_red(icon,query):
    icon.icon = image_red
 
def change_image_green(icon,query):
    icon.icon = image_green

icon = pystray.Icon("GFG", image_yellow, "Server status", 
                    menu=pystray.Menu(
    pystray.MenuItem("Start server", 
                     after_click),
    pystray.MenuItem("Stop server", 
                     after_click),
    pystray.MenuItem("Exit", after_click)))
query = ""
 

 
def currentStatusOfServer(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    if  (b'Off' in message.payload):
        change_image_red(icon,query)
    else:
        change_image_green(icon,query)




icon.run_detached()
subscribe.callback(currentStatusOfServer, publishStatusTopic, hostname=mqttHostName)