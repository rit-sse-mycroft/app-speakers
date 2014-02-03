from mycroft.client import MycroftClient
import subprocess, pyaudio, socket, threading

def app_dependency(client, msg_type, data):
    client.up()

def msg_query(client, msg_type, data):
    if data['action'] == 'stream_tts':
        client_ip = data['data']['ip']
        port = data['data']['port']
        subprocess.call('vlc tcp://{0}:{1} vlc://quit'.format(client_ip, port))
    elif data['action'] == 'stream_video':
        subprocess.call('vlc {0} vlc://quit'.format(data['data']))
    elif data['action'] == 'stream_spotify':
        client_ip = data['data']['ip']
        port = data['data']['port']
        audio_client = socket.create_connection((client_ip, port))
        thread = threading.Thread(target=play_music, args=[audio_client])
        thread.start()

def play_music(client):
    chunk = 2048
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            output=True)

    while True:
        try:
            data = client.recv(8192)
            stream.write(data)
        except ConnectionResetError:
            break

    stream.stop_stream()
    stream.close()

    p.terminate()



client = MycroftClient('localhost', 1847, './app.json')
client.on('APP_DEPENDENCY', app_dependency)
client.on('MSG_QUERY', msg_query)
client.start()
