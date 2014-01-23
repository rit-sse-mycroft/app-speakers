require 'mycroft'
require 'socket'

class Speakers < Mycroft::Client

  attr_accessor :verified

  def initialize(host, port)
    @key = '/path/to/key'
    @cert = '/path/to/cert'
    @manifest = './app.json'
    @generate_instance_ids = true
    @port = 3000
    @verified = false
    super
  end

  def connect
    # Your code here
  end

  def on_data(parsed)
    if parsed[:type] == 'APP_MANIFEST_OK' or parsed[:type] == 'APP_MANIFEST_FAIL'
      check_manifest(parsed)
      @verified = true
      up
    elsif parsed[:type] == 'MSG_QUERY'
      if parsed[:data]["action"] == "stream_tts"
        clientIP = parsed[:data]['data']['ip']
        port = parsed[:data]['data']['port']
        `vlc tcp://#{clientIP}:#{port} --sout-all vlc://quit`
      elsif parsed[:data]["action"] == "stream_video"
        `vlc #{parsed[:data]} --sout-all vlc://quit`
      end
    end
  end

  def on_end
    # Your code here
  end
end

Mycroft.start(Speakers)
