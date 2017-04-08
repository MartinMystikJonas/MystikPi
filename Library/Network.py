import socket
import errno
import time

class Network(object):
  port = 0
  serversocket = None
  clientsocket = None
  address = None

  def __init__(self, port):
    port = port
    self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.serversocket.bind(('', port))
    self.serversocket.listen(5)
    print("[Network] Listening for connections on " + self.getIpAddress() + ":" + str(port));

  def getIpAddress(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipAddress = s.getsockname()[0]
    s.close()
    return ipAddress

  def waitForConnection(self):
    (clientsocket, address) = self.serversocket.accept()
    self.clientsocket = clientsocket
    self.address = address
    self.clientsocket.setblocking(0)
    print("[Network] " + str(self.address) + " Connection accepted")

  def read(self):
   try:
     messageRaw = self.clientsocket.recv(1024)
     if (not messageRaw) or (messageRaw[0] == 255):
       print ("[Network] " + str(self.address) + " Connection lost")
       raise IOError("Connection lost")
     message = messageRaw.decode().rstrip()
     print ("[Network] " + str(self.address) + " <<< " + message)
     return message
   except socket.error as e:
     err = e.args[0]
     if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
       return None
     else:
       raise

  def write(self, message):
    fullMessage = message + "\r\n";
    self.clientsocket.send(fullMessage.encode())
    print ("[Network] " + str(self.address) + " >>> " + message)
    return message

if __name__=="__main__":
  network = Network(12346);
  while True:
    print("Waiting for connection")
    network.waitForConnection()
    print("Connected")
    while True:
      try:
        command = network.read();
        if(command != None):
          print("Received '" + command + "'")
          network.write("Received '" + command + "'");
        else:
          time.sleep(1)
          print(".")
      except IOError:
        print("Connection lost")
        break
