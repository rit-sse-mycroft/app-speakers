"""
speakers.py

Speakers client for Mycroft.
USAGE:
`python speakers.py`
"""

from mycroft.client import MycroftClient
import subprocess
import socket
import threading
import telnetlib
import random
import sys

# only import pyaudio if it is installed, otherwise just show a warning
try:
    import pyaudio
except ImportError:
    print("WARNING: pyaudio not found, functionality is limited")
    pyaudio = None


class Speakers:

    def __init__(self, client):
        self.client = client
        # initialize VLC
        if sys.platform == 'darwin':
            vlc = '/Applications/VLC.app/Contents/MacOS/VLC'
        else:
            vlc = 'vlc'

        # randomize which port is used (this should be enough)
        port = random.randint(2000, 60000)
        # start up vlc
        subprocess.call(
            '{0} --extraint rc --rc-host=localhost:{1}'.format(
                vlc,
                port
            )
        )
        self.vlc_conn = telnetlib.Telnet(
            host='localhost',
            port=port
        )

    def app_dependency(self, client, msg_type, data):
        self.client.up()

    def msg_query(self, client, msg_type, data):
        if data['action'] == 'stream_tts':
            client_ip = data['data']['ip']
            port = data['data']['port']
            cmd = 'enqueue tcp://{0}:{1}\n'.format(client_ip, port)
            self.vlc_conn.write(cmd)

        elif data['action'] == 'stream_video':
            cmd = 'enqueue {0}'.format(data['data'])
            self.vlc_conn.write(cmd)

        elif data['action'] == 'stream_spotify':
            client_ip = data['data']['ip']
            port = data['data']['port']
            audio_client = socket.create_connection((client_ip, port))
            thread = threading.Thread(target=play_music, args=[audio_client])
            thread.start()

    def play_music(self, client):
        if not pyaudio:
            print("WARNING: Cannot play this stream; pyaudio not installed")
            return

        chunk = 2048
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            output=True
        )

        while True:
            try:
                data = client.recv(8192)
                stream.write(data)
            except ConnectionResetError:
                break

        stream.stop_stream()
        stream.close()

        p.terminate()

client = MycroftClient('speakers', 'localhost', 1847, './app.json')
speakers = Speakers(client)
client.on('APP_DEPENDENCY', speakers.app_dependency)
client.on('MSG_QUERY', speakers.msg_query)
client.start()
