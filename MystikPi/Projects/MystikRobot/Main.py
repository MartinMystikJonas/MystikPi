import sys
sys.path.insert(0,'../../Library')

import time
from grovepi import *
from Network import *
from RgbDisplay import *

# settings
networkPort = 12346

# configuration
network = Network(networkPort)
display = RgbDisplay()

# init
display.warning("Loading...\n"+network.getIpAddress()+":"+str(networkPort))

time.sleep(3)

print("Waiting for connection")
display.info("Ready on "+str(networkPort)+"\n"+network.getIpAddress()+":"+str(networkPort))

while True:
  network.waitForConnection()
  print("Connected")
  display.success("Connected\n"+network.getIpAddress())
  while True:
    try:
      command = network.read();
      if(command != None):
        print("Received '" + command + "'")
        network.write("Received '" + command + "'");
        display.success(command+"\n"+network.getIpAddress())
      else:
        time.sleep(1)
        print(".")
    except IOError:
      print("Connection lost")
      display.warning("Connection lost\n"+network.getIpAddress())
      break