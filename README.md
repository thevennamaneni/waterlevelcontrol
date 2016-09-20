# waterlevelcontrol
An IoT based Water Level controller based on the MQTT protocol

There are two scripts in the folder. range_sensor and subscribe. The range sensor checks the water level, controls the relay and uploads the data to the topic 'scubewater'(had to come up with some random name) on test.mosquitto.org. The subscribe script listens on the topic 'scubewater1' and then does the required actions.

Note: The above scripts will not work on a PC. copy it to a raspberry pi.
