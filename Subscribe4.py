import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

##import range_sensor4
def waterlevel():
  GPIO.setmode(GPIO.BCM)
  TRIG = 23 
  ECHO = 24

  ##print "Distance Measurement In Progress"

  GPIO.setup(TRIG,GPIO.OUT)
  GPIO.setup(ECHO,GPIO.IN)

  GPIO.output(TRIG, False)
  ##print "Waiting For Sensor To Settle"
  time.sleep(2)

  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)

  while GPIO.input(ECHO)==0:
    pulse_start = time.time()

  while GPIO.input(ECHO)==1:
    pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start

  distance = pulse_duration * 17150

  distance = round(distance, 2)

  ##print "Distance:",distance,"cm"

  GPIO.cleanup()
  return distance

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("scubewater1")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
   ## print(msg.topic+" "+str(msg.payload))
    Message1 = str(msg.payload)
    MtrStatus = 0
    if(Message1 == "ON MOTOR"):
      if(waterlevel() < 10):
          print "Tank is FULL no need to on motor"
          MtrStatus = 0
      else:
          print "Motor is now ON"
          MtrStatus = 1
    elif(Message1 == "OFF MOTOR"):
      print "Motor Is now OFF"
      MtrStatus = 0
    elif(Message1 == "STATUS"):
      print "The current tank GAP is:" + str(waterlevel()) + "centimeters"
      

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.


client.loop_forever()
