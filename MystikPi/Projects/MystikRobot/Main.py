import sys
sys.path.insert(0,'../../Library')

import time
from grovepi import *
from Network import *

# settings
networkPort = 12346

# configuration
network = Network(networkPort)

# init
setRGB(255,0,0)
setText("Loading...\n"+network.getIpAddress())

time.sleep(100)

while True:
  print("Waiting for connection")
  setRGB(255,0,0)
  setText("Waiting for connection\n"+network.getIpAddress())
  network.waitForConnection()
  print("Connected")
  setRGB(0,255,0)
  setText("Connected\n"+network.getIpAddress())
  while True:
    try:
      command = network.read();
      if(command != None):
        print("Received '" + command + "'")
        network.write("Received '" + command + "'");
        setText(message+"\n"+network.getIpAddress())
      else:
        time.sleep(1)
        print(".")
    except IOError:
      print("Connection lost")
      setRGB(255,0,0)
      setText("Connected\n"+network.getIpAddress())
      break