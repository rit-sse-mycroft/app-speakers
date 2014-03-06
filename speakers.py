"""
speakers.py

Speakers client for Mycroft.
USAGE:
`python speakers.py`
"""

import mycroft
import socket
import threading
import telnetlib
import random
import sys
import subprocess

# only import pyaudio if it is installed, otherwise just show a warning
try:
    import pyaudio
except ImportError:
    print("WARNING: pyaudio not found, functionality is limited")
    pyaudio = None


class Speakers(mycroft.App):

    def __init__(self):
        # initialize VLC
        if sys.platform == 'darwin':
            vlc = '/Applications/VLC.app/Contents/MacOS/VLC'
        else:
            vlc = 'vlc'

        # randomize which port is used (this should be enough)
        port = random.randint(2000, 60000)
        # start up vlc

        def start_vlc():
            subprocess.call(
                '{0} --extraint rc --rc-host=localhost:{1}'.format(
                    vlc,
                    port
                )
            )
        threading.Thread(target=start_vlc).start()
        self.vlc_conn = telnetlib.Telnet(
            host='localhost',
            port=port
        )

    @mycroft.on('APP_DEPENDENCY')
    def app_dependency(self, verb, body):
        self.up()

    @mycroft.on('MSG_QUERY')
    def msg_query(self, verb, body):
        if body['action'] == 'stream_tts':
            client_ip = body['data']['ip']
            port = body['data']['port']
            cmd = 'enqueue tcp://{0}:{1}\nplay\n'.format(client_ip, port)
            self.vlc_conn.write(cmd.encode('utf-8'))

        elif body['action'] == 'stream_video':
            cmd = 'enqueue {0}\nplay\n'.format(body['data'])
            self.vlc_conn.write(cmd)

        elif body['action'] == 'stream_spotify':
            client_ip = body['data']['ip']
            port = body['data']['port']
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

if __name__ == '__main__':
    app = Speakers()
    app.start('app.json', 'speakers')
