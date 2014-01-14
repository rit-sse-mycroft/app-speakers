#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import sys

def main():
  s = None
  host = None
  MYCROFT_PORT = None
  s, host, MYCROFT_PORT = init(s, host, MYCROFT_PORT)
  manifest = getManifest()
  connectToMycroft(s, host, MYCROFT_PORT)
  sendManifest(s, manifest)
  checkManifest(s)
  print("Manifest approved")
  input("APP_UP?")
  s.send(bytes("6\nAPP_UP", 'UTF-8'))
  input("APP_DOWN?")
  s.send(bytes("8\nAPP_DOWN", 'UTF-8'))
  input("Close Connection?")
  s.close()

def init(s, host, MYCROFT_PORT):
  s = socket.socket()         # Create a socket object
  host = socket.gethostname() # Get local machine name
  MYCROFT_PORT = 1847                # Reserve a port for your service.
  return s, host, MYCROFT_PORT

def getManifest():
  return("APP_MANIFEST " + open("./app.json").read())

def connectToMycroft(s, host, MYCROFT_PORT):
  s.connect((host, MYCROFT_PORT))

def sendManifest(s, manifest):
  input("Send manifest?")
  size = len(bytes(manifest, 'UTF-8'))
  s.send(bytes((str(size)+"\n"+manifest), 'UTF-8'))

def checkManifest(s):
  msg = getMessage(s)
  split = msg.split() 

  if (split[0] != "APP_MANIFEST_OK"): #Checks that the manifest was approved, if not closes the connect.
    s.close()

def getMessage(s):
  char = (s.recv(1))
  msg = char

  while(char != bytes("\n", 'UTF-8')): #Read the message byte by byte to find the length
    char = (s.recv(1))
    msg += char

  msg = msg.decode('UTF-8') #decodes the message length.
  numBytes = int(msg[:(len(msg)-1)]) 
  msg = s.recv(numBytes) #Reads the rest of the message.

  msg = msg.decode('UTF-8') #decodes the message.	
  return msg


if __name__ == '__main__':
  main()