#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import sys
import threading
import json
import pygame
import random

pygame.mixer.init(frequency=15050, size=-16, channels=2, buffer=4096)

def main():
  mycroft = None
  host = None
  MYCROFT_PORT = None
  mycroft, host, MYCROFT_PORT = init(mycroft, host, MYCROFT_PORT)
  manifest = getManifest()
  connectToMycroft(mycroft, host, MYCROFT_PORT)
  sendManifest(mycroft, manifest)
  checkManifest(mycroft)
  print("Manifest approved")
  mycroft.send(bytes("6\nAPP_UP", 'UTF-8')) #APP_UP
  
  threadCount = 0
  while threadCount < 5:
    threading.Thread(target=runThread(mycroft)).start()
    threadCount += 1

def runThread(mycroft):
	while True:
		handleMessage(mycroft)

def init(mycroft, host, MYCROFT_PORT):
  mycroft = socket.socket()         # Create a socket object
  host = socket.gethostname() # Get local machine name
  MYCROFT_PORT = 1847                # Reserve a port for your service.
  return mycroft, host, MYCROFT_PORT

def getManifest():
  return("APP_MANIFEST " + open("./app.json").read())

def connectToMycroft(mycroft, host, MYCROFT_PORT):
  mycroft.connect((host, MYCROFT_PORT))

def sendManifest(mycroft, manifest):
  size = len(bytes(manifest, 'UTF-8'))
  mycroft.send(bytes((str(size)+"\n"+manifest), 'UTF-8'))

def checkManifest(mycroft):
  msg = getMessage(mycroft)
  splitMsg = msg.split() 

  if (splitMsg[0] != "APP_MANIFEST_OK"): #Checks that the manifest was approved, if not closes the connect.
    mycroft.close()

def handleMessage(mycroft):
  msg = getMessage(mycroft)
  splitMsg = msg.split()
  parseMsg = json.loads(splitMsg[1])
  print("got a message")
  print(splitMsg)
  print(parseMsg)
  if (parseMsg['remoteProcedure'] == "doStream"):
  	stream = connectToStream(parseMsg['port'], parseMsg['ip'], parseMsg['id'])
  	playSound(stream)

def playSound(stream):
  audio = pygame.mixer
  audio.Channel(1)
  sound = audio.Sound(buffer = stream.recv(200*1024))
  sound.play()	

def connectToStream(port, ip, id):
  stream = socket.socket()
  stream.connect(('localhost', port))
  stream.send(bytes(id, 'UTF-8'))
  return stream

def getMessage(mycroft):
  char = (mycroft.recv(1))
  msg = char

  while(char != bytes("\n", 'UTF-8')): #Read the message byte by byte to find the length
    char = (mycroft.recv(1))
    msg += char

  msg = msg.decode('UTF-8') #decodes the message length.
  numBytes = int(msg[:(len(msg)-1)]) 
  msg = mycroft.recv(numBytes) #Reads the rest of the message.

  msg = msg.decode('UTF-8') #decodes the message.	
  return msg


if __name__ == '__main__':
  main()
