#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
MYCROFT_PORT = 1847                # Reserve a port for your service.
manifest = open("./app.json")

s.connect((host, MYCROFT_PORT))
s.send(manifest)
print (s.recv(1024))
s.close                # Close the socket when done