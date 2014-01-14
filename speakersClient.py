#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import sys


s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
MYCROFT_PORT = 1847                # Reserve a port for your service.
manifest = "APP_MANIFEST " + open("./app.json").read()
size = sys.getsizeof(manifest)
s.connect((host, MYCROFT_PORT))
input("Send manifest?")
s.send(bytes((str(size)+"\n"+manifest), 'UTF-8'))
print("Manifest sent. Maybe?")
print (s.recv(1024)) 
s.close                # Close the socket when done