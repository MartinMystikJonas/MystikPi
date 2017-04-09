import sys
sys.path.insert(0,'../../Library')

import time
import traceback
from grovepi import *
from Network import *
from RgbDisplay import *

# settings
networkPort = 12346

# configuration
network = Network(networkPort)
display = RgbDisplay()

#commands

def executeCommand(command):
  if(command == "beep"):
    digitalWrite(3, 1);
    sleep(0.2)
    digitalWrite(3, 0);
  else:
    network.write("Unknown command")


# init
display.warning("Loading...\n"+network.getIpAddress()+":"+str(networkPort))

time.sleep(3)

print("Waiting for connection")
display.info("Ready on "+str(networkPort)+"\n"+network.getIpAddress()+":"+str(networkPort))

while True:

  try:

    network.waitForConnection()
    print("Connected")
    display.success("Connected\n"+network.getIpAddress())

    while True:
      try:
        command = network.read();
        if(command != None):
          print("Received '" + command + "'")
          network.write(command);
          display.success(command+"\n"+network.getIpAddress())
          executeCommand(command)
        else:
          time.sleep(0.1)
      except ConnectionLost:
        print("Connection lost")
        display.warning("Connection lost\n"+network.getIpAddress())
        break
      except:
        print("Unexpected error " + traceback.format_exc());

  except KeyboardInterrupt:
    break
  except:
    print("Unexpected error " + traceback.format_exc());