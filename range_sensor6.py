import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
##GPIO.setmode(GPIO.BCM)



def OnBuzzer():
  GPIO.setmode(GPIO.BCM)
  BUZZER = 4
  GPIO.setup(BUZZER,GPIO.OUT)
  GPIO.output(BUZZER, True)
  time.sleep(1)
  GPIO.output(BUZZER, False)
  GPIO.cleanup()
def OnMotor():
  GPIO.setmode(GPIO.BCM)
  RELAY = 25
  GPIO.setup(RELAY,GPIO.OUT)
  GPIO.output(RELAY, True)
def OffMotor():
  GPIO.setmode(GPIO.BCM)
  RELAY = 25
  GPIO.setup(RELAY,GPIO.OUT)
  GPIO.output(RELAY, False)
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
  ##return distance
  if(distance > 10.0):
    OnMotor()
  elif(distance < 5.0):
    OffMotor()
    OnBuzzer()
  return distance
while(1):
  
  depth = waterlevel()
  mqttc = mqtt.Client("python_pub")
  mqttc.connect("test.mosquitto.org", 1883)
  mqttc.publish("scubewater",depth)
  mqttc.loop(2)
  time.sleep(4)




