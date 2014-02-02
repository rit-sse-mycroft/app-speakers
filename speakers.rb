require 'mycroft'
require 'socket'
require './portaudio'

class Speakers < Mycroft::Client

  attr_accessor :verified

  def initialize(host, port)
    @key = '/path/to/key'
    @cert = '/path/to/cert'
    @manifest = './app.json'
    @port = 3000
    @verified = false
    super
  end
  
  on 'APP_DEPENDENCY' do |data|
    up
  end

  on 'MSG_QUERY' do |data|
    if data["action"] == "stream_tts"
      clientIP = data['data']['ip']
      port = data['data']['port']
      `vlc tcp://#{clientIP}:#{port} --sout-all vlc://quit`
    elsif data["action"] == "stream_video"
      `vlc #{data} --sout-all vlc://quit`
    end
  end

end

Mycroft.start(Speakers)
